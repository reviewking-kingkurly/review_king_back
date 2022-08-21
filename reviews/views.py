import json
import boto3, uuid

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from reviews.models       import Review, ReviewImage, ProductPurchasedWith, KeywordFromReview
from products.models      import Product, SubCategory, OrderedItem
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
        
    @login_decorator
    def get(self, request):
        try:
            data            = json.loads(request.body)
            user            = request.user
            ordered_item_id = data['ordered_item_id']
            
            order_item = OrderedItem.objects.get(id=ordered_item_id)
            
            if order_item.order.user_id != user.id:
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)
            
            results = {
                'product_id'            : order_item.product.id,
                'product_name'          : order_item.product.name,
                'product_price'         : order_item.product.price,
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
            
            return JsonResponse({'results': results}, status=200)
        
        except OrderedItem.DoesNotExist:
            return JsonResponse({'message': 'ORDER_ITEM_DOES_NOT_EXIST'}, status=404)
        
class ReviewDetailView(View):
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
