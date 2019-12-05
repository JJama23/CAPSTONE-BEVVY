# user/views.py
from user.models import User

from django.views.generic import TemplateView #이거 맞나?
from django.conf import settings
from django.views.generic.base import View
from django.middleware.csrf import _compare_salted_tokens
from user.oauth.providers.naver import NaverLoginMixin

from django.contrib.auth import get_user_model
# from user.forms import UserRegistrationForm, LoginFor
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect




# 생략
# class UserLoginView(LoginView):           # 회원가입 한걸로의 로그인 기능
#     authentication_form = LoginForm
#     template_name = 'user/login_form.html'
#
#     def form_invalid(self, form):
#         messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
#         return super().form_invalid(form)

#
class AboutView(TemplateView):
    template_name = 'user/login_form.html'

class SocialLoginCallbackView(NaverLoginMixin, View):

    success_url = settings.LOGIN_REDIRECT_URL
    failure_url = settings.LOGIN_URL
    required_profiles = ['email', 'name']
    model = get_user_model()

    def get(self, request, *args, **kwargs):

        provider = kwargs.get('provider')

        if provider == 'naver': # 프로바이더가 naver 일 경우
            csrf_token = request.GET.get('state')
            code = request.GET.get('code')
            if not _compare_salted_tokens(csrf_token, request.COOKIES.get('csrftoken')): # state(csrf_token)이 잘못된 경우
                # messages.error(request, '잘못된 경로로 로그인하셨습니다.', extra_tags='danger')
                return HttpResponseRedirect(self.failure_url)
            is_success, error = self.login_with_naver(csrf_token, code)
            if not is_success: # 로그인 실패할 경우
                messages.error(request, error, extra_tags='danger')
            return HttpResponseRedirect(self.success_url if is_success else self.failure_url)

        return HttpResponseRedirect(self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value
