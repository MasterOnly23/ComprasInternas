from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from usuarios.forms import EditArea
from usuarios.models import User
from tienda.forms import ContactForm, EditPedidoForm


from django.core.mail import send_mail, BadHeaderError
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.contrib import messages
from django.conf import settings

from tienda.models import Producto, Pedido,Orden , TiendaStockproducto, TiendaArticulos, TiendaProductos, ProductosDestacados, PedidoCancelado
from tienda.carrito import Carrito


from django.db.models import Q


from datetime import datetime, timedelta

#paginacion
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest


from django.contrib.sessions.models import Session

from tienda.context_processor import total_carrito
import json


#export excel
from django_excel import make_response_from_query_sets
# Create your views here.


#parseo legajo
def authLegajo(request):
    user = request.user
    if request.user.is_authenticated:
        return str(user.legajo)


#parseo area
def authArea(request):
    user = request.user
    if request.user.is_authenticated:
        return str(user.area)
    
def get_carrito(request):
    carrito_lista = request.COOKIES.get('carrito_compras')
    carrito = Carrito(request)
    if carrito_lista:
        carrito.cart = json.loads(carrito_lista)
    return carrito


def index(request):
    user = request.user
    userLegajo = authLegajo(request)
    userArea = authArea(request)
    queryset = request.GET.get("buscarProducto")
    pagina = request.GET.get("page", 1)
    productos = TiendaProductos.objects.order_by('-stockProducto')
    fecha_hoy = datetime.today().isoweekday()

    destacados = ProductosDestacados.objects.filter(user_id = user.id).order_by('-acumulador')[:6]
    destacados1 = destacados[0:2]
    destacados2 = destacados[2:4]
    destacados3 = destacados[4:6]
    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()
    
    #carrito
    carrito = get_carrito(request)
    

    try:
        paginator = Paginator(productos, 9)
        productos = paginator.page(pagina)
    except:
        raise Http404

    if queryset:

            articulo = TiendaProductos.objects.filter(descProducto__icontains=queryset)
            return render(request, 'productos.html', {"articulo":articulo, 'paginator':paginator, 'legajo':userLegajo, 'is_staff':is_staff, 'destacados':destacados, 'destacados1':destacados1, 'destacados2':destacados2, 'destacados3':destacados3})
    return render(request, 'productos.html', {'user':user, 'productos':productos, "fecha_hoy":fecha_hoy, 'paginator':paginator, 'legajo':userLegajo,'is_staff':is_staff, 'area':userArea, 'destacados':destacados, 'destacados1':destacados1, 'destacados2':destacados2, 'destacados3':destacados3, 'carrito':carrito})




def agregar_producto(request, producto_id):
    carrito = get_carrito(request)
    producto = TiendaProductos.objects.get(id=producto_id)
    if producto.categoria == 'Farmacia':
        carrito.agregar_prod_farmacia(producto)
    else:
        carrito.agregar_prod_accesorios(producto)
    response = redirect("index")
    response.set_cookie('carrito_compras', json.dumps(carrito.cart))
    return response

def elminar_producto(request, producto_id):
    carrito = get_carrito(request)
    producto = TiendaProductos.objects.get(id=producto_id)
    carrito.eliminar(producto)
    response = redirect("index")
    response.set_cookie('carrito_compras', json.dumps(carrito.cart))
    return response

def restar_producto(request, producto_id):
    carrito = get_carrito(request)
    producto = TiendaProductos.objects.get(id=producto_id)
    if producto.categoria == 'Farmacia':
        carrito.restarFarmacia(producto)
    else:
        carrito.restarAccesorios(producto)
    response = redirect("index")
    response.set_cookie('carrito_compras', json.dumps(carrito.cart))
    return response

def limpiar_carrito(request):
    response = redirect("index")
    response.delete_cookie('carrito_compras')
    return response

# def carrito(request):
#     user = request.user
#     productos = TiendaProductos.objects.all()
#     return render(request, 'carrito.html', {'user':user, 'productos':productos})

