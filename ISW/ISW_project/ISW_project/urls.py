"""
URL configuration for ISW_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from polls import views

app_name = "polls"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.UserLoginView.as_view(), name='login'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('home/', login_required(views.lista_prodotti), name='home'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('', views.lista_prodotti, name="lista_prodotti"),
    path('carrello/', views.carrello, name="carrello"),
    path('aggiungi_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('get/', views.CheckoutView.as_view(), name="get"),
    path('post/', views.CheckoutView.as_view(), name="post"),
    path('remove_product/<int:id>/', views.remove_product, name="remove_product"),
    path('increase_quantity/<int:id>/', views.increase_quantity, name="increase_quantity"),
    path('decrease_quantity/<int:id>/', views.decrease_quantity, name="decrease_quantity"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout")
]
