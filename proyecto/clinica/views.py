from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)

from .models import Especialidad, Medico, Paciente, Cita, HistorialClinico
from .forms import (
    EspecialidadForm, MedicoForm, PacienteForm, CitaForm,
    HistorialClinicoForm, RegistroUsuarioForm
)


# ---------- Autenticación ----------

def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido/a, {user.first_name or user.username}!')
            return redirect('clinica:dashboard')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})


# ---------- Dashboard ----------

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'clinica/dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        ctx['total_pacientes'] = Paciente.objects.filter(activo=True).count()
        ctx['total_medicos'] = Medico.objects.filter(activo=True).count()
        ctx['total_especialidades'] = Especialidad.objects.count()
        ctx['citas_hoy'] = Cita.objects.filter(fecha=hoy).select_related('paciente', 'medico')
        ctx['citas_pendientes'] = Cita.objects.filter(estado='pendiente').count()
        ctx['proximas_citas'] = Cita.objects.filter(
            fecha__gte=hoy, estado__in=['pendiente', 'confirmada']
        ).select_related('paciente', 'medico').order_by('fecha', 'hora')[:8]
        ctx['medicos_por_especialidad'] = Especialidad.objects.annotate(
            total=Count('medicos')
        ).order_by('-total')[:6]
        return ctx


# ---------- Especialidad ----------

class EspecialidadListView(LoginRequiredMixin, ListView):
    model = Especialidad
    template_name = 'clinica/especialidad_list.html'
    context_object_name = 'especialidades'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        qs = super().get_queryset().annotate(total_medicos=Count('medicos'))
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs


class EspecialidadCreateView(LoginRequiredMixin, CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:especialidad_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Nueva Especialidad'}

    def form_valid(self, form):
        messages.success(self.request, 'Especialidad creada correctamente.')
        return super().form_valid(form)


class EspecialidadUpdateView(LoginRequiredMixin, UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:especialidad_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Editar Especialidad'}

    def form_valid(self, form):
        messages.success(self.request, 'Especialidad actualizada correctamente.')
        return super().form_valid(form)


class EspecialidadDeleteView(LoginRequiredMixin, DeleteView):
    model = Especialidad
    template_name = 'clinica/confirmar_eliminar.html'
    success_url = reverse_lazy('clinica:especialidad_lista')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Especialidad eliminada.')
        return super().form_valid(form)


# ---------- Médico ----------

class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = 'clinica/medico_list.html'
    context_object_name = 'medicos'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        qs = super().get_queryset().select_related('especialidad')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(apellido__icontains=q) |
                Q(rut__icontains=q) | Q(especialidad__nombre__icontains=q)
            )
        return qs


class MedicoDetailView(LoginRequiredMixin, DetailView):
    model = Medico
    template_name = 'clinica/medico_detalle.html'
    context_object_name = 'medico'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['citas'] = self.object.citas.select_related('paciente').order_by('-fecha', '-hora')[:10]
        return ctx


class MedicoCreateView(LoginRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:medico_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Nuevo Médico'}

    def form_valid(self, form):
        messages.success(self.request, 'Médico registrado correctamente.')
        return super().form_valid(form)


class MedicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:medico_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Editar Médico'}

    def form_valid(self, form):
        messages.success(self.request, 'Médico actualizado correctamente.')
        return super().form_valid(form)


class MedicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medico
    template_name = 'clinica/confirmar_eliminar.html'
    success_url = reverse_lazy('clinica:medico_lista')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Médico eliminado.')
        return super().form_valid(form)


# ---------- Paciente ----------

class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'clinica/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(rut__icontains=q)
            )
        return qs


class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'clinica/paciente_detalle.html'
    context_object_name = 'paciente'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['citas'] = self.object.citas.select_related('medico').order_by('-fecha', '-hora')[:10]
        ctx['historial'] = self.object.historial.select_related('medico').order_by('-fecha')[:10]
        return ctx


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:paciente_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Nuevo Paciente'}

    def form_valid(self, form):
        messages.success(self.request, 'Paciente registrado correctamente.')
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:paciente_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Editar Paciente'}

    def form_valid(self, form):
        messages.success(self.request, 'Paciente actualizado correctamente.')
        return super().form_valid(form)


class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'clinica/confirmar_eliminar.html'
    success_url = reverse_lazy('clinica:paciente_lista')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Paciente eliminado.')
        return super().form_valid(form)


# ---------- Cita ----------

class CitaListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'clinica/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 10
    login_url = 'login'

    def get_queryset(self):
        qs = super().get_queryset().select_related('paciente', 'medico')
        q = self.request.GET.get('q')
        estado = self.request.GET.get('estado')
        if q:
            qs = qs.filter(
                Q(paciente__nombre__icontains=q) | Q(paciente__apellido__icontains=q) |
                Q(medico__nombre__icontains=q) | Q(medico__apellido__icontains=q)
            )
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estados'] = Cita.ESTADO_CHOICES
        ctx['estado_actual'] = self.request.GET.get('estado', '')
        return ctx


class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'clinica/cita_detalle.html'
    context_object_name = 'cita'
    login_url = 'login'


class CitaCreateView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:cita_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Agendar Cita'}

    def form_valid(self, form):
        messages.success(self.request, 'Cita agendada correctamente.')
        return super().form_valid(form)


class CitaUpdateView(LoginRequiredMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'clinica/form_generico.html'
    success_url = reverse_lazy('clinica:cita_lista')
    login_url = 'login'
    extra_context = {'titulo': 'Editar Cita'}

    def form_valid(self, form):
        messages.success(self.request, 'Cita actualizada correctamente.')
        return super().form_valid(form)


class CitaDeleteView(LoginRequiredMixin, DeleteView):
    model = Cita
    template_name = 'clinica/confirmar_eliminar.html'
    success_url = reverse_lazy('clinica:cita_lista')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Cita eliminada.')
        return super().form_valid(form)


@login_required(login_url='login')
def cambiar_estado_cita(request, pk, estado):
    cita = get_object_or_404(Cita, pk=pk)
    estados_validos = dict(Cita.ESTADO_CHOICES)
    if estado in estados_validos:
        cita.estado = estado
        cita.save()
        messages.success(request, f'Cita marcada como "{estados_validos[estado]}".')
    return redirect('clinica:cita_detalle', pk=pk)


# ---------- Historial clínico ----------

class HistorialCreateView(LoginRequiredMixin, CreateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = 'clinica/form_generico.html'
    login_url = 'login'
    extra_context = {'titulo': 'Nueva Entrada de Historial Clínico'}

    def get_initial(self):
        initial = super().get_initial()
        paciente_id = self.request.GET.get('paciente')
        if paciente_id:
            initial['paciente'] = paciente_id
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Entrada de historial clínico agregada.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clinica:paciente_detalle', args=[self.object.paciente.pk])


class HistorialDeleteView(LoginRequiredMixin, DeleteView):
    model = HistorialClinico
    template_name = 'clinica/confirmar_eliminar.html'
    login_url = 'login'

    def get_success_url(self):
        messages.success(self.request, 'Entrada de historial eliminada.')
        return reverse_lazy('clinica:paciente_detalle', args=[self.object.paciente.pk])