def creoDestacado(cantidad, productoId, userId):
    
    try:
        prod2 = ProductosDestacados.objects.filter(user_id = userId).exists()
        if prod2:
            try:
                if productoId is not None:
                    prodUser = ProductosDestacados.objects.filter(user_id = userId).all()
                    try:
                        if ProductosDestacados.objects.filter(producto_id=productoId, user_id=userId).exists():
                                print('soy el if')
                                acumuloadorBase = ProductosDestacados.objects.get(producto_id = productoId,
                                                                                                user_id = userId).acumulador
                                            
                                            

                                productoDestacado = ProductosDestacados.objects.get(producto_id = productoId,
                                                                                    user_id = userId,
                                                                                    )
                                productoDestacado.acumulador = acumuloadorBase + cantidad
                                productoDestacado.save()
                        else:
                                print('soy el else')
                                prodDestNew = ProductosDestacados(producto_id = productoId, user_id = userId,
                                                                            acumulador = cantidad )
                                prodDestNew.save()

                    except:
                        logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
                        logErrorFile = 'log_error/keyslogDestacado_{}.txt'.format(logFecha)
                        with open (logErrorFile, 'a') as log_file:
                            log_file.write('Error produtoDestacado, confirmacion de existencia de usuario y producto')
                        return redirect("index")


            except:
                logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
                logErrorFile = 'log_error/keyslogDestacado_{}.txt'.format(logFecha)
                with open (logErrorFile, 'a') as log_file:
                    log_file.write('Error produtoDestacado, productoId is None')
                return redirect("index")
        else:
            print('soy el else de usuario')
            prod3 = ProductosDestacados(user_id = userId, producto_id = productoId, acumulador = cantidad)
            prod3.save()

    except:
        logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        logErrorFile = 'log_error/keyslogDestacado_{}.txt'.format(logFecha)
        with open (logErrorFile, 'a') as log_file:
            log_file.write('Error produtoDestacado, prod2')
        return redirect("index")
        


@login_required
def pedido_mail(request):
    carrito = Carrito(request)
    user = request.user
    productos = TiendaProductos.objects.all()
    fecha_hoy = datetime.today().isoweekday()
    print(request.COOKIES.get("carrito_compras"))
    articulos_json = request.COOKIES.get("carrito_compras")
    articulos = json.loads(articulos_json or '{}')
    productosCarrito = articulos.items()
    print(articulos)
    userLegajo = authLegajo(request)
    nombreApellido = f'{user.first_name} {user.last_name}'
    totalCarrito = total_carrito(request)

    try:
        if not articulos == {}:
            orden = Orden(usuario = nombreApellido,
                                legajo = userLegajo,
                                totalCarrito = totalCarrito['total_carrito'],
                                user = user,
                                )
            orden.save()
            print(orden.id)

            for key, value in productosCarrito:
                    pedir = Pedido(producto_id = value['producto_id'],
                    codProducto = TiendaProductos.objects.get(id=value['producto_id']).codProducto,
                    nombre = value['nombre'],
                    precio = value['precio'],
                    acumulado = value['acumulado'],
                    cantidad = value['cantidad'], 
                    nroPedido_id = orden.id
                    )


                    creoDestacado(value['cantidad'], value['producto_id'], user.id)
                    pedir.save()
                
            total = 0

        else:
            total = 0
    except:
        logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        logErrorFile = 'tienda/log_error/keyslog_{}.txt'.format(logFecha)
        with open (logErrorFile, 'a') as log_file:
            log_file.write('Error al crear el pedido')

        messages.error(request, "Ha ocurrido un Error al crear el pedido, vuelva a intentarlo o comuniquese con el admin")
        return limpiar_carrito(request)
    try:

        for key, value in articulos.items():
            total += float(value["acumulado"])
    except:
        logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        logErrorFile = 'tienda/log_error/keyslog_{}.txt'.format(logFecha)
        with open (logErrorFile, 'a') as log_file:
            log_file.write('Error en el valor total del carrito')

        messages.error(request, "Ha ocurrido un Error con el total")
        return limpiar_carrito(request)
        
        
    subject = "Pedido Compras Internas"
    html_message = render_to_string('pedido.html', {'user':user, 'productos':productos, 'productosCarrito':productosCarrito, 'totalCarrito':total})
    plain_message = render_to_string('pedido.html', {'user':user, 'productos':productos, 'productosCarrito':productosCarrito, 'totalCarrito':total})

    from_email = user.email
    abastecimiento = 'abastecimiento@farmaciasdrahorro.com.ar'
    drogueria =  'drogueria@farmaciasdrahorro.com.ar'
    if not articulos == {}:
        try:
            send_mail(subject, plain_message, from_email, ['pruebacomprasinternas@gmail.com', user.email], html_message=html_message)
            messages.success(request, "Pedido realizado correctamente")

            return limpiar_carrito(request)
        except :
            logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            logErrorFile = 'tienda/log_error/keyslog_{}.txt'.format(logFecha)
            with open (logErrorFile, 'a') as log_file:
                log_file.write("Error con el envio del mail")

            messages.error(request, "Tu pedido se ha realizado pero ha ocurrido un Error con el envio del mail")
            return limpiar_carrito(request)
    else:
        messages.error(request, "El carrito esta vacio, asegurese de cargar los articulos")
        
        return limpiar_carrito(request)

