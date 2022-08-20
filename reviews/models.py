from django.db import models

from core.models import TimeStampModel

class Review(TimeStampModel): 
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta: 
        db_table = "reviews"

class ReviewImage(models.Model): 
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    img_url = models.URLField(max_length=500)

    class Meta: 
        db_table = "review_images"

class ProductPurchasedWith(models.Model): 
    review  = models.ForeignKey('Review', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta: 
        db_table = "purchased_with"

class KeywordFromReview(models.Model): 
    review       = models.ForeignKey('Review', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('products.SubCategory', on_delete=models.CASCADE)
    
    class Meta: 
        db_table = "keywords_from_review"

class Like(TimeStampModel): 
    user   = models.ForeignKey("users.User", on_delete=models.CASCADE)
    review = models.ForeignKey("Review", on_delete=models.CASCADE)

    class Meta: 
        db_table = "likes"