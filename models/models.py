#-*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import re
from odoo.exceptions import ValidationError

class modulo_clase(models.Model):
    _name = 'modulo.clase'
    _description = 'clase'

    name = fields.Char(string="Nombre")
    description = fields.Text(string="Tipo de aula")
    fecha = fields.Date(string="Fecha")
    hora_inicio = fields.Char(string="Hora de inicio", widget="time")
    hora_fin = fields.Char(string="Hora de fin", widget="time")
    profesor_id = fields.Many2one(
        comodel_name='modulo.profesor', 
        string="Profesor", 
        ondelete='restrict')
    alumno_ids = fields.Many2many(
        comodel_name='modulo.alumno', 
        string="Alumnos", 
        ondelete='cascade')
        
    @api.constrains('hora_inicio', 'hora_fin')
    def _check_hora(self):
        for record in self:
            hora_inicio = record.hora_inicio.strip()
            hora_fin = record.hora_fin.strip()
            # verificar que el formato sea HH:MM
            if not re.match(r'^\d{1,2}:\d{2}$', hora_inicio) or not re.match(r'^\d{1,2}:\d{2}$', hora_fin):
                raise ValidationError("La hora debe estar en formato HH:MM")
            # verificar que las horas y minutos sean válidos
            hi, mi = map(int, hora_inicio.split(':'))
            hf, mf = map(int, hora_fin.split(':'))
            if hi < 0 or hi > 23 or mi < 0 or mi > 59 or hf < 0 or hf > 23 or mf < 0 or mf > 59:
                raise ValidationError("La hora debe ser válida")
            # verificar que la hora de inicio sea menor que la hora de fin
            if record.hora_inicio > record.hora_fin:
                raise ValidationError("La hora de inicio debe ser menor que la hora de fin")

class modulo_profesor(models.Model):
    _name = 'modulo.profesor'
    _description = 'Profesor'

    name = fields.Char(string="Nombre")
    apellidos = fields.Char(string="Apellidos")
    email = fields.Char(string="Email")
    clases_ids = fields.One2many(
        comodel_name='modulo.clase',
        inverse_name='profesor_id', 
        string="Clases", 
        ondelete='set null')
    
    #el email debe ser unico:
    _sql_constraints = [
        ('email_unique',
        'UNIQUE(email)',
        "El email debe ser único"),
    ]


class modulo_alumno(models.Model):
    _name = 'modulo.alumno'
    _description = 'alumno'
    name = fields.Char(string="Nombre")
    apellidos = fields.Char(string="Apellidos")
    email = fields.Char(string="Email")
    dni = fields.Char(string="DNI", size=9)
    photo = fields.Image(max_width=100, max_height=100)
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    last_login = fields.Datetime(string="Último acceso", default=lambda self: fields.Datetime.now())
    enrollment_date = fields.Date(string="Fecha de inscripción", default=fields.Date.today())
    nivel_estudios  = fields.Selection(
        [('1', 'Primaria'), ('2', 'ESO'), ('3', 'Bachillerato')], string="Nivel de estudios")
    clases_ids = fields.Many2many(
        comodel_name='modulo.clase', 
        string="Clases", 
        ondelete='cascade')
    
    _sql_constraints = [
        ('email_unique',
        'UNIQUE(email)',
        "El email debe ser único"),
    ]

    @api.constrains('dni')
    def _check_dni(self):
        for record in self:
            dni = record.dni
            if dni and len(dni) == 9:
                if not re.match(r'^\d{8}[A-Za-z]$', dni):
                    raise ValidationError("El DNI debe tener 8 números seguidos de una letra.")
            else:
                raise ValidationError("El DNI debe tener 9 caracteres.")