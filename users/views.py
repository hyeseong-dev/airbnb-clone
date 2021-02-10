import os
import requests
import pprint
from django.views         import View
from django.views.generic import FormView
from django.urls          import reverse_lazy
from django.shortcuts     import render, redirect, reverse, redirect
from django.contrib.auth  import authenticate, login, logout
from users                import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {"first_name": "Nicoas", "last_name": "Serr", "email": "itn@las.com"}

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ''
        user.save()
        # to do : add success message
    except models.User.DoesNotExist:
        # to do : add error message
        pass
    return redirect(reverse('core:home'))


def github_login(request):
    client_id = os.environ.get('GH_ID')
    redirect_url = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(
        f"http://github.com/login/oauth/authorize?client_id={client_id}&redirect_url={redirect_url}&scope=read:user"
    )

class GithubException(Exception):
    pass

def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            result = requests.post( # requests library를 이용해서 post요청
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept":"application/json"},
            )
            result_json = result.json()
            error = result_json.get("error", None)
            if error is not None: # 깃헙 로그인이 10분이상 지체? 되거나 오류시
                raise GithubException()
            else:
                access_token = result_json.get('access_token')
                profile_request= requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization":f"token {access_token}",
                        "Accept": "application/json",
                    },
                    )
                
                pprint.pprint(profile_request.json())
                username = profile_json.get('login', None)
                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email')
                    bio = profile_json.get('bio')
                    models.User.objects.get(email=email)
                    if user is not None:
                        return redirect(reverse("users:login"))
                    else:
                        user = models.User.objects.create(
                            username=email, first_name=name, bio=bio, email=email)
                        login(request, user)
                        return redirect(reverse('core:home'))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))

        