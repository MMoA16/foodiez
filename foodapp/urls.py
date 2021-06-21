from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name="home"),
    path('registration/',register,name="registration"),
    path("login/",login_form,name="login"),
    path("cuisines/<int:taskid>/",cuisines,name="cuisines"),
    path("logout/",logoutuser,name="logout"),
    path("additems/<int:taskid>",additem,name="additem"),
    path("cart/",cart1,name="cart"),
    path("deleteitem/<int:taskid>",deleteitem,name="deleteitem"),
    path("addi/<int:taskid>",addi,name="addi"),
    path("orders/",order,name="orders"),
    # path("updatequantity/<int:taskid>/<int:tag>",update,name="updatequantity")
    path("place/",place1,name="place")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
