from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistroForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Pedido, Fidelizacion, Cupon
from decimal import Decimal
import random, string
from datetime import date, timedelta



def login_view(request):
    form = LoginForm(request.POST or None)
    message = ''
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard' if user.is_superuser else 'home')
        else:
            message = 'Usuario o contraseña incorrectos'

    return render(request, 'cuentas/login.html', {'form': form, 'message': message})


def logout_view(request):
    logout(request)
    return redirect('login')


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})


def is_admin(user):
    return user.is_superuser


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'cuentas/admin_dashboard.html')


def comidas_rapidas_view(request):
    return render(request, 'cuentas/comidas_rapidas.html')

def bebidas_view(request):
    return render(request, 'cuentas/bebidas.html')


@login_required
def procesar_pedido_view(request):
    if request.method == 'POST':
        try:
            total = Decimal(request.POST.get('total', '0'))
        except:
            messages.error(request, "Total inválido")
            return redirect('formulario')

        if total <= 0:
            messages.error(request, "Debes seleccionar al menos un producto.")
            return redirect('formulario')

        pedido = Pedido.objects.create(usuario=request.user, total=total)

        fidelizacion, _ = Fidelizacion.objects.get_or_create(usuario=request.user)
        fidelizacion.total_pedidos += 1
        fidelizacion.total_gastado += total
        fidelizacion.save()

        recompensa = fidelizacion.verificar_recompensa()
        if recompensa:
            messages.success(request, f"¡Felicidades! Has ganado: {recompensa}")
        else:
            messages.success(request, "Pedido registrado exitosamente.")

        return redirect('formulario')

    return render(request, 'cuentas/formulario.html')

def generar_codigo_cupon():
    return 'DESC-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def calcular_descuento_para_proxima_compra(total):
    if total >= 100000:
        return 20000
    elif total >= 60000:
        return 10000
    elif total >= 30000:
        return 5000
    return 0

def formulario_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('name')
        telefono = request.POST.get('phone')
        tipo_pedido = request.POST.get('orderType')
        direccion = request.POST.get('address') if tipo_pedido == 'delivery' else ''
        metodo_pago = request.POST.get('payment')
        comentarios = request.POST.get('comments')

        total_str = request.POST.get('total', '0').replace('.', '')
        try:
            total = Decimal(total_str)
        except:
            messages.error(request, "Total inválido.")
            return redirect('formulario')

        if total <= 0:
            messages.error(request, "Selecciona al menos un producto.")
            return redirect('formulario')

        # Calcular descuento y crear cupón
        descuento = calcular_descuento_para_proxima_compra(total)
        if descuento > 0:
            codigo = generar_codigo_cupon()
            expiracion = date.today() + timedelta(days=30)

            cupon = Cupon.objects.create(
                codigo=codigo,
                valor_descuento=descuento,
                cliente=nombre,
                expiracion=expiracion
            )

            mensaje = f"¡Pedido enviado exitosamente! Usa el cupón <strong>{codigo}</strong> y obtén ${descuento:,} de descuento en tu próxima compra. Válido hasta {expiracion.strftime('%d/%m/%Y')}."
        else:
            mensaje = "¡Pedido enviado exitosamente! No has generado cupón esta vez, ¡inténtalo con una compra mayor!"

        # Guardar pedido
        Pedido.objects.create(
            nombre=nombre,
            telefono=telefono,
            tipo_pedido=tipo_pedido,
            direccion=direccion,
            metodo_pago=metodo_pago,
            comentarios=comentarios,
            total=total
        )

        messages.success(request, mensaje)
        return redirect('formulario')

    return render(request, 'formulario.html')
