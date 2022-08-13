from django.shortcuts import render

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from .forms import UserForm
from django.views.generic.edit import CreateView
from django.http import  JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views #new
from django.views import View
from .forms import RegisterForm

# class get_users(CreateView):
#     def get(self, request, *args, **kwargs):
#         user=User.objects.all()
#         fileduse=UserForm()
#         context={
#             "user":user,
#             "filed":fileduse
#         }
    
#         return render(request, 'configrate/users.html',context)


#     def post(self, request, *args, **kwargs):
#         if  not request.POST.get("username"):
            
#             context={
#                 "status":0,
#                 "message":"لا يوجد اسم مستخدم"
#             }
#             return JsonResponse(context)
#         if not  request.POST.get("password1") or not  request.POST.get("password2"):
#             context={
#                 "status":0,
#                 "message":"يجب عليك كتابة كلمة المرور"
#             }
#             return JsonResponse(context)
#         print("first_name"*10)
#         if request.method == 'POST':
#             print(request.POST.get('username'))
         
#         # obje=User.objects.create_user(
#         #     request.POST.get("username"),
#         #     request.POST.get("email"),
#         #     request.POST.get("password1"),
#         #     request.POST.get("first_name"),
#         #     request.POST.get("list_name"),
#         # )
#         user = User.objects.create_user(
#             username=request.POST.get("username"),
#             email=request.POST.get("email"),
#             password=request.POST.get("password1"),
#             first_name=request.POST.get("first_name"),                 
#             last_name=request.POST.get("list_name"),                 
#                                  )
        
#         user.save()

#         if user.id:
#             context={
#                     "status":1,
#                     "message":"تم الحفظ"
#                 }
#         else:
#             context={
#                     "status":0,
#                     "message":"خطاء في الحفظ"
#                 }
#         return JsonResponse(context)
        # if form.is_valid():
        #     book = form.save()
        #     book.save()
        #     return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
        # return render(request, 'books/book-create.html', {'form': form})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'configrate/users.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        # if request.user.is_authenticated:
        #     return redirect(to')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            context={
                    "status":1,
                    "message":"تم الحفظ"
                }
        else:
            context={
                "status":0,
                "message":form.errors
            }
    
        return JsonResponse(context)


# def get_users(request):
#     user=UserR.objects.all()
#     fileduse=UserForm()
#     context={
#         "user":user,
#         "filed":fileduse
#     }
    
#     return render(request, 'configrate/users.html',context)


class UserDataJson(BaseDatatableView):
    # The model we're going to show
    model = User

    # define the columns that will be returned
    columns = [
    'id',
    "first_name",
    "last_name",
    "username",
    ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non-sortable columns use empty
    # value like ''
    order_columns = [
    'id',
    "first_name",
    "last_name",
    "username",

    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500
    count = 0
    def render_column(self, row, column):
        if column == "id":
            self.count += 1
            return self.count
        else:
            # We want to render user as a custom column
            return super(UserDataJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