def buscarProducto(request, nombreProd):
        #comprobar permisos
        is_staff = request.user.groups.filter(name='Staff').exists()

        fecha_hoy = datetime.today().isoweekday()
        queryset = request.GET.get("buscarProducto")
        #carrito
        carrito = get_carrito(request)
        try:
            if queryset:

                articulo = TiendaProductos.objects.filter(
                    Q(descProducto__icontains = queryset) |
                    Q(producto__icontains = queryset)
                    # Q(numero__icontains= queryset)
                ).order_by('-stockProducto').distinct()

                
                return render(request, 'buscar.html', {"articulo":articulo, "fecha_hoy":fecha_hoy, 'is_staff':is_staff, 'carrito':carrito})
            else:
                return render(request, 'buscar.html', {"busqueda":queryset, "msg":'No data', "fecha_hoy":fecha_hoy, 'is_staff':is_staff, 'carrito':carrito})
        except:
            return render(request, 'buscar.html', {"msg":'No data', "fecha_hoy":fecha_hoy, 'is_staff':is_staff, 'carrito':carrito})



def buscarCategoria(request, categoria):
        #comprobar permisos
        is_staff = request.user.groups.filter(name='Staff').exists()

        fecha_hoy = datetime.today().isoweekday()
        pagina = request.GET.get("page", 1)
        #carrito
        carrito = get_carrito(request)
        
        if categoria:

            productosCategoria = TiendaProductos.objects.filter(
                Q(categoria__icontains = categoria) #|
                # Q(numero__icontains= queryset)
            ).distinct()

            try:
                paginator = Paginator(productosCategoria, 9)
                productosCategoria = paginator.page(pagina)
            except:
                raise Http404

            return render(request, 'categorias/categorias.html', {"productosCategoria":productosCategoria, 'paginator':paginator, "fecha_hoy":fecha_hoy, 'is_staff':is_staff, 'carrito':carrito})
        else:
            return render(request, 'categorias/categorias.html', {"busqueda":categoria, "msg":'No data', "fecha_hoy":fecha_hoy, 'is_staff':is_staff, 'carrito':carrito})





@login_required
def perfil(request):
    #comprobar permisos
    is_staff = request.user.groups.filter(name='Staff').exists()

    return render(request, 'perfil.html', {'is_staff':is_staff})


def contact_form(request):
    user = request.user
    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()
    return render(request, 'contacto.html', {'user':user, 'is_staff':is_staff})


