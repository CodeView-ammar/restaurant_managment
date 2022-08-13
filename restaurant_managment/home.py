from django.shortcuts import render
from django.contrib.auth import views as auth_views #new


# def index(request):
#     return render(request, 'index.html',{})
# def index(request):
#     if request.method == 'POST':
#         formlog = auth_views.LoginView.as_view(template_name='configrate/login.html')

#         if 'login' in request.POST:
#             if formlog.is_valid():
#                 formlog.save()
#                 username = form.cleaned_data.get('username')
#                 messages.success(request, f'Your account has been created! You are now able to log in')
#                 return redirect('\\')
#     else:
#         form =
#         formlog = auth_views.LoginView.as_view(template_name='index.html')
#     return render(request, 'index.html', {'form': form, 'formlog': formlog})