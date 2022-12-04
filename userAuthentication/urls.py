from django.urls import path,include
from . import views

urlpatterns = [
    path("signIn",views.UserSignIN.as_view(),name="sign_In_ULR"),
    path("signup",views.UserSignUp.as_view(),name="sign_Up_ULR"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    path("",include("userProjects.urls")),
    #404 triggeres
    path("<str:any>",views.Page404.as_view(),name="Page_404"),
    path("<int:any>",views.Page404.as_view(),name="Page_404"),
    
]
