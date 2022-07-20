from django.db import models
from django.contrib.auth.models import *
class Actividad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=100,null=True, blank=True)
    controlador = models.CharField(max_length=100,null=True, blank=True)
    accion = models.CharField(max_length=100,null=True, blank=True)
    actividad_padre_id = models.IntegerField(null=True, blank=True)
    orden = models.IntegerField(null=True, blank=True)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class TipoUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class ClientePortal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class Permiso(models.Model):
    id = models.AutoField(primary_key=True)
    actividades = models.ForeignKey(Actividad, models.DO_NOTHING, null=True, blank=True, related_name='permiso_actividad')
    tiposussuarios = models.ForeignKey(TipoUsuario, models.DO_NOTHING, null=True, blank=True, related_name='permiso_actividad')
    visualizar = models.BooleanField(null=True, blank=True)
    editar = models.BooleanField(null=True, blank=True)
    importar = models.BooleanField(null=True, blank=True)
    exportar = models.BooleanField(null=True, blank=True)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

class Tienda(models.Model):
    id = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='tienda_clienteportal')

    def __str__(self):
        return f"{self.direccion}"

class UserManager(BaseUserManager):
  def _create_user(self, email, username, nombres, apellidos, password, dni, is_staff,
    is_superuser, **extra_fields):

    user = self.model(
      email=email,
        username=username,
      nombres=nombres,
      apellidos=apellidos,
      dni=dni,
      is_staff = is_staff,
      is_superuser = is_superuser,
      **extra_fields
    )
    user.set_password(password)
    user.save(using=self.db)
    return user

  def create_user(self, email, username, nombres, apellidos, dni, password=None,
    **extra_fields):

    return self._create_user(email, username, nombres, apellidos, dni, password,
      False, False, **extra_fields)

  def create_superuser(self, email, username, nombres, apellidos, dni, password=None,
    **extra_fields):

    return self._create_user(email, username, nombres, apellidos, dni, password,
      True, True, **extra_fields)

class Colaborador(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=254, unique=True, default="un")
    email = models.CharField(max_length=254, unique=True,)
    dni = models.CharField(max_length=8, unique=True,)
    celular = models.CharField(max_length=9, null=True, blank=True)
    tipousuarios = models.ForeignKey(TipoUsuario, models.DO_NOTHING, null=True, blank=True, related_name='colaborador_tipousuario')
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='colaborador_tienda')
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='colaborador_clienteportal')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Firma(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

class TipoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_comercial = models.CharField(max_length=500)
    razon_social = models.CharField(max_length=500)
    correo = models.CharField(max_length=500)
    RUC = models.CharField(max_length=11)
    celular = models.CharField(max_length=20)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.razon_social} {self.RUC}"

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    precio_base = models.DecimalField(max_digits=30, decimal_places=15)
    descripcion = models.CharField(max_length=1000)
    tiene_igv = models.BooleanField(null=True, blank=True)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    tipoproductos = models.ForeignKey(TipoProducto, models.DO_NOTHING, null=True, blank=True, related_name='producto_tipoproducto')
    empresas = models.ForeignKey(Empresa, models.DO_NOTHING, null=True, blank=True, related_name='producto_empresa')
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='producto_clienteportal')

    def __str__(self):
        return f"{self.nombre}"

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=500)
    apellidos = models.CharField(max_length=500)
    nombre_completo = models.CharField(max_length=500, null=True, blank=True)
    correo = models.CharField(max_length=500)
    dni = models.CharField(max_length=11)
    celular = models.CharField(max_length=20)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Persona(models.Model):
    id  = models.AutoField(primary_key=True)
    empresas = models.ForeignKey(Empresa, models.DO_NOTHING, null=True, blank=True, related_name='persona_empresa')
    clientes = models.ForeignKey(Cliente, models.DO_NOTHING, null=True, blank=True, related_name='persona_cliente')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)

class TipoPago(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class TipoEstadoProducto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class TipoMoneda(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    abreviacion = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500)
    personas = models.ForeignKey(Persona, models.DO_NOTHING, null=True, blank=True, related_name='venta_persona')
    colaboradores = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='venta_colaborador')
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='venta_tienda')
    descripcion = models.CharField(max_length=1000)
    impuesto = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    total = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_venta = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    es_credito = models.BooleanField(null=True, blank=True)
    tipopagos = models.ForeignKey(TipoPago, models.DO_NOTHING, null=True, blank=True, related_name='venta_tipopago')
    tipoestadoproductos = models.ForeignKey(TipoEstadoProducto, models.DO_NOTHING, null=True, blank=True, related_name='venta_tipoestadoproducto')
    tipomonedas = models.ForeignKey(TipoMoneda, models.DO_NOTHING, null=True, blank=True, related_name='venta_tipomoneda')
    tipocomprobante = models.CharField(max_length=500, null=True, blank=True)
    tipoigv = models.CharField(max_length=500, null=True, blank=True)
    tipopago = models.CharField(max_length=500, null=True, blank=True)
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='venta_clienteportal')
    comprobanteaprobado = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo}"

class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    precio_sin_descuento = models.DecimalField(max_digits=30, decimal_places=15)
    precio_unitario = models.DecimalField(max_digits=30, decimal_places=15)
    cantidad = models.DecimalField(max_digits=30, decimal_places=15)
    total = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    descuento_unitario = models.DecimalField(max_digits=30, decimal_places=15)
    productos = models.ForeignKey(Producto, models.DO_NOTHING, null=True, blank=True, related_name='detalleventa_producto')
    ventas = models.ForeignKey(Venta, models.DO_NOTHING, null=True, blank=True, related_name='detalleventa_venta')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

