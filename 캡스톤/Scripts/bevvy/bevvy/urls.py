
from django.contrib import admin
from django.urls import path
from django.conf.urls import url # 새로 추가함 db 받으라고

from user.views import AboutView, SocialLoginCallbackView
from rating.views import RatingPage, ResultPage, checkdata, MyPage, MyPageTap



# , beer_recommend
# , polls
from django.contrib.auth.views import LogoutView  #로그아웃!



urlpatterns = [
    path('test/',checkdata.as_view()),
    path('mypage/',MyPage.as_view()),
    path('mypage/tap',MyPageTap.as_view()),

    # url(r'^polls/$',polls),
    # path('polls/',polls),
    # url(r'^rating/$',polls),
    # url(r'^$', beer_recommend, name='beer_recommend'),

    # path("result/", beer_recommend, name='beer_recommend'), #이거는 수정된거

    path('login/',AboutView.as_view()),
    path('user/login/social/<provider>/callback/', SocialLoginCallbackView.as_view()),
    path('rating/',RatingPage.as_view()),

    path('result/',ResultPage.as_view()),  #이거는 수정전꺼

    path('logout/', LogoutView.as_view()),
    path('admin/', admin.site.urls),
]
