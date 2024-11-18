from django.contrib import admin
from .models import UserProfile, SolicitudArriendo, Inmueble

# Register your models here.
# Métodos para acceder a los campos relacionados de User
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_nombres', 'get_apellidos', 'get_correo', 'get_user_type')

    def get_nombres(self, obj):
        return obj.user.first_name
    get_nombres.admin_order_field = 'user__first_name'
    get_nombres.short_description = 'Nombres'

    def get_apellidos(self, obj):
        return obj.user.last_name
    get_apellidos.admin_order_field = 'user__last_name'
    get_apellidos.short_description = 'Apellidos'

    def get_correo(self, obj):
        return obj.user.email
    get_correo.admin_order_field = 'user__email'
    get_correo.short_description = 'Correo'

    def get_user_type(self, obj):
        return obj.user_type
    get_user_type.admin_order_field = 'user_type'
    get_user_type.short_description = 'Tipo de Usuario'


class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('id_solicitud', 'userProfile', 'inmueble', 'fecha_solicitud', 'estado_solicitud', 'estado_solicitud')
    search_fields = ('userProfile__nombres', 'userProfile__apellidos', 'inmueble__nombre', 'estado_solicitud')
    list_filter = ['estado_solicitud']

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'tipo_inmueble', 'precio_mensual')
    search_fields = ('nombre', 'descripcion', 'tipo_inmueble')
    list_filter = ['tipo_inmueble']

#reordenamos el codigo dejando los model admin al final
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Inmueble, InmuebleAdmin)
admin.site.register(SolicitudArriendo, SolicitudArriendoAdmin)