@login_required
def misPedidos(request):
    user = request.user
    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()
    ordenes = Orden.objects.filter(user_id=user.id).order_by('-fecha_creacion')
    pagina = request.GET.get("page", 1)
    pedidosLista = list(ordenes)
    print(pedidosLista)
    if len(pedidosLista) == 0:
        msg = 'Aun no tienes nigun pedido'
        return render(request, 'mis_pedidos.html', {'ordenes':ordenes,'is_staff':is_staff, 'msg':msg})
    else:
        try:
            paginator = Paginator(ordenes, 15)
            ordenes = paginator.page(pagina)
        except:
            raise Http404
        return render(request, 'mis_pedidos.html', {'ordenes':ordenes,'is_staff':is_staff, 'paginator':paginator})


@login_required
def cancelarPedido(request, id_orden):
    user = request.user
    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()
    orden = Orden.objects.get(pk=id_orden)
    pedidos = Pedido.objects.filter(nroPedido_id=id_orden)


    subject = "Pedido Compras Internas"
    html_message = render_to_string('pedidocancelado.html', {'user':user, 'orden':orden,})
    plain_message = render_to_string('pedidocancelado.html', {'user':user, 'orden':orden,})
    from_email = user.email 
    abastecimiento = 'abastecimiento@farmaciasdrahorro.com.ar'
    drogueria =  'drogueria@farmaciasdrahorro.com.ar'
    try:
            orden.estado = 'Cancelado'
            orden.save()
            for pedido in pedidos:
                pedidoCancelado = PedidoCancelado()
                pedidoCancelado.nroPedido = pedido.nroPedido
                pedidoCancelado.producto_id = pedido.producto_id
                pedidoCancelado.codProducto = pedido.codProducto
                pedidoCancelado.nombre = pedido.nombre
                pedidoCancelado.precio = pedido.precio
                pedidoCancelado.acumulado = pedido.acumulado
                pedidoCancelado.cantidad = pedido.cantidad
                pedidoCancelado.save()
            pedidos.delete()
            send_mail(subject, plain_message, from_email, ['pruebacomprasinternas@gmail.com', user.email], html_message=html_message)
            messages.success(request, "Pedido cancelado correctamente")
            return misPedidos(request)
    except BadHeaderError:
            logFecha = datetime.now().strftime('%y-%m-%d_%H-%M-%S')
            logErrorFile = 'tienda/log_error/keyslog_{}.txt'.format(logFecha)
            with open (logErrorFile, 'a') as log_file:
                log_file.write("Error al cancelar pedido")
            messages.error(request, "Ha ocurrido un Error con la cancelacion del pedido")
            return redirect("index")

        


    



@login_required
def filtroEstado(request, estado):
        user = request.user
        #comprobar permisos
        is_staff = user.groups.filter(name='Staff').exists()
        if estado == 'Entregado':
            pedidos = Pedido.objects.filter(estado=estado,
                                            user_id=user.id)

            return render(request, 'mis_pedidos.html', {'pedidos':pedidos,'is_staff':is_staff})
        


        elif estado == 'Pendiente':
            pedidos = Pedido.objects.filter(estado=estado,
                                            user_id=user.id)

            return render(request, 'mis_pedidos.html', {'pedidos':pedidos,'is_staff':is_staff})
        
        elif estado == 'Cancelado':
            pedidos = Pedido.objects.filter(estado=estado,
                                            user_id=user.id)

            return render(request, 'mis_pedidos.html', {'pedidos':pedidos,'is_staff':is_staff})
        


def pedidosOrden(request, nro_orden):
    user = request.user
    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()

    pedidos = Pedido.objects.filter(nroPedido_id=nro_orden)
    pagina = request.GET.get("page", 1)
    try:
        paginator = Paginator(pedidos, 10)
        pedidos = paginator.page(pagina)
    except:
        raise Http404
    return render(request, 'pedidosProductos.html', {'pedidos':pedidos,'is_staff':is_staff, 'paginator':paginator})







