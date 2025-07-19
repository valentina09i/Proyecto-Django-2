from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cuentas.urls')),  # incluye las URLs de la app cuentas
]