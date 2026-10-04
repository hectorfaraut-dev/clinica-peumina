from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Especialidad, Medico, Paciente, Cita, HistorialClinico


class BootstrapFormMixin:
    """Agrega la clase 'form-control' / 'form-select' a todos los campos."""
    def _bootstrap(self):
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.setdefault('class', 'form-select')
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault('class', 'form-check-input')
            else:
                widget.attrs.setdefault('class', 'form-control')


class EspecialidadForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()


class MedicoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            'nombre', 'apellido', 'rut', 'especialidad', 'telefono',
            'email', 'horario_inicio', 'horario_fin', 'activo'
        ]
        widgets = {
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'type': 'time'}),
            'rut': forms.TextInput(attrs={'placeholder': '12345678-9'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()


class PacienteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nombre', 'apellido', 'rut', 'fecha_nacimiento', 'sexo',
            'telefono', 'email', 'direccion', 'prevision', 'alergias', 'activo'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'alergias': forms.Textarea(attrs={'rows': 2}),
            'rut': forms.TextInput(attrs={'placeholder': '12345678-9'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()


class CitaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()
        self.fields['medico'].queryset = Medico.objects.filter(activo=True)
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)


class HistorialClinicoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['paciente', 'medico', 'cita', 'diagnostico', 'tratamiento', 'notas']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()
        self.fields['cita'].required = False


class RegistroUsuarioForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bootstrap()


class BusquedaForm(forms.Form):
    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Buscar...'
        })
    )
