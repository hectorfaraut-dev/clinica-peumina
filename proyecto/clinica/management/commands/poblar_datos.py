import random
from datetime import date, timedelta, time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from clinica.models import Especialidad, Medico, Paciente, Cita, HistorialClinico


class Command(BaseCommand):
    help = "Puebla la base de datos con datos de ejemplo para Clínica Peumina."

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@clinicapeumina.cl', 'admin1234')
            self.stdout.write(self.style.SUCCESS('Superusuario creado -> usuario: admin / clave: admin1234'))

        especialidades_data = [
            ('Medicina General', 'Atención primaria y consultas generales.'),
            ('Pediatría', 'Atención médica para niños y adolescentes.'),
            ('Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón.'),
            ('Dermatología', 'Diagnóstico y tratamiento de enfermedades de la piel.'),
            ('Traumatología', 'Tratamiento de lesiones del sistema musculoesquelético.'),
            ('Ginecología', 'Salud del sistema reproductivo femenino.'),
        ]
        especialidades = []
        for nombre, descripcion in especialidades_data:
            esp, _ = Especialidad.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})
            especialidades.append(esp)

        medicos_data = [
            ('Javiera', 'Muñoz', '12345678-9', 0, '+56911111111', 'jmunoz@clinicapeumina.cl'),
            ('Matías', 'Rojas', '13456789-0', 1, '+56922222222', 'mrojas@clinicapeumina.cl'),
            ('Camila', 'Fernández', '14567890-1', 2, '+56933333333', 'cfernandez@clinicapeumina.cl'),
            ('Tomás', 'Soto', '15678901-2', 3, '+56944444444', 'tsoto@clinicapeumina.cl'),
            ('Valentina', 'Contreras', '16789012-3', 4, '+56955555555', 'vcontreras@clinicapeumina.cl'),
            ('Sebastián', 'Pizarro', '17890123-4', 5, '+56966666666', 'spizarro@clinicapeumina.cl'),
        ]
        medicos = []
        for nombre, apellido, rut, esp_idx, telefono, email in medicos_data:
            medico, _ = Medico.objects.get_or_create(
                rut=rut,
                defaults=dict(
                    nombre=nombre, apellido=apellido,
                    especialidad=especialidades[esp_idx],
                    telefono=telefono, email=email,
                    horario_inicio=time(9, 0), horario_fin=time(18, 0),
                )
            )
            medicos.append(medico)

        pacientes_data = [
            ('Antonia', 'López', '20111222-3', date(1990, 5, 12), 'F', '+56977777771'),
            ('Diego', 'Vargas', '20222333-4', date(1985, 8, 23), 'M', '+56977777772'),
            ('Isidora', 'Castro', '20333444-5', date(2001, 1, 30), 'F', '+56977777773'),
            ('Benjamín', 'Reyes', '20444555-6', date(1978, 11, 2), 'M', '+56977777774'),
            ('Florencia', 'Tapia', '20555666-7', date(1995, 3, 17), 'F', '+56977777775'),
            ('Ignacio', 'Morales', '20666777-8', date(2010, 6, 9), 'M', '+56977777776'),
            ('Josefa', 'Araya', '20777888-9', date(1966, 12, 25), 'F', '+56977777777'),
            ('Cristóbal', 'Silva', '20888999-0', date(1999, 9, 14), 'M', '+56977777778'),
        ]
        pacientes = []
        previsiones = ['Fonasa', 'Isapre', 'Particular']
        for nombre, apellido, rut, nacimiento, sexo, telefono in pacientes_data:
            paciente, _ = Paciente.objects.get_or_create(
                rut=rut,
                defaults=dict(
                    nombre=nombre, apellido=apellido, fecha_nacimiento=nacimiento,
                    sexo=sexo, telefono=telefono,
                    email=f"{nombre.lower()}.{apellido.lower()}@example.com",
                    direccion="Peumo, O'Higgins", prevision=random.choice(previsiones),
                )
            )
            pacientes.append(paciente)

        hoy = date.today()
        motivos = [
            'Control general', 'Dolor de cabeza persistente', 'Chequeo anual',
            'Dolor abdominal', 'Control de presión arterial', 'Consulta dermatológica',
            'Dolor en articulaciones', 'Control pediátrico',
        ]
        estados = ['pendiente', 'confirmada', 'atendida']
        horas = [time(9, 0), time(10, 30), time(11, 0), time(15, 0), time(16, 30), time(17, 0)]

        creadas = 0
        for i in range(15):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            dia_offset = random.randint(-10, 15)
            fecha = hoy + timedelta(days=dia_offset)
            hora = random.choice(horas)
            estado = 'atendida' if dia_offset < 0 else random.choice(['pendiente', 'confirmada'])
            cita, created = Cita.objects.get_or_create(
                medico=medico, fecha=fecha, hora=hora,
                defaults=dict(paciente=paciente, motivo=random.choice(motivos), estado=estado)
            )
            if created:
                creadas += 1
                if estado == 'atendida':
                    HistorialClinico.objects.create(
                        paciente=paciente, medico=medico, cita=cita,
                        diagnostico='Cuadro leve, evolución favorable.',
                        tratamiento='Reposo e hidratación, control en 7 días si persisten síntomas.',
                        notas='Paciente cooperador durante la consulta.'
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Datos de ejemplo creados: {len(especialidades)} especialidades, '
            f'{len(medicos)} médicos, {len(pacientes)} pacientes, {creadas} citas.'
        ))
