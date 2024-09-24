from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='app/index.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='app/logout.html'),name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    # path('',views.index,name='index'),
    path('home',views.home, name='home'),
    path('newregister',views.newregister,name='newregister'),
    path('register', views.register, name='regi'),
    path("otpverifyuser/<int:num>" ,views.otpverifyuser, name='otpverifyuser'),
    path('otpverify', views.verify67, name='otpverify'),
    path('newfeatch/',views.newfeatch,name='newfeatch'),
    path('featchsearch/',views.featchsearch,name='featchsearch'),
    path("featchpage/<int:pk>",views.featchpage,name='featchpage'),
    path("fetch",views.fetch,name='fetch'),
    path("custview/<int:pk>" , views.custview, name='custview'),
    path("relese1",views.relese1,name='relese1'),
    path("relese2/<int:im>",views.relese2,name='relese2'),
    path("intrestonly",views.sionly,name='intrestonly'),
    path("closefetch",views.closefetch,name='closefetch'),


    


]