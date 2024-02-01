# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Model inheritance to add professional and specialty ID fields'


    professional_license = fields.Char(string="Cédula profesional", help="Escribe tu Cédula profesional")
    specialty_certificate = fields.Char(string="Cédula de especialidad", help="Escribe tu Cédula de especialidad")
    profession = fields.Char(string="Carrera o profesión", help="Escribe tu carrera")
    university = fields.Char(string="Universidad de procedencia", help="¿De que universidad vienes?")
