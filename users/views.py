from django.views       import View
from django.shortcuts   import render, redirect
from users              import forms

class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={'email':"itn@las.com"})
        return render(request, 'users/login.html',context={'form':form})

    def post(self, request):
        form = forms.LoginForm(request.POST) # forms.py에서 처리한 로직을 form 변수에서 가져옴. 통상 아이디, 비번 정보를 담고 있음
        if form.is_valid():                  # 데이터가 유효성 검증
            print(form.clean_data)
        return render(request, 'users/login.html', {"form":form})