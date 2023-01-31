from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from shop.form import CustomUserForm,PasswordChangingForm
from django.contrib.auth import authenticate,login,logout
import json
import random
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.conf import settings
#Home Page



def home(request):
    products=Product.objects.filter(trending=1)
    context={'products':products}
    return render(request,"shop/index.html",context)


#Login

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")

    else:
    
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Sesion Iniciada")
                return redirect("/")
            else:
                messages.error(request,"Contraseña o Usuario incorrecto")
                return redirect('/login')
        return render(request,"shop/login.html")


#LogOut



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Sesión finalizada con exito")
        return redirect("/")


#Register



def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registrado con exito, ya puedes iniciar sesión....!")
            return redirect('/login')
    context={'form':form}
    return render(request,"shop/register.html",context)


#Collections



def collections(request):
    category=Category.objects.filter(status=0)
    context={'category':category}
    return render(request,"shop/collections.html",context)


#Collection View



def collectionviews(request,name):
    if(Category.objects.filter(status=0,name=name)):
        products=Product.objects.filter(category__name=name)
        context={'products':products,'category_name':name}
        return render(request,"shop/products/index.html",context)
    else:
        messages.warning(request,'No se encontro la categoria')
        return redirect('collections')


#Product Details



def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            context={'products':products}
            return render(request,"shop/products/product_details.html",context)
        else:
            messages.error(request,'No se encontro el producto')
            return redirect('collections')
    else:
        messages.error(request,'No se encontro la categoria')
        return redirect('collections')


#Add To Cart



def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                     return JsonResponse({'status':'Producto en el carrito '}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Producto agregado al carrito'}, status=200)
                    else:
                         return JsonResponse({'status':'Sin stock'}, status=200)
        else:
            return JsonResponse({'status':'Inicia sesión para añadir al carrito'}, status=200)
    else:
        return JsonResponse({'status':'Acceso invalido'},status=200)


#View Cartpage



def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        context={"cart":cart}
        return render(request,"shop/cart.html",context)
    else:
        return redirect("/")


#Remove Cart Items



def cart_remove(request,crid):
    cart_item=Cart.objects.get(id=crid)
    cart_item.delete()
    return redirect("/cart/")



#Add To Favorite



def add_to_fav(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                 if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                     return JsonResponse({'status':'Producto en favoritos '}, status=200)
                 else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Producto agregado a favoritos'}, status=200)
          

        else:
            return JsonResponse({'status':'Inicia sesión para añadir a favoritos'}, status=200)
    else:
        return JsonResponse({'status':'Acceso invalido'},status=200)


#View Favorite



def fav(request):
     if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        context={"fav":fav}
        return render(request,"shop/fav.html",context)
     else:
        return redirect("/")


#Remove Favorite


def fav_remove(request,fid):
    fav_item=Favourite.objects.get(id=fid)
    fav_item.delete()
    return redirect("/fav")


#CheackOut Page



def cheack_out(request):
    rowcart=Cart.objects.filter(user=request.user)
    for item in rowcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems=Cart.objects.filter(user=request.user)
    totel_price=0
    for item in cartitems:
        totel_price=totel_price+item.product.selling_price*item.product_qty
    
    userprofile=Profile.objects.filter(user=request.user.id).first()
 
    context={"cartitems":cartitems,"totel_price":totel_price,"userprofile":userprofile}
    return render(request,"shop/cheackout.html",context)



#Place Order

    
def place_order(request):


    currentuser = User.objects.filter(id=request.user.id).first()

    if not currentuser.first_name:
        currentuser.first_name=request.POST.get('fname')
        currentuser.last_name=request.POST.get('lname')
        currentuser.save()

    if not Profile.objects.filter(user=request.user):
        userprofile = Profile()
        userprofile.user = request.user
        userprofile.phone=request.POST.get('phone')
        userprofile.address=request.POST.get('address')
        userprofile.city=request.POST.get('city')
        userprofile.state=request.POST.get('state')
        userprofile.country=request.POST.get('country')
        userprofile.pincode=request.POST.get('pincode')
        userprofile.save()

    if request.user.is_authenticated:
        if request.method == 'POST':
            neworder=Order()
            neworder.user=request.user
            neworder.firstname=request.POST.get('fname')
            neworder.lastname=request.POST.get('lname')
            neworder.email=request.POST.get('email')
            neworder.phone=request.POST.get('phone')
            neworder.address=request.POST.get('address')
            neworder.city=request.POST.get('city')
            neworder.state=request.POST.get('state')
            neworder.country=request.POST.get('country')
            neworder.pincode=request.POST.get('pincode')


            neworder.payment_mode=request.POST.get('payment_mode')
            neworder.payment_id=request.POST.get('payment_id')

            


            

            cart=Cart.objects.filter(user=request.user)
            cart_totel_price=0

            for item in cart:
                cart_totel_price = cart_totel_price + item.product.selling_price * item.product_qty

            neworder.totel_price=cart_totel_price

            trackno=random.randint(1111111,9999999)
            while Order.objects.filter(tracking_no=trackno) is None:
                 trackno=random.randint(1111111,9999999)


            neworder.tracking_no=trackno
            neworder.save()


            neworderitems=Cart.objects.filter(user=request.user)
            for item in neworderitems:
                Orderitem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.product.selling_price,
                    quentity=item.product_qty,
                )


                #to decrese product in product quantity

                orderproduct = Product.objects.filter(id=item.product_id).first()
                orderproduct.quantity = orderproduct.quantity - item.product_qty
                orderproduct.save()


                #to clear user cart

                Cart.objects.filter(user=request.user).delete()


                messages.success(request, "Su pedido ha sido realizado con exito")
                

            return redirect("/")
    
        else:
            return redirect("/")
    else:
        return redirect("/")


#Payment (Pending)


#My Orderspage



def my_orders(request):
    orders=Order.objects.filter(user=request.user)
    context={"orders":orders}
    return render(request,"shop/orders.html",context)


# View Order Page



def order_view(request,tno):
    order=Order.objects.filter(tracking_no=tno).filter(user=request.user).first()
    orderitems=Orderitem.objects.filter(order=order)
    context={"order":order,"orderitems":orderitems}
    return render(request,"shop/orderview.html",context)


# View Orderdetails



def productlist_ajax(request):
    products=Product.objects.filter(status=0).values_list('name',flat=True)
    productslist=list(products)
    return JsonResponse(productslist,safe=False)



#Search Product



def searchproduct(request):
    if request.method == 'POST':
        searchedterm=request.POST.get('productsearch')
        if searchedterm == " ":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=Product.objects.filter(name__contains=searchedterm).first()
            if product:
                return redirect("product_details/"+ product.category.name+'/'+product.name)
            else:
                messages.info(request,"No se encontraron coincidencias con su busqueda")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
         return redirect(request.META.get('HTTP_REFERER'))



#Password Changing



class PasswordChangeView(PasswordChangeView):
    form_class=PasswordChangingForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request,'shop/pass_change_success.html')








    






    
