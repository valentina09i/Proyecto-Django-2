from django.urls import path
from .views import login_view, logout_view
from django.views.generic import TemplateView
from .views import registro_view
from .views import admin_dashboard
from .views import (
    login_view, logout_view, registro_view, admin_dashboard,
    comidas_rapidas_view, bebidas_view
)
from django.views.generic import TemplateView
from .views import procesar_pedido_view




urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', registro_view, name='registro'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('comidas_rapidas/', comidas_rapidas_view, name='comidas_rapidas'),
    path('bebidas/', bebidas_view, name='bebidas'),
    path('formulario/', procesar_pedido_view, name='formulario'),
    path('', TemplateView.as_view(template_name='cuentas/home.html'), name='home'),
    
]