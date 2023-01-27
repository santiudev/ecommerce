from django.urls import path
from .import views


urlpatterns=[
    path("",views.home,name="home"),
    path("register/",views.register,name="register"),
    path("login/",views.login_page,name="login"),
    path("logout/",views.logout_page,name="logout"),
    path("category/",views.collections,name="category"),
    path("categorys/<str:name>",views.collectionviews,name="category"),
    path("product_details/<str:cname>/<str:pname>",views.product_details,name="product_details"),
    path("addtocart/",views.add_to_cart,name="addtocart"),
    path("cart/",views.cart_page,name="cart"),
    path("cart_remove/<str:crid>",views.cart_remove,name="cart_remove"),
    path("addtofav/",views.add_to_fav,name="addtofav"),
    path("fav/",views.fav,name="fav"),
    path("fav_remove/<str:fid>",views.fav_remove,name="fav_remove"),
    path("cheackout/",views.cheack_out,name="cheackout"),
    path("placeorder/",views.place_order,name="placeorder"),
    
    path("my_orders/",views.my_orders,name="my_orders"),
    path("order_view/<str:tno>",views.order_view,name="order_view"),
    path("productlist/",views.productlist_ajax,name="productlist"),
    path("searchproduct",views.searchproduct,name="searchproduct"),
    path("change_password",views.PasswordChangeView.as_view(template_name='shop/pass_change.html'),name='change_password'),
    path("password_success",views.password_success,name="password_success"),
    

    
]