# @login_required
# def contact_form(request):
#     user = request.user
#     mail = [user.email]
#     if request.method == "GET":
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data["subject"]
#             from_email = form.cleaned_data["from_email"]
#             message = form.cleaned_data['message']
#             archivos = form.cleaned_data['archivos']
#             try:
#                 send_mail(subject, message, from_email, ['jfdaza@farmaciasdrahorro.com.ar'])
#             except BadHeaderError:
#                 return HttpResponse("Invalid header found.")
#             messages.success(request, "Mensaje enviado correctamente")
#             return render(request, 'productos.html')
#     return render(request, "contacto.html", {"form": form})




#-----------------------------------------------------------------------------------------------------------

# ADMINISTRADOR

class AdministradorView(HttpRequest):

    @login_required
    def listaPedidos(request):
        user = request.user
        #comprobar permisos
        is_staff = user.groups.filter(name='Staff').exists()
        pedidos = Pedido.objects.all()
        users = User.objects.all()

        return render(request, 'lista_pedidos.html', {'pedidos':pedidos, 'users':users,'is_staff':is_staff})


    def editarPedido(request, id_pedido):
        
        pedido = Pedido.objects.filter(id = id_pedido).first()

        form = EditPedidoForm(instance=pedido)
        # messages.success(request, "Los datos se modificaron correctamente")
        return render(request, 'administrador/editar_pedido.html', {'form':form, 'pedido':pedido})

    def actualizarPedido(request, id_pedido):

        pedido = Pedido.objects.get(pk=id_pedido)
        form = EditPedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos se modificaron correctamente")
            return redirect(AdministradorView.listaPedidos)
        else:
            return Http404
        

    def eliminar_pedido(request, id_pedido):
        
        pedido = Pedido.objects.get(pk=id_pedido)
        pedido.delete()
        messages.success(request, "Los datos se eliminaron correctamente")
        pedidos = Pedido.objects.all()


        return render(request, 'administrador/lista_pedidos.html', {'pedidos':pedidos})
    

    def filtroUsuario(request, id_user, rango=None):
        pedidos = Pedido.objects.filter(user_id=id_user)
        users = User.objects.all()
        

        return render(request, 'administrador/lista_pedidos_users.html', {'pedidos':pedidos, 'users':users})

    @login_required
    def filtroFecha(request, rango):
        user = request.user
        #comprobar permisos
        is_staff = user.groups.filter(name='Staff').exists()
        if rango == 'hoy':
            print("hoy")
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            print(fecha_hoy)
            ordenes = Orden.objects.filter(fecha_creacion=fecha_hoy,
                                            user_id=user.id)

            rango_actual = 'hoy'

            return render(request, 'mis_pedidos.html', {'ordenes':ordenes,'is_staff':is_staff})
        


        elif rango == 'semana':
            users = User.objects.all()
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
            fecha_semana = fecha_hoy - timedelta(days=7)
            fecha_mes_pasado = datetime.strptime(datetime.today().strftime('%Y-%m')+'-01', '%Y-%m-%d')
            ordenes = Orden.objects.filter(fecha_creacion__gte=datetime.date(fecha_semana),
                                            fecha_creacion__lte=datetime.date(fecha_hoy),
                                            user_id=user.id)


            return render(request, 'mis_pedidos.html', {'ordenes':ordenes, 'users':users,'is_staff':is_staff})


        elif rango == 'mes':
            users = User.objects.all()
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
            # fecha_mes_pasado = fecha_hoy - timedelta(days=30)
            fecha_mes_pasado = datetime.strptime(datetime.today().strftime('%Y-%m')+'-01', '%Y-%m-%d')
            print(fecha_mes_pasado)
            ordenes = Orden.objects.filter(fecha_creacion__gte=datetime.date(fecha_mes_pasado),
                                            fecha_creacion__lte=datetime.date(fecha_hoy),
                                            user_id=user.id)

            rango_actual = 'mes'

            return render(request, 'mis_pedidos.html', {'ordenes':ordenes, 'users':users, 'rango_actual':rango_actual,'is_staff':is_staff})


        elif rango == 'año':
            users = User.objects.all()
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
            fecha_semana = fecha_hoy - timedelta(days=7)
            fecha_año = datetime.strptime(datetime.today().strftime('%Y')+'-01-01', '%Y-%m-%d')
            ordenes = Orden.objects.filter(fecha_creacion__gte=datetime.date(fecha_año),
                                            fecha_creacion__lte=datetime.date(fecha_hoy),
                                            user_id=user.id)


            return render(request, 'mis_pedidos.html', {'ordenes':ordenes, 'users':users,'is_staff':is_staff})


        else:
            ordenes = Orden.objects.all()
            return render(request, 'mis_pedidos.html', {'ordenes':ordenes, 'users':users,'is_staff':is_staff})



        # elif rango == 'mes' and id_user == None:
        #         users = User.objects.all()
        #         fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        #         fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
        #         fecha_mes_pasado = datetime.strptime(datetime.today().strftime('%Y-%m')+'-01', '%Y-%m-%d')
        #         print(fecha_mes_pasado)
        #         pedidos = Pedido.objects.filter(fecha_creacion__gte=datetime.date(fecha_mes_pasado),
        #                                         fecha_creacion__lte=datetime.date(fecha_hoy))

        #         rango_actual = 'mes'
        #         print(rango_actual)

        #         return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users, 'rango_actual':rango_actual})


        
        
        
        
    def filtroUsuarioFecha(request, id_user, rango):
        if rango == 'hoy':
            users = User.objects.all()
            print("hoy")
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            print(fecha_hoy)
            pedidos = Pedido.objects.filter(fecha_creacion=fecha_hoy,
                                                user_id=id_user)

            return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})

        elif rango == 'mes' and id_user != None:
            users = User.objects.all()
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
            # fecha_mes_pasado = fecha_hoy - timedelta(days=30)
            fecha_mes_pasado = datetime.strptime(datetime.today().strftime('%Y-%m')+'-01', '%Y-%m-%d')
            print('mes usu-fecha')
            pedidos = Pedido.objects.filter(fecha_creacion__gte=datetime.date(fecha_mes_pasado),
                                            fecha_creacion__lte=datetime.date(fecha_hoy),
                                            user_id=id_user)

            return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})




    def filtroFechaUsuario(request, id_user, rango):
        if rango == 'hoy':
            users = User.objects.all()
            print("hoy")
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            print(fecha_hoy)
            pedidos = Pedido.objects.filter(fecha_creacion=fecha_hoy,
                                                user_id=id_user)

            return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})

        elif rango == 'mes' and id_user != None:
            users = User.objects.all()
            fecha_hoy = datetime.today().strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
            # fecha_mes_pasado = fecha_hoy - timedelta(days=30)
            fecha_mes_pasado = datetime.strptime(datetime.today().strftime('%Y-%m')+'-01', '%Y-%m-%d')
            print('mes usu-fecha')
            pedidos = Pedido.objects.filter(fecha_creacion__gte=datetime.date(fecha_mes_pasado),
                                            fecha_creacion__lte=datetime.date(fecha_hoy),
                                            user_id=id_user)

            return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})









        # pedidos = Pedido.objects.filter(user_id=id_user)
        # users = User.objects.all()
            

        # return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})




    # def filtroFechaHoy(request, id_user=None):
    #         users = User.objects.all()
    #         print("hoy")
    #         fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    #         print(fecha_hoy)
    #         pedidos = Pedido.objects.filter(fecha_creacion__range=fecha_hoy)

    #         return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})
    
    
    # def filtroFechaMes(request,id_user=None):
    #         users = User.objects.all()
    #         fecha_hoy = datetime.today().strftime('%Y-%m-%d')
    #         fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d')
    #         fecha_mes_pasado = fecha_hoy - timedelta(days=30)
    #         pedidos = Pedido.objects.filter(fecha_creacion__gte=datetime.date(fecha_mes_pasado),
    #                                         fecha_creacion__lte=datetime.date(fecha_hoy))

    #         return render(request, 'administrador/lista_pedidos_fecha.html', {'pedidos':pedidos, 'users':users})

