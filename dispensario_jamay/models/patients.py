# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import date
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class Patients(models.Model):
    _name = 'hospital.patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Model to register all patients'
    _rec_name = 'id'


    consecutive = fields.Char(string="Folio", track_visibility="onchange", help="Numero consecutivo de pacientes", readonly=True)

    #Consecutivo
    @api.model
    def create(self, variables):
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.pacientes')
        variables['consecutive'] = correlativo
        return super(Patients, self).create(variables)

    #Funcion para NO eliminar registros
    @api.constrains()
    def unlink(self):
        # Verifica si el usuario pertenece al grupo antes de permitir la eliminación
        if not self.env.user.has_group('dispensario_jamay.hospital_patients_permision_delete'):
            raise UserError('No puedes eliminar registros si no perteneces al grupo autorizado.')

        return super(Patients, self).unlink()

    # Patient identification
    file_number = fields.Char(string="Número de expediente", track_visibility='onchange',
                              help="Escribe el número del expediente")
    _sql_constraints = [
        (
            "name_unique",
            "unique(file_number)",
            "Ya existe este numero de expediente",
        ),
    ]

    # Personal information

    # Funcion name_get para obtener el nombre completo (nombre y apellidos) que se utilizara en prescription.note
    def name_get(self):
        result = []  # Inicializa una lista vacía para almacenar las tuplas de ID y nombre personalizado
        for record in self:  # Itera sobre cada registro en el conjunto de registros de DiagnosticNote
            name = f"{record.name} {record.first_last_name} {record.second_last_name}"  # Construye el nombre personalizado utilizando la clave y el nombre del diagnóstico
            result.append((record.id,
                           name))  # Agrega una tupla a la lista result con el ID del registro y el nombre personalizado
        return result  # Devuelve la lista de tuplas de ID y nombres personalizados

    name = fields.Char(string="Nombre(s)", track_visibility='onchange', help="Escribe el nombre del paciente",
                       required=True)
    first_last_name = fields.Char(string="Primer apellido", track_visibility='onchange',
                                  help="Escribe el primer apellido del paciente", required=True)
    second_last_name = fields.Char(string="Segundo apellido", track_visibility='onchange',
                                   help="Escribe el segundo apellido del paciente", required=True)
    name_full = fields.Char(string="Nombre completo", compute='_compute_name_full', store=True, )
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True, index=True,
                              string="Nombre del Medico", help="Nombre del medico")

    # Funcion para crear campo name_full y concatenar nombre y apellidos
    @api.depends('name', 'first_last_name', 'second_last_name')
    def _compute_name_full(self):
        for patient in self:
            patient.name_full = f"{patient.name} {patient.first_last_name} {patient.second_last_name}"

    # Funcion para calcular la edad
    @api.depends("birthday")
    def onchange_age(self):
        for record in self:
            if record.birthday:
                d1 = record.birthday
                d2 = datetime.today().date()
                rf = relativedelta(d2, d1)  # Relativedelta es para restar entre fechas
                record.age = str(rf.years) + " " + 'Años'
            else:
                record.age = "Sin fecha de nacimiento"

    birthday = fields.Date(string="Fecha de nacimiento", track_visibility='onchange',
                           help="Seleccione la fecha de nacimiento", required=True)
    age = fields.Char(string="Edad", compute=onchange_age)

    # Funcion para que no se seleccione una fecha que no coincida con el cumpleaños del usuario
    @api.constrains('birthday')
    def _limitar_fecha(self):
        for record in self:
            if record.birthday and record.birthday >= fields.Date.today():
                raise ValidationError(_("La fecha de cumpleaños no puede ser mayor que hoy"))

    sex = fields.Selection([('man', 'Hombre'), ('woman', 'Mujer')], string="Sexo", track_visibility='onchange',
                           help="Seleccione su sexo")
    gender = fields.Selection([('male', 'Masculino'), ('female', 'Femenino')], string="Género",
                              track_visibility='onchange', help="Seleccione su género")
    country_id = fields.Many2one(comodel_name='res.country', string="País de nacimiento", track_visibility='onchange',
                                 help="Seleccione su país de nacimiento", domain=[('code', '=', 'MX')])
    state = fields.Selection([('jal', 'Jalisco')], string="Entidad de nacimiento", track_visibility='onchange',
                             help="Seleccione su entidad de nacimiento")  # Nombre diferente para la tabla
    curp = fields.Char(string="CURP", track_visibility='onchange', help="Escribe su CURP")
    migrant = fields.Selection([('no', 'No'), ('yes', 'Si')], string="Migrante", track_visibility='onchange',
                               help="¿Es migrante?")
    religion = fields.Char(string="Religión", track_visibility='onchange', help="¿Cual es su religion?")
    disabled = fields.Selection([('no', 'No'), ('yes', 'Si')], string="Discapacitado", track_visibility='onchange',
                                help="¿Está discapacitado?")
    indigenous = fields.Selection([('no', 'No'), ('yes', 'Si')], string="Indígena", track_visibility='onchange',
                                  help="¿Es indigena?")
    speak_indigenous = fields.Selection([('no', 'No'), ('yes', 'Si')], string="¿Habla alguna lengua indígena?",
                                        track_visibility='onchange', help="¿Habla alguna lengua indígena?")
    phone = fields.Char(string="Teléfono", track_visibility='onchange', help="Escribe su numero de telefono")
    marinal_status = fields.Selection(
        [('single', 'Soltero'), ('married', 'Casado'), ('free_union', 'Unión libre'), ('ignore', 'Se ignora')],
        string="Estado conyugal", track_visibility='onchange', help="¿Cuál es su estado conyugal?")
    scholarship = fields.Selection(
        [('primary', 'Primaria'), ('high_school', 'Secundaria'), ('preparatory', 'Preparatoria'),
         ('degree', 'Licenciatura'), ('doctorate', 'Doctorado')], string="Escolaridad", track_visibility='onchange',
        help="¿Cual es su escolaridad?")
    read_and_write = fields.Selection([('no', 'No'), ('yes', 'Si')], string="¿Sabe leer y escribir?",
                                      track_visibility='onchange', help="¿Sabe leer y escribir?")
    occupation = fields.Char(string="Ocupación", track_visibility='onchange', help="¿Cual es su ocupación?")
    active = fields.Boolean(string="Archivado", default=True)
    # Domicilio
    resides = fields.Boolean(string="¿Reside en el extranjero?", track_visibility='onchange',
                             help="¿Reside en el extranjero?")
    country_dom_id = fields.Many2one(comodel_name='res.country', string="País", track_visibility='onchange',
                                     help="Seleccione su país", domain=[('code', '=', 'MX')])
    foreigner = fields.Boolean(string="Foráneo", track_visibility='onchange', help="¿Es foraneo?")
    type_of_road = fields.Selection([('street', 'Calle'), ('avenue', 'Avenida'), ('private', 'Privada')],
                                    string="Tipo de vialidad", track_visibility='onchange',
                                    help="¿Cuál es el tipo de vialidad?")
    road_name = fields.Char(string="Nombre de vialidad", track_visibility="onchange",
                            help="Escribe el nombre de la vialidad")
    num_ext = fields.Char(string="Número exterior", track_visibility="onchange", help="Escribe el número exterior")
    num_int = fields.Char(string="Número interior", track_visibility="onchange", help="Escribe el número interior")
    between_street = fields.Char(string="Entre calle", track_visibility="onchange", help="Entre calle")
    and_street = fields.Char(string="Y calle", track_visibility="onchange", help="Y calle")
    c_p = fields.Char(string="Código postal", track_visibility='onchange', help="¿Cuál es el código postal?")
    ignore_cp = fields.Boolean(string="Se ignora C.P", track_visibility='onchange', help="¿Se ignora el C.P?")
    settlement_type = fields.Selection(
        [('conj_hab', 'Conjunto habitacional'), ('ranch', 'Rancheria'), ('col', 'Colonia'), ('walker', 'Andador')],
        string="Tipo de asentamiento", track_visibility='onchange', help="¿Cuál es el tipo de asentamiento?")
    name_settlement = fields.Char(string="Nombre de asentamiento", track_visibility='onchange',
                                  help="Escribe el nombre del asentamiento (Colonia)")
    fed = fields.Selection([('jal', 'Jalisco')], string="Entidad federativa", track_visilibity="onchange",
                           help="Seleccione su entidad federativa")
    municipalities = fields.Selection([('jamay', 'Jamay')], string="Municipios", track_visibility='onchange',
                                      help="Seleccione su municipio")
    location = fields.Selection(
        [('not_specified', 'No especificado'), ('san_agustin', 'San agustin'), ('san_miguel', 'San miguel'),
         ('malta', 'Maltaraña')], string="Localidad", track_visibility='onchange', help="Seleccione su localidad")
    other_location = fields.Char(string="Otra localidad", track_visibility='onchange',
                                 help="¿Existe alguna otra localidad?")
    medical_note_one2many = fields.One2many('medical.note', 'patients_ids', string="Nota medica")


