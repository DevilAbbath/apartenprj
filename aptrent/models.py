from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Inmueble(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_totales = models.FloatField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=100)
    tipo_inmueble = models.CharField(max_length=50)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
# Crear el perfil de usuario para linkearlo al User de Django
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #relacion 1 a 1
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=9, blank=True)
    user_type = models.CharField(max_length=20, choices=[('arrendatario', 'Arrendatario'), ('arrendador', 'Arrendador')])
    direccion = models.CharField(max_length=200, blank=True)
    #Espificar que el campo no quede vacio o en blanco
    nombres = models.CharField(max_length=100, blank=False)
    apellidos = models.CharField(max_length=100, blank=False)
    correo = models.EmailField(blank=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user_type}"
    
#Signals o señales para crear y guardar los UserProfile
#los KWARGS o Keyboard Arguments se usan para pasar n cantidad de 
#argumentos con nombre sin necesidad de definirlos
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userProfile.save()
    
#Apartado de Ingreso de solicitudes de arriendo
class SolicitudArriendo(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    
    #Relacionarlo con UserProfile en vez del User
    userProfile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    inmueble = models.ForeignKey('Inmueble', on_delete=models.CASCADE)
    fecha_solicitud = models.DateField()
    estado_solicitud = models.CharField(max_length=20, choices=[
        ('pendiente','Pendiente'),
        ('aceptada','Aceptada'),
        ('rechazada','Rechazada')
    ])
    
    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.userProfile.nombres}"