class CreditoBoletaFactura(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_pagar = models.DateField(null=True, blank=True)
    monto_pagar = models.DecimalField(max_digits=30, decimal_places=15)
    estado = models.CharField(max_length=3)
    fecha_creacion = models.DateField(auto_now_add=True)
    ventas = models.ForeignKey(Venta, models.DO_NOTHING, null=True, blank=True, related_name='creditoboletafactura_venta')

    def __str__(self):
        return f"{self.nombre}"

class CreditoVenta(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500, null=True, blank=True)
    monto_pago = models.DecimalField(max_digits=30, decimal_places=15)
    fecha_abono = models.DateField(null=True, blank=True)
    descripcion = models.CharField(max_length=1000, null=True, blank=True)
    ventas = models.ForeignKey(Venta, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_venta')
    personas = models.ForeignKey(Persona, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_persona')
    colaboradores = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_colaborador')
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_tienda')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    tipomonedas = models.ForeignKey(TipoMoneda, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_tipomoneda')
    tipopagos = models.ForeignKey(TipoPago, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_tipopago')
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='creditoventa_clienteportal')

class Compra(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500)
    personas = models.ForeignKey(Persona, models.DO_NOTHING, null=True, blank=True, related_name='compra_persona')
    colaboradores = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='compra_colaborador')
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='compra_tienda')
    descripcion = models.CharField(max_length=1000)
    impuesto = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    total = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    tipomonedas = models.ForeignKey(TipoMoneda, models.DO_NOTHING, null=True, blank=True, related_name='compra_tipomoneda')
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='compra_clienteportal')

    def __str__(self):
        return f"{self.codigo}"

class DetalleCompra(models.Model):
    id = models.AutoField(primary_key=True)
    precio_unitario = models.DecimalField(max_digits=30, decimal_places=15)
    cantidad = models.DecimalField(max_digits=30, decimal_places=15)
    total = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    productos = models.ForeignKey(Producto, models.DO_NOTHING, null=True, blank=True, related_name='detallecompra_producto')
    compras = models.ForeignKey(Compra, models.DO_NOTHING, null=True, blank=True, related_name='detallecompra_compra')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    cambiar_precio = models.BooleanField(null=True, blank=True)
    precio_unitario_compra = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    tipo_cambio = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    porcentaje_ganancia = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    precio_unitario_soles = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

class Movimiento(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500)
    colaboradores_emisor = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_colaborador_creacion')
    fue_preparado = models.BooleanField(null=True, blank=True)
    colaboradores_transporte = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_colaborador_transporte')
    fue_enviado = models.BooleanField(null=True, blank=True)
    colaboradores_receptor = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_colaborador_receptor')
    fue_recibido = models.BooleanField(null=True, blank=True)
    tiendas_origen = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_tiendaorigin')
    tiendas_destino = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_tiendadestino')
    descripcion = models.CharField(max_length=1000)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_movimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='movimiento_clienteportal')

    def __str__(self):
        return f"{self.codigo}"

class DetalleMovimiento(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=30, decimal_places=15)
    productos = models.ForeignKey(Producto, models.DO_NOTHING, null=True, blank=True, related_name='detallemovimiento_producto')
    movimientos = models.ForeignKey(Movimiento, models.DO_NOTHING, null=True, blank=True, related_name='detallemovimineto_movimiento')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

class Entrega(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500)
    colaboradores_emisor = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='entrega_colaborador_preparador')
    fue_preparado = models.BooleanField(null=True, blank=True)
    colaboradores_transporte = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='entrega_colaborador_transporte')
    fue_enviado = models.BooleanField(null=True, blank=True)
    personas = models.ForeignKey(Persona, models.DO_NOTHING, null=True, blank=True, related_name='entrega_persona')
    fue_entregado = models.BooleanField(null=True, blank=True)
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='entrega_tienda')
    descripcion = models.CharField(max_length=1000)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    ventas = models.ForeignKey(Venta, models.DO_NOTHING, null=True, blank=True, related_name='entrega_venta')
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='entrega_clienteportal')

    def __str__(self):
        return f"{self.codigo}"

class DetalleEntrega(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.DecimalField(max_digits=30, decimal_places=15)
    productos = models.ForeignKey(Producto, models.DO_NOTHING, null=True, blank=True, related_name='detalleentrega_producto')
    entregas = models.ForeignKey(Entrega, models.DO_NOTHING, null=True, blank=True, related_name='detalleentrega_entrega')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

class ProductoGasto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=500)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"

class Gasto(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=500)
    colaboradores = models.ForeignKey(Colaborador, models.DO_NOTHING, null=True, blank=True, related_name='gasto_colaborador')
    tiendas = models.ForeignKey(Tienda, models.DO_NOTHING, null=True, blank=True, related_name='gasto_tienda')
    descripcion = models.CharField(max_length=1000)
    impuesto = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    total = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_gasto = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)
    clientesportales = models.ForeignKey(ClientePortal, models.DO_NOTHING, null=True, blank=True, related_name='gasto_clienteportal')

    def __str__(self):
        return f"{self.codigo}"

class DetalleGasto(models.Model):
    id = models.AutoField(primary_key=True)
    monto_gastado = models.DecimalField(max_digits=30, decimal_places=15)
    productos_gastos = models.ForeignKey(ProductoGasto, models.DO_NOTHING, null=True, blank=True, related_name='detallegasto_productogasto')
    gastos = models.ForeignKey(Gasto, models.DO_NOTHING, null=True, blank=True, related_name='detallegasto_gasto')
    estado = models.CharField(max_length=3, null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True, blank=True)

