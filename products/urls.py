from django.urls import path

from products.views import ProductDetailView, RelatedCategoryView, RelatedProductView, PurchasedProductView, SearchView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/<int:product_id>/related_cate', RelatedCategoryView.as_view()),
    path('/<int:product_id>/related_prod', RelatedProductView.as_view()),
    path('/<int:product_id>/pruchased_prod', PurchasedProductView.as_view()),
    path('/search', SearchView.as_view())
]