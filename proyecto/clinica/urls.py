from django.urls import path
from . import views

app_name = 'clinica'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('registro/', views.registro_view, name='registro'),

    # Especialidades
    path('especialidades/', views.EspecialidadListView.as_view(), name='especialidad_lista'),
    path('especialidades/nueva/', views.EspecialidadCreateView.as_view(), name='especialidad_crear'),
    path('especialidades/<int:pk>/editar/', views.EspecialidadUpdateView.as_view(), name='especialidad_editar'),
    path('especialidades/<int:pk>/eliminar/', views.EspecialidadDeleteView.as_view(), name='especialidad_eliminar'),

    # Médicos
    path('medicos/', views.MedicoListView.as_view(), name='medico_lista'),
    path('medicos/nuevo/', views.MedicoCreateView.as_view(), name='medico_crear'),
    path('medicos/<int:pk>/', views.MedicoDetailView.as_view(), name='medico_detalle'),
    path('medicos/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='medico_editar'),
    path('medicos/<int:pk>/eliminar/', views.MedicoDeleteView.as_view(), name='medico_eliminar'),

    # Pacientes
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_lista'),
    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_crear'),
    path('pacientes/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detalle'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='paciente_eliminar'),

    # Citas
    path('citas/', views.CitaListView.as_view(), name='cita_lista'),
    path('citas/nueva/', views.CitaCreateView.as_view(), name='cita_crear'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detalle'),
    path('citas/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_editar'),
    path('citas/<int:pk>/eliminar/', views.CitaDeleteView.as_view(), name='cita_eliminar'),
    path('citas/<int:pk>/estado/<str:estado>/', views.cambiar_estado_cita, name='cita_cambiar_estado'),

    # Historial clínico
    path('historial/nuevo/', views.HistorialCreateView.as_view(), name='historial_crear'),
    path('historial/<int:pk>/eliminar/', views.HistorialDeleteView.as_view(), name='historial_eliminar'),
]