class Doctor_note(models.Model):
    _name = "medical.note"
    _description = "Note from doctor"
    _rec_name = 'id'

    date_medical = fields.Date(string="Fecha")
    ts = fields.Integer(string="TS (mmHg)")
    td = fields.Integer(string="TD (mmHg)")

    @api.onchange('ts', 'td')
    def _presion_arterial_media(self):
        self.tam = ((self.ts - self.td) / 3) + self.td

    tam = fields.Float(string="Tension Arterial Media",track_visibility="onchange",help="Escribe la Tension Arterial Media", compute="_presion_arterial_media")
    temp = fields.Integer(string="TEMP (GC)")
    frecc = fields.Integer(string="FRECC (ppm)")
    frecr = fields.Integer(string="FRECR (rpm)")
    glucosa = fields.Integer(string="GLUCOSA (mg/dl)")
    peso = fields.Integer(string="PESO (kg)", required=True)
    talla = fields.Integer(string="TALLA (cm)")
    imc = fields.Float(string="IMC", compute="_compute_imc")
    perimetro_cefalico = fields.Integer(string="PERIMETRO CEFALICO")
    perimetro_abdominal = fields.Integer(string="PERIMETRO ABDOMINAL (cm)")
    saturacion_oxigeno = fields.Integer(string="SATURACION OXIGENO")
    estado_nutricional = fields.Char(string="ESTADO NUTRICIONAL",compute="_compute_estado_nutricional",track_visibility="onchange",help="Estado nutricional")

    @api.onchange('imc')
    def _compute_estado_nutricional(self):
        for record in self:
            if record.imc < 18:
                record.estado_nutricional = "BAJO PESO"
            elif 18 <= record.imc < 25:
                record.estado_nutricional = "PESO SALUDABLE"
            elif 25 <= record.imc < 30:
                record.estado_nutricional = "SOBREPESO"
            elif 30 <= record.imc < 35:
                record.estado_nutricional = "OBESIDAD GRADO 1"
            elif 35 <= record.imc < 40:
                record.estado_nutricional = "OBESIDAD GRADO 2"
            elif record.imc >= 40:
                record.estado_nutricional = "OBESIDAD GRADO 3"


    nota_medica = fields.Text(string="Nota medica")
    patients_ids = fields.Many2one('hospital.patients')
    name_patients_id = fields.Many2one(comodel_name='hospital.patients', string="Nombre del paciente")
    user_name_medic = fields.Many2one(comodel_name='res.users', string="Nombre del medico")
    sequence = fields.Integer()
    # Funcion para calcular el IMC
    @api.onchange('talla','peso')
    def _compute_imc(self):
        if self.talla and self.peso:
            self.imc = self.peso / ((self.talla / 100) * (self.talla / 100))
        else:
            self.imc == 0.00






