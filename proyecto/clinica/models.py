from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse


rut_validator = RegexValidator(
    regex=r'^\d{7,8}-[\dkK]$',
    message="El RUT debe tener el formato 12345678-9"
)

telefono_validator = RegexValidator(
    regex=r'^\+?\d{8,15}$',
    message="Ingrese un número de teléfono válido (8 a 15 dígitos)."
)


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Medico(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="perfil_medico"
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True, validators=[rut_validator])
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.PROTECT, related_name="medicos"
    )
    telefono = models.CharField(max_length=15, validators=[telefono_validator])
    email = models.EmailField()
    horario_inicio = models.TimeField(default="09:00")
    horario_fin = models.TimeField(default="18:00")
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"Dr(a). {self.nombre} {self.apellido} - {self.especialidad}"

    def get_absolute_url(self):
        return reverse('clinica:medico_detalle', args=[self.pk])

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True, validators=[rut_validator])
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='O')
    telefono = models.CharField(max_length=15, validators=[telefono_validator])
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    prevision = models.CharField(
        max_length=50, blank=True,
        help_text="Fonasa, Isapre, Particular, etc."
    )
    alergias = models.TextField(blank=True, help_text="Alergias conocidas del paciente")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"

    def get_absolute_url(self):
        return reverse('clinica:paciente_detalle', args=[self.pk])

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def edad(self):
        from datetime import date
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="citas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="citas")
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-fecha', '-hora']
        constraints = [
            models.UniqueConstraint(
                fields=['medico', 'fecha', 'hora'],
                name='unico_horario_por_medico'
            )
        ]

    def __str__(self):
        return f"{self.paciente} con {self.medico} - {self.fecha} {self.hora}"

    def get_absolute_url(self):
        return reverse('clinica:cita_detalle', args=[self.pk])


class HistorialClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="historial")
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, related_name="atenciones")
    cita = models.ForeignKey(
        Cita, on_delete=models.SET_NULL, null=True, blank=True, related_name="historial"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField(blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Historial Clínico"
        verbose_name_plural = "Historiales Clínicos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Historial de {self.paciente} - {self.fecha.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse('clinica:paciente_detalle', args=[self.paciente.pk])
