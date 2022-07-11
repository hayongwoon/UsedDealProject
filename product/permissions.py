from rest_framework.permissions import BasePermission
from django.db.models import Avg, Count


class IsRegisterdMoreThanTwoRliabilityPoint(BasePermission):
    """
    거래 신뢰도가 2 보다 높은 사용자는 쓰기, 수정, 삭제 가능
    이외에는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        reviews = user.deal_seller
        reviews_avg = reviews.aggregate(avg=Avg('rating'))["avg"]
        reviews_cnt = reviews.aggregate(cnt=Count('rating'))["cnt"]
        user_reliability_point = '{:.2f}'.format(((reviews_avg * reviews_cnt) + user.deal_reliability_avg) / (reviews_cnt + 1))

        if request.method in self.SAFE_METHODS or \
            user.is_authenticated and user_reliability_point > 2:

            return True

        return False
