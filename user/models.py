from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True)

    # 실제 사용자들은 전화번호로 서로 연락하여 중고거래를 하기 때문에 해당 필드를 추가했고, 정규식을 활용해서 해당 필드를 입력 받을 것이다.
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)

    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

    # 거래 후 구매자는 판매자에게 거래 신뢰도 점수를 줄 수 있고, 5점 만점에 소숫점 1번째 자리까지 나타낸다.
    deal_reliability_avg = models.DecimalField("거래 신뢰도", max_digits=3, decimal_places=2, default=5)

    # default가 있는 경우, Post시리얼라이즈에서는 필드에서 제외한다.
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(to='WatchList', verbose_name="관심 목록") 
    introduction = models.TextField("소개")
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")

    def __str__(self) -> str:
        return f'{self.user.username}님의 프로필 입니다.'

class WatchList(models.Model):
    name = models.CharField("관심 목록", max_length=50)

    def __str__(self):
        return self.name
