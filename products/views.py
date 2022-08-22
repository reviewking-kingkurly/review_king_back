from django.http  import JsonResponse
from django.views import View

from products.models import Product, SubCategory
from reviews.models  import Review
from reviews.models  import KeywordFromReview, ProductPurchasedWith

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.select_related('sub_category').get(id=product_id)
            product_detail = {
                'product_id'          : product.id,
                'product_sub_category': product.sub_category.id,
                'product_name'        : product.name,
                'product_description' : product.description,
                'product_price'       : product.price,
                'product_thumbnail'   : product.thumbnail,
            }
            return JsonResponse({"results" : product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "PRODUCT_DOES_NOT_EXIST"}, status=404)

class RelatedCategoryView(View):
    def get(self, request, product_id):
        related_products = KeywordFromReview.objects.filter(review__product_id = product_id)
        related_products_list = list(set(related_product.sub_category_id for related_product in related_products))
        
        count_list = []
        for sub_category_id in related_products_list:
            sub_category_count = related_products.filter(sub_category_id = sub_category_id).count()
            count_list.append(sub_category_count)
        total_count = sum(sorted(count_list, reverse=True)[:5])

        related_categories_list = []
        for sub_category_id in related_products_list:
            related_categories = {
                'sub_category_id' : sub_category_id,
                'sub_category_name' : SubCategory.objects.get(id = sub_category_id).name,
                'sub_category_count' : related_products.filter(sub_category_id = sub_category_id).count(),
                'sub_category_share': round(related_products.filter(sub_category_id = sub_category_id).count()/total_count*100)
            }
            related_categories_list.append(related_categories)
        related_categories_list = sorted(related_categories_list, key=lambda x:x['sub_category_count'], reverse=True)[:5]
        
        return JsonResponse({"total_count" : total_count, "results" : related_categories_list}, status=200)

class RelatedProductView(View):
    def get(self, request, product_id):
        try:
            sub_category       = int(request.GET.get('sub_category'))
            related_products   = KeywordFromReview.objects.filter(review__product_id = product_id)
            related_categories = list(set(related_product.sub_category_id for related_product in related_products))

            if sub_category in related_categories:
                products = Product.objects.filter(sub_category_id = sub_category).order_by("?")
                related_product_list = [{
                    'product_id'   : product.id,
                    'product_name' : product.name,
                    'product_price': product.price,
                } for product in products]
                return JsonResponse({"results" : related_product_list}, status=200)
            
            else:
                return JsonResponse({"message" : "INVALID_SUB_CATEGORY"}, status=400)

        except TypeError:
            return JsonResponse({"message" : "MUST_ENTER_SUB_CATEGORY_ON_URI"}, status=400)

        except ValueError:
            return JsonResponse({"mesasge" : "MUST_PUT_VALUE_OF_SUB_CATEGORY"}, status=400)

class PurchasedProductView(View):
    def get(self, request, product_id):
        purchased_products = ProductPurchasedWith.objects.select_related('product').filter(review__product_id = product_id)
        purhcased_products_list = [{
            'product_id'       : purchased_product.product.id,
            'product_name'     : purchased_product.product.name,
            'product_price'    : purchased_product.product.price,
            'product_thumbnail': purchased_product.product.thumbnail,
        } for purchased_product in purchased_products]
        
        return JsonResponse({"results" : purhcased_products_list}, status=200)

class SearchView(View):
    def get(self, request):
        products = Product.objects.all()
        product_list = [{
            'product_id'       : product.id,
            'product_name'     : product.name,
            'product_price'    : product.price,
            'product_thumbnail': product.thumbnail
        } for product in products]

        reviews = Review.objects.select_related('product').all()
        review_list = [{
            'review_id'     : review.id,
            'product_id'    : review.product.id,
            'product_name'  : review.product.name,
            'review_content': review.content,
        } for review in reviews]

        return JsonResponse({"product" : product_list, "review" : review_list}, status=200)