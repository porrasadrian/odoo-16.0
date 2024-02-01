# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from datetime import date
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError



class DoctorNote(models.Model):
    _name = "medical.note"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Note from doctor"
    _rec_name = 'id'

    consecutive_medical_note = fields.Char(string="Folio", track_visibility="onchange",
                                           help="Numero consecutivo de notas medicas", readonly=True)

    # Consecutivo
    @api.model
    def create(self, variables):
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.notas.medicas')
        variables['consecutive_medical_note'] = correlativo
        return super(DoctorNote, self).create(variables)

    date_medical = fields.Date(string="Fecha", track_visibility="onchange", help="Selecciona la fecha")
    ts = fields.Integer(string="Tension Sistolica (mmHg)", track_visibility="onchange",
                        help="Escribe la Tension Sistolica")
    td = fields.Integer(string="Tension Diastolica (mmHg)", track_visibility="onchange",
                        help="Escribe la Tension Diastolica")

    @api.onchange('ts', 'td')
    def _presion_arterial_media(self):
        self.tam = ((self.ts - self.td) / 3) + self.td

    tam = fields.Float(string="Tension Arterial Media", track_visibility="onchange",
                       help="Escribe la Tension Arterial Media", readonly=True, compute="_presion_arterial_media")
    temp = fields.Integer(string="Temperatura (GC)", track_visibility="onchange", help="Escribe la temperatura")
    frecc = fields.Integer(string="Frecuencia cardiaca (ppm)", track_visibility="onchange",
                           help="Escribe la Frecuencia cardiaca")
    frecr = fields.Integer(string="Frecuencia respiratoria (rpm)", track_visibility="onchange",
                           help="Escribe la Frecuencia respiratoria")
    glucosa = fields.Integer(string="GLUCOSA (mg/dl)", track_visibility="onchange", help="Escribe la Glucosa")
    peso = fields.Integer(string="PESO (kg)", required=True, track_visibility="onchange",
                          help="Escribe el peso del paciente")
    talla = fields.Integer(string="TALLA (cm)", track_visibility="onchange", help="Escribe la estatura del paciente")
    imc = fields.Float(string="Indice de masa corporal", compute="_compute_imc", track_visibility="onchange",
                       help="Indice de masa corporal")
    perimetro_cefalico = fields.Integer(string="PERIMETRO CEFALICO", track_visibility="onchange",
                                        help="Escribe el Perimetro cefalico")
    perimetro_abdominal = fields.Integer(string="PERIMETRO ABDOMINAL (cm)", track_visibility="onchange",
                                         help="Escribe el Perimetro abdominal")
    saturacion_oxigeno = fields.Integer(string="SATURACION OXIGENO", track_visibility="onchange",
                                        help="Escribe la saturacion de oxigeno")
    nota_medica = fields.Text(string="Nota medica", track_visibility="onchange",
                              help="Escribe la nota medica del paciente")
    patients_ids = fields.Many2one('hospital.patients')
    name_patients_id = fields.Many2one(comodel_name='hospital.patients', string="Nombre del paciente",
                                       track_visibility="onchange", help="Selecciona el nombre del paciente")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, readonly=True, index=True,
                              string="Nombre del Medico", help="Nombre del medico")
    active = fields.Boolean(string="Archivado", default=True)
    sequence = fields.Integer()
    # Este campo de name_full se esta utilizando para poder mandarlo llamar en la vista de busqueda
    name_full = fields.Char(related="name_patients_id.name_full", string="Nombre completo", readonly="1")

    # Funcion para NO eliminar registros
    @api.constrains()
    def unlink(self):
        # Verifica si el usuario pertenece al grupo antes de permitir la eliminación
        if not self.env.user.has_group('dispensario_jamay.hospital_patients_permision_delete'):
            raise UserError('No puedes eliminar registros si no perteneces al grupo autorizado.')

        return super(DoctorNote, self).unlink()

    # Funcion para calcular el IMC
    @api.onchange('talla', 'peso')
    def _compute_imc(self):
        if self.talla and self.peso:
            self.imc = self.peso / ((self.talla / 100) * (self.talla / 100))
        else:
            self.imc == 0.00

    estado_nutricional = fields.Char(string="ESTADO NUTRICIONAL", compute="_compute_estado_nutricional",
                                     track_visibility="onchange", help="Estado nutricional")

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







    # Funcion para imprimir el reporte
    def print_medical_note(self):
        return self.env.ref('dispensario_jamay.req_dispensario_jamay').report_action(self)
