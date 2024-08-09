from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from accounts import models
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views import View
from django.views.generic import View,ListView , DetailView, CreateView, DeleteView, UpdateView, RedirectView,TemplateView,FormView
from django.urls import reverse,reverse_lazy
from .decorators import *
import math

# Create your views here.


class IndexView(TemplateView):
    template_name = 'accounts/index_class.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sample_text1'] = "Sample Test1"
        context['sample_text2'] = "Sample Test2"
        return context

# class IndexListView(ListView):
#     template_name = 'accounts/index_class.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['customers'] = Customer.objects.all()
#         context['orders'] = Order.objects.all()
#         return context
# class IndexListView(ListView):
#     template_name = 'accounts/index_class.html'

#     def get_queryset(self):
#         # Provide the queryset for the main list
#         return Customer.objects.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['orders'] = Order.objects.all()  # Add additional context data
#         return context
# class CustomerDetail(DeleteView):
#     context_object_name = 'Customer'
#     model = models.Customer
#     template_name = 'accounts/Customer_details.html'


# class AddCustomer(CreateView):
#     fields= "__all__"
#     model = models.Customer
#     template_name = 'accounts/customer_form.html'

# class UpdateCustomer(UpdateView):
#     fields= "__all__"
#     model = models.Customer

# class DeleteCustomer(DeleteView):
#     model = models.Customer
#     context_object_name = 'cust'
#     success_url = reverse_lazy("testListView")
#     template_name = "accounts/delete_customer.html"        


unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )
            messages.success(request, 'Account was created for :' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or Password is Incorrect')
            # return render(request,'accounts/login.html', context)
    context = {}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orders_count = orders.count()
    orders_delivered = Order.objects.filter(status="Delivered").count()
    orders_pending = Order.objects.filter(status="Pending").count()
    context = {'customers': customers, 'orders':orders, 'orders_count': orders_count,'orders_delivered': orders_delivered, 'orders_pending':orders_pending }

    return render(request, 'accounts/index.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def UserPage(request):
    orders = request.user.customer.orders.all()

    orders_count = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    
    # print('ORDERS',orders)
    context = {'orders': orders, 'orders_count': orders_count,'orders_delivered': orders_delivered, 'orders_pending':orders_pending}
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/accounts_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    for product in products:
        product.price = math.ceil(product.price)

    context = {'products':products}
    return render(request, 'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_details(request,pk):
    prod = Product.objects.get(id=pk)
    prod_orders_count = Order.objects.filter(product=prod).values('customer').distinct().count()

    orders_count = Order.objects.filter(product=prod).count()
    orders_prod = Order.objects.filter(product=prod)

    orders_delivered = Order.objects.filter(product=prod, status="Delivered").count()
    orders_pending = Order.objects.filter(product=prod, status="Pending").count()
    orders_out_of_delivered = Order.objects.filter(product=prod, status="Out of Deliver").count()


    context = {'orders_count':orders_count, 'orders_delivered':orders_delivered,'orders_pending':orders_pending,
               'prod_orders_count': prod_orders_count, 'orders_prod': orders_prod,'orders_out_of_delivered':orders_out_of_delivered,'prod':prod}
    return render(request, 'accounts/product_details.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.orders.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders':orders , 'orders_count': orders_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer,Order, fields=('product', 'status'), extra=5)

    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        # print('Printing Post:',request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset , 'customer': customer}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing Post:',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html',context)

