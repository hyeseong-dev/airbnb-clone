import uuid
from django.conf                import settings
from django.contrib.auth.models import AbstractUser
from django.db                  import models
from django.core.mail           import send_mail


class User(AbstractUser):

    """ Custom User Model"""

    GENDER_MALE =  "Male"
    GENDER_FEMALE ="Female"
    GENDER_OTHER = "Other"

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER,  "Other"),   
    ]

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = [
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    ]

    CURRENCY_USD = 'usd'
    CURRENCY_KRW = 'krw'

    CURRENCY_CHOICES =[
        (CURRENCY_USD, 'USD'),
        (CURRENCY_KRW, 'KWD'),
    ]

    avatar          = models.ImageField(upload_to='avatars', blank=True )
    gender          = models.CharField(choices=GENDER_CHOICES, max_length=10,  blank=True )
    bio             = models.TextField(blank=True)
    birthdate       = models.DateField(null=True, blank=True)
    language        = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN)
    currency        = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=CURRENCY_KRW)
    superhost       = models.BooleanField(default=False)
    email_verified  = models.BooleanField(default=False)
    email_secret    = models.CharField(max_length=20, default='', blank=True)

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20] # 16진수 20개의 문자열을 생성함
            self.email_secret = secret
            send_mail(
                'Verify AirBnB Account', # 제목 부분
                f"Verify Account, This Is Your Secret: {secret}", # 메시지, 바디에 해당
                settings.EMAIL_FROM, # 누구로 부터온 이메일
                [self.email], # 이메일 받는 사람
                fail_silently=False, # 오류발생시 조용히 할거냐 말거냐?
            )
            print('여기까지 오긴하네')
        return
    class Meta:
        db_table = 'users'