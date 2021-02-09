from django.views         import View
from django.views.generic import FormView
from django.urls          import reverse_lazy
from django.shortcuts     import render, redirect, reverse
from django.contrib.auth  import authenticate, login, logout
from users                import forms

# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForm(initial={'email':"itn@las.com"})
#         return render(request, 'users/login.html',context={'form':form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST) # forms.py에서 처리한 로직을 form 변수에서 가져옴. 통상 아이디, 비번 정보를 담고 있음
#         if form.is_valid():                  # 데이터가 유효성 검증
#             email    = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse('core:home'))
#         return render(request, 'users/login.html', {"form":form})

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
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))