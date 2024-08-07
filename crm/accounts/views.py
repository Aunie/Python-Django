from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for :' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orders_count = orders.count()
    orders_delivered = Order.objects.filter(status="Delivered").count()
    orders_pending = Order.objects.filter(status="Pending").count()
    context = {'customers': customers, 'orders':orders, 'orders_count': orders_count,'orders_delivered': orders_delivered, 'orders_pending':orders_pending }

    return render(request, 'accounts/index.html', context)

@login_required(login_url='login')
def products(request):
    return render(request, 'accounts/products.html')

@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders':orders , 'orders_count': orders_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
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
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html',context)

