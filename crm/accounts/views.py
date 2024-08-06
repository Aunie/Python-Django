from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from .forms import OrderForm
# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    orders_count = orders.count()
    orders_delivered = Order.objects.filter(status="Delivered").count()
    orders_pending = Order.objects.filter(status="Pending").count()
    context = {'customers': customers, 'orders':orders, 'orders_count': orders_count,'orders_delivered': orders_delivered, 'orders_pending':orders_pending }

    return render(request, 'accounts/index.html', context)

def products(request):
    return render(request, 'accounts/products.html')

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()
    context = {'customer': customer, 'orders':orders , 'orders_count': orders_count}
    return render(request, 'accounts/customer.html', context)


def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        # print('Printing Post:',request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)

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

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html',context)
