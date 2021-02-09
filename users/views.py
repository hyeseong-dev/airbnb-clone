from django.views       import View
from django.shortcuts   import render, redirect
from users              import forms

class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={'email':"itn@las.com"})
        return render(request, 'users/login.html',context={'form':form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data,'로그인 뷰의 포스트 데이터의 폼.클린데이터 호출')
        return render(request, 'users/login.html', {"form":form})