import json
import boto3, uuid

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction
from django.db.models import Count
from datetime         import date, timedelta
from operator         import itemgetter

from reviews.models       import Review, ReviewImage, ProductPurchasedWith, KeywordFromReview, Like
from products.models      import Product, SubCategory, OrderedItem, Order
from core.utils           import login_decorator
from core.review_keyword  import review_keyword
from review_king.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)

class ReviewView(View):
    @login_decorator
    def post(self, request):
        try:
            user       = request.user
            product_id = request.POST['product_id']
            content    = request.POST['content']
            files      = request.FILES.getlist('files')
            product_id_purchased_with = request.POST.getlist('product_id_purchased_with')
            
            s3resource = boto3.resource('s3', aws_access_key_id= AWS_ACCESS_KEY_ID, aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
            
            product = Product.objects.get(id=product_id)
            
            if Review.objects.filter(user_id=user.id, product_id=product_id):
                return JsonResponse({'message' : 'THE_REVIEW_ALREADY_EXISTS'}, status=404)
            
            with transaction.atomic():
                review = Review.objects.create(
                    user    = user,
                    product = product,
                    content = content,
                )
                
                for file in files :
                    file._set_name(str(uuid.uuid4()))
                    s3resource.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key='/%s'%(file), Body=file)
                    ReviewImage.objects.create(
                        review  = review,
                        img_url = 'https://review-king-kurly.s3.ap-northeast-2.amazonaws.com/'+"/%s"%(file),
                    )
                    
                for product_id in product_id_purchased_with :
                    ProductPurchasedWith.objects.create(
                        review     = review,
                        product_id = product_id
                    )
                    
                review_keyword_subcategories = review_keyword(review.id)
                for subcategory in review_keyword_subcategories:
                    if SubCategory.objects.get(name=subcategory):
                        subcategory = SubCategory.objects.get(name=subcategory)
                        if subcategory.id != review.product.sub_category.id:
                            KeywordFromReview.objects.create(
                                review       = review,
                                sub_category = subcategory
                            )
                        
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except transaction.TransactionManagementError:
            return JsonResponse({'message': 'TRANSACTION_MANAGEMENT_ERROR'}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)
        
class WriteReviewView(View):
    @login_decorator
    def get(self, request, ordered_item_id):
        try:
            user = request.user
            
            order_item = OrderedItem.objects.get(id=ordered_item_id)
            
            if order_item.order.user_id != user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)
            
            results = {
                'order_number'          : order_item.order.order_num,
                'product_id'            : order_item.product.id,
                'product_name'          : order_item.product.name,
                'product_price'         : order_item.product.price,
                'product_description'   : order_item.product.description,
                'product_quantity'      : order_item.quantity,
                'product_thumbnail'     : order_item.product.thumbnail,
                'delivery_date'         : [delivery.delievery_date for delivery in order_item.delivery_set.all()],
                'order_status'          : order_item.order.order_status.status,
                'product_purchased_with':[{
                    'product_id'       : product_with.product.id,
                    'product_name'     : product_with.product.name,
                    'product_thumbnail': product_with.product.thumbnail,
                    'product_price'    : product_with.product.price
                } for product_with in order_item.order.ordereditem_set.all()]
            }
            
            return JsonResponse({'message': 'SUCCESS', 'results': results}, status=200)
        
        except OrderedItem.DoesNotExist:
            return JsonResponse({'message': 'ORDER_ITEM_DOES_NOT_EXIST'}, status=404)
        
class ReviewDetailView(View):
    @login_decorator
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            
            results = {
                'id': review.id,
                'user_name'             : review.user.name,
                'user_grade'            : review.user.grade,
                'content'               : review.content,
                'created_at'            : review.created_at,
                'review_image'          : [review_image.img_url for review_image in review.reviewimage_set.all()],
                'product_id'            : review.product.id,
                'product_name'          : review.product.name,
                'product_description'   : review.product.description,
                'review_like'           : review.like_set.all().count(),
                'review_like_choice'    : [like.id for like in review.like_set.filter(user=request.user)],
                'product_purchased_with':[{
                    'product_id'       : product_with.product.id,
                    'product_name'     : product_with.product.name,
                    'product_price'    : product_with.product.price,
                    'product_thumbnail': product_with.product.thumbnail
            } for product_with in review.productpurchasedwith_set.all()]
            }
            
            return JsonResponse({'results': results}, status=200)
        
        except Review.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

class WriteReviewListView(View):
    @login_decorator
    def get(self, request):
        user   = request.user
        orders = Order.objects.filter(user=user,ordered_at__range=[
            date.today() - timedelta(days=30), date.today() + timedelta(days=1)
            ])
        results = [{
            'order_number' : order.order_num,
            'order_status' : order.order_status.status,
            'ordered_at'   : order.ordered_at,
            'product'      :[{
                'product_id'       : order_item.product.id,
                'product_name'     : order_item.product.name,
                'product_thumbnail': order_item.product.thumbnail,
                'review_id'        : [review.id for review in order_item.product.review_set.filter(user=user)]
            } for order_item in order.ordereditem_set.all()]
        } for order in orders]
        
        return JsonResponse({'results': results}, status=200)

class BestReviewListView(View):
    def get(self, request):
        reviews = Review.objects.filter(created_at__range=[
            date.today() - timedelta(days=30), date.today() + timedelta(days=1)
            ]).annotate(review_like=Count('like')).order_by('-like')[:10]
        
        results = [{
            'review_id'         : review.id,
            'review_content'    : review.content,
            'product_id'        : review.product.id,
            'product_name'      : review.product.name,
            'product_thumbnail' : review.product.thumbnail,
            'product_price' : review.product.price,
        } for review in reviews]
        
        return JsonResponse({'results': results}, status=200)

class ReviewRankingCategoryView(View):
    def get(self, request):
        sub_categories = SubCategory.objects.all()
        sub_category_names = [sub_category.name for sub_category in sub_categories]
        
        category_list = []
        
        for sub_category_name in sub_category_names:
            review = Review.objects.filter(product_id__sub_category__name=sub_category_name)
            sub_category = sub_categories.get(name=sub_category_name)
            category_list.append({
                'sub_category'      : sub_category.id,
                'sub_category_name' : sub_category.name,
                'review_count'      : review.count(),
                'product'           : [{
                    'product_id'        : product.id,
                    'product_name'      : product.name,
                    'product_thumbnail' : product.thumbnail,
                }for product in sub_category.product_set.all()]
            })
        
        results = sorted(category_list, key=itemgetter('review_count'), reverse=True)[:5]
        
        return JsonResponse({'results': results}, status=200)

class ReviewLikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            review_id = data['review_id']
            
            review = Review.objects.get(id=review_id)
            like, flag = Like.objects.get_or_create(review=review,user=request.user)
            
            if not flag:
                like.delete()
                message = 'NO_CONTENT'
                
            else:
                message = 'SUCCESS'
                
            return JsonResponse({'message': message}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class ReviewListView(View):
    def get(self, request, product_id):
        try:            
            reviews = Review.objects.filter(product_id=product_id)
            
            review_list = [{
                'id': review.id,
                'user_name'             : review.user.name,
                'user_grade'            : review.user.grade,
                'content'               : review.content,
                'created_at'            : review.created_at,
                'review_image'          : [review_image.img_url for review_image in review.reviewimage_set.all()],
                'review_like'           : review.like_set.all().count(),
            }for review in reviews]
            
            results = sorted(review_list, key=itemgetter('review_like'), reverse=True)
            
            return JsonResponse({'results': results}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)