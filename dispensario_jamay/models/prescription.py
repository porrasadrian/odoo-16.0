from odoo import fields,models,api
from odoo.exceptions import UserError
class Prescription(models.Model):
    _name ='prescription.note'
    _description = 'Table to add medical prescriptions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_patients_prescription'

    consecutive_prescription = fields.Char(string="Folio", track_visibility="onchange", help="Numero consecutivo de recetas medicas",
                              readonly=True)
    # Consecutivo
    @api.model
    def create(self, variables):
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.recetas.medicas')
        variables['consecutive_prescription'] = correlativo
        return super(Prescription, self).create(variables)

    curp = fields.Char(string="CURP",search="True", readonly=True, track_visibility="onchange",help="CURP del paciente")
    record = fields.Char(string="Expedientes",search="True", readonly=True,track_visibility="onchange", help="Numero de expediente del paciente")
    name_patients_prescription = fields.Many2one(comodel_name='hospital.patients',search="True",string="Nombre del paciente",track_visibility="onchange",help="Nombre completo del paciente")
    date_patients_prescription = fields.Date(string="Fecha de nacimiento del paciente", readonly=True,track_visibility="onchange",help="Fecha de nacimiento del paciente")
    active = fields.Boolean(string="Archivado", default=True)
    details = fields.Text(string="Detalles de las indicaciones", help="Escribe los detalles de las indicaciones")
    prescription_line_ids = fields.One2many('prescription.note.line', 'prescription_id')

    ############# RELATED PARA FILTROS ############################
    name_full_prescription = fields.Char(related="name_patients_prescription.name_full")
    diagnosis_name = fields.Char(related='prescription_line_ids.diagnosis.diagnostic_name', store=True,
                                 string='Nombre del diagnostico', readonly=True)
    medic_name = fields.Char(related="prescription_line_ids.search_medicine", string="Nombre del medicamento")

    ############# RELATED PARA FILTROS ############################

    #Funcion para traer la informacion de los campos que estan en hospital.patients
    @api.constrains('name_patients_prescription')
    def _onchange_name_patients_prescription(self):
        if self.name_patients_prescription:
            self.record = self.name_patients_prescription.file_number
            self.date_patients_prescription = self.name_patients_prescription.birthday
            self.curp = self.name_patients_prescription.curp

        # Funcion para NO eliminar registros

    @api.constrains()
    def unlink(self):
        # Verifica si el usuario pertenece al grupo antes de permitir la eliminación
        if not self.env.user.has_group('dispensario_jamay.hospital_patients_permision_delete'):
            raise UserError('No puedes eliminar registros si no perteneces al grupo autorizado.')

        return super(Prescription, self).unlink()


class PrescriptionLine(models.Model):
    _name = 'prescription.note.line'
    _description = 'Model to save medical prescriptions'


    prescription_id = fields.Many2one(comodel_name='prescription.note', invisible=True)
    diagnosis = fields.Many2one(comodel_name='diagnostic.note',
                                string="Buscar diagnostico (Clave o nombre de diagnostico)",track_visibility="onchange",help="¿Cual es el diagnostico del paciente?")
    search_medicine = fields.Char(string="Buscar medicamento (Clave o nombre de medicamento)",track_visibility="onchange",help="Selecciona el producto")
    presentation = fields.Char(string="Presentacion",track_visibility="onchange",help="Presentacion del medicamento")
    admon = fields.Char(string="Via de Admon",track_visibility="onchange",help="Via de administracion del medicamento")
    qty = fields.Char(string="Cantidad",track_visibility="onchange",help="Escribe la cantidad del medicamento")
    indications = fields.Char(string="Indicaciones",track_visibility="onchange",help="Escribe las indicaciones al paciente")
    duration = fields.Char(string="Duracion",track_visibility="onchange",help="Escribe la duracion en la cual debe tomar el medicamento el paciente")
    sequence = fields.Integer()






