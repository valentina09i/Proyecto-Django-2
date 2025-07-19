from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from decimal import Decimal
from django.shortcuts import render, redirect

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, default='Pendiente')

class Fidelizacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    total_pedidos = models.PositiveIntegerField(default=0)
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    premios_canjeados = models.PositiveIntegerField(default=0)

    def verificar_recompensa(self):
        if self.total_pedidos % 5 == 0:
            return "Comida gratis"
        elif self.total_gastado >= 100:
            return "10% de descuento"
        return None
    
class Cupon(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    valor_descuento = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.CharField(max_length=100)  # opcional: puedes relacionarlo con un modelo Cliente
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - ${self.valor_descuento}"
