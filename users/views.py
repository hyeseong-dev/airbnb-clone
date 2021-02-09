from django.views        import View
from django.shortcuts    import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from users               import forms

class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={'email':"itn@las.com"})
        return render(request, 'users/login.html',context={'form':form})

    def post(self, request):
        form = forms.LoginForm(request.POST) # forms.py에서 처리한 로직을 form 변수에서 가져옴. 통상 아이디, 비번 정보를 담고 있음
        if form.is_valid():                  # 데이터가 유효성 검증
            email    = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('core:home'))
        return render(request, 'users/login.html', {"form":form})

def log_out(request):
    logout(request)
    return redirect(reverse('core:home'))