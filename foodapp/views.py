from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import User
import datetime
global number
def index(request):
	it=items.objects.all()
	rest=restaurant.objects.all()
	number=0
	if request.user.is_authenticated:
		u=userdata.objects.get(user=request.user)
		number=cart.objects.filter(user_name=u).count()
	return render(request,"index.html",{"items":it,"resto":rest,"num":number})

def register(request):
	form = NewUserForm()
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			userdata(user=User.objects.get(username=username)).save()
			login(request, user)
			messages.success(request, 'Account was successful created and has been logged in')
			return redirect('home')
	context = {'form':form}
	return render(request, 'register.html', context)

def login_form(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("home")
		else:
			return render(request, 'login.html', {'error_message': 'Incorrect username and/or password.'})
	else:
		return render(request,"login.html")

def cuisines(request,taskid):
	it=items.objects.filter(rest__id=taskid)
	img=restaurant.objects.get(id=taskid)
	number=0
	if request.user.is_authenticated:
		u=userdata.objects.get(user=request.user)
		number=cart.objects.filter(user_name=u).count()
	return render(request,"cuisines.html",{"items":it,"img":img,"num":number,"name":it[0].rest})

@login_required(login_url='login')
def logoutuser(request):
	logout(request)
	return redirect("home")

@login_required(login_url='login')
def additem(request,taskid):
	u=userdata.objects.get(user=request.user)
	if cart.objects.filter(item__id=taskid,user_name=u).exists():
		ca=cart.objects.get(item__id=taskid,user_name=u)
		ca.quantity+=1
		ca.price=ca.item.item_price*ca.quantity
		ca.time=ca.quantity*ca.item.duration
		ca.save()
	else :
		if cart.objects.filter(user_name=u).exists():
			g=cart.objects.filter(user_name=u)[0]
			iu=items.objects.get(id=taskid)
			if g.item.rest.id==iu.rest.id:
				cart(user_name=u,item=iu,quantity=1,price=iu.item_price,time=iu.duration).save()
			else:
				messages.add_message(request,messages.INFO,"You can order from only one restaurant")
				return redirect(request.META['HTTP_REFERER']) 
		else:
			it=items.objects.get(id=taskid)
			cart(user_name=u,item=it,quantity=1,price=it.item_price,time=it.duration).save()
	return redirect(request.META['HTTP_REFERER']) 

@login_required(login_url='login')
def cart1(request):
	loca=[]
	number=0
	user2=userdata.objects.get(user=request.user)
	ca=cart.objects.filter(user_name=user2)
	size=len(ca)
	if size!=0:
		loca=locality.objects.get(rest__id=ca[0].item.rest.id)
		number=cart.objects.filter(user_name=user2).count()
	total=int(0)
	time=int(0)
	for i in ca:
		time+=i.time
		total+=i.price
	context={"items":ca,"total":total,"time":time,"size":size,"loca":loca,"num":number}
	return render(request,"cart.html",context)

@login_required(login_url='login')
def deleteitem(request,taskid):
	ca=cart.objects.get(id=taskid)
	if(ca.quantity==0):
		ca.delete()
		ca.save()
	else:
		ca.quantity=ca.quantity-1
		ca.save()
	number=0
	if request.user.is_authenticated:
		u=userdata.objects.get(user=request.user)
		number=cart.objects.filter(user_name=u).count()
	return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def addi(request,taskid):
	ca=cart.objects.get(id=taskid)
	ca.quantity=ca.quantity+1
	ca.save()
	number=0
	if request.user.is_authenticated:
		u=userdata.objects.get(user=request.user)
		number=cart.objects.filter(user_name=u).count()
	return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def place1(request):
	user1=userdata.objects.get(user=request.user)
	menus = [" x ".join([z.item.name,str(z.quantity)]) for z in cart.objects.filter(user_name = user1)]
	local=request.POST['local']
	cart1=cart.objects.filter(user_name=user1)
	total=int(0)
	for i in cart1:
		total+=i.price
	orders(user=user1,items="\n".join(menus),rest=cart1[0].item.rest,total=total,local=local).save()
	cart1.delete()
	messages.add_message(request,messages.INFO,"Order has been successfully placed")
	return redirect("home")

@login_required(login_url='login')
def order(request):
	number=0
	user1=userdata.objects.get(user=request.user)
	obj=orders.objects.filter(user=user1)
	number=cart.objects.filter(user_name=user1).count()
	return render(request,"order.html",{"orders":obj,"num":number})