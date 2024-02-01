# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class Diagnostic(models.Model):
    _name = 'diagnostic.note'
    _description = 'Model to store all existing diagnostics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'id'

    diagnostic_name = fields.Char(string="Nombre del diagnóstico",track_visibility="onchange",help="Escribe el nombre del diagnostico")


    #Funcion que concatena los campos diagnostic_key y diagnostic_name
    def name_get(self):
        result = []  # Inicializa una lista vacía para almacenar las tuplas de ID y nombre personalizado
        for record in self: # Itera sobre cada registro en el conjunto de registros de DiagnosticNote
            name = f"{record.diagnostic_name}" # Construye el nombre personalizado utilizando la clave y el nombre del diagnóstico
            result.append((record.id, name)) # Agrega una tupla a la lista result con el ID del registro y el nombre personalizado
        return result # Devuelve la lista de tuplas de ID y nombres personalizados

    active = fields.Boolean(string="Archivado", default=True)

    # Funcion para NO eliminar registros
    @api.constrains()
    def unlink(self):
        # Verifica si el usuario pertenece al grupo antes de permitir la eliminación
        if not self.env.user.has_group('dispensario_jamay.hospital_patients_permision_delete'):
            raise UserError('No puedes eliminar registros si no perteneces al grupo autorizado.')

        return super(Diagnostic, self).unlink()

