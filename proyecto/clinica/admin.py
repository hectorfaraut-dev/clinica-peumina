from django.contrib import admin
from .models import Especialidad, Medico, Paciente, Cita, HistorialClinico


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'rut', 'especialidad', 'telefono', 'email', 'activo')
    list_filter = ('especialidad', 'activo')
    search_fields = ('nombre', 'apellido', 'rut', 'email')


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'rut', 'edad', 'telefono', 'email', 'prevision', 'activo')
    list_filter = ('sexo', 'prevision', 'activo')
    search_fields = ('nombre', 'apellido', 'rut', 'email')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'medico')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'medico__nombre', 'medico__apellido')
    date_hierarchy = 'fecha'


@admin.register(HistorialClinico)
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha')
    list_filter = ('fecha', 'medico')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'diagnostico')
