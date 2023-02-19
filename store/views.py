from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
import datetime
# Create your views here.
import json




def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        items =[]  
        order = {'get_cart_total':0 , 'get_cart_items':0, 'shipping':False} 
        cartItems = order['get_cart_items']
        customer = {'name':'' , 'email':''}
    products = Product.objects.all()
    context = {
        'items':items,
        'order':order,
        'products':products,
        'cartItems':cartItems,
        'customer':customer,
    }

    return render(request ,'store/store.html',context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        items =[]   
        order = {'get_cart_total':0 , 'get_cart_items':0, 'shipping':False} 
        cartItems = order['get_cart_items']
        customer = {'name':'' , 'email':''}
    context = {
        'items':items,
        'order':order,
         'cartItems':cartItems,
         'customer':customer,
    }
    return render(request ,'store/cart.html',context)
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        items =[]   
        order = {'get_cart_total':0 , 'get_cart_items':0 , 'shipping':False}
        cartItems = order['get_cart_items'] 
        customer = {'name':'' , 'email':''}
        return redirect('../accounts/login/')
    context = {
        'items':items,
        'order':order,
         'cartItems':cartItems,
         'customer':customer,
    }
    return render(request ,'store/checkout.html',context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(f'product id = {productId}')
    print(f'Action = {action}')

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order , created = Order.objects.get_or_create(customer=customer,completed=False)
    orderItem , created = OrderItem.objects.get_or_create(order = order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove' :
        orderItem.quantity = (orderItem.quantity -1)    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
       
    return JsonResponse('Item was added', safe=False)




def processOrder(request):
    transaction_id= datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,completed=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.completed = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )    
    else:
        print("User is not logged in ...")    
    return JsonResponse('Payment complete',safe=False)




def product_detail(request,pk):
    products = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer,completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        items =[]   
        order = {'get_cart_total':0 , 'get_cart_items':0 , 'shipping':False}
        cartItems = order['get_cart_items'] 
        customer = {'name':'' , 'email':''}
        return redirect('../accounts/login/')
    context = {
        'items':items,
        'order':order,
         'cartItems':cartItems,
         'customer':customer,
         'products':products,
    }
    return render (request,'store/product_detail.html',context)