# -*- coding: utf-8 -*-
import re

from thefuzz     import fuzz, process
from konlpy.tag  import Hannanum

from reviews.models  import Review
from products.models import SubCategory

def review_keyword(review_id):
    # 다른 파일 리뷰, 상품명 불러오기
    review = Review.objects.get(id=review_id)
    review = review.content
    review = re.sub('[0-9]+', '', review)
    review = re.sub('[A-Za-z]+', '', review)
    review = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》]', '', review)
    hannanum = Hannanum()
    keyword_list = hannanum.nouns(review)
    subcategories = [subcategory.name for subcategory in SubCategory.objects.all()]
    result = []
    for keyword in keyword_list:
        match = process.extract(keyword, subcategories, scorer=fuzz.partial_ratio)
        for match in match:
            if match[1] >= 100:
                result.append(match[0])
    my_set = set(result) #집합set으로 변환
    result = list(my_set) #list로 변환

    return result