from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    # Agrega cualquier otro campo adicional que necesites para tus usuarios
    direccion = models.CharField(max_length=200)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    # Agrega cualquier otro campo adicional que necesites para tus categorías

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    # Agrega cualquier otro campo adicional que necesites para tus métodos de pago

    def __str__(self):
        return self.nombre

class Resena(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    contenido = models.TextField()
    calificacion = models.FloatField()

    def __str__(self):
        return f"Reseña de {self.usuario.email} para {self.producto.nombre}: {self.contenido[:50]}"

class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Venta de {self.usuario.email} - Precio Total: {self.precio_total}"

class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura #{self.id} - Venta: {self.venta.id}, Fecha: {self.fecha}"
