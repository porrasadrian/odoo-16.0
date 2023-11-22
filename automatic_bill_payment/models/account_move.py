from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    automatic_journal_id = fields.Many2one(comodel_name='account.journal', string="Diario para pago automatico",
                                           domain=[('type', 'in', ['bank', 'cash'])], copy=False) #Se filtran los diarios para que solo se muestren de tipo banco
                                                                                                  #y efectivo

    def action_post(self): #se manda llamar la funcion action_post del boton registrr pago
        res = super(AccountMove, self).action_post() #se aplica el super a la clase y al action_post
        if self.move_type == 'in_invoice' and self.automatic_journal_id: # Se aplican dos condiciones, si el tipo de movimiento es de proveedor y si hay un diario seleccionado
            #vas a crear todo este diccionario (los campos estan almacenados en los pagos)
            vals_payment = {
                'partner_id': self.partner_id.id,
                'journal_id': self.automatic_journal_id.id,
                'date': fields.Date.today(),
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'amount': self.amount_total,
                'currency_id': self.currency_id.id,
                'ref': self.name
            }
            payment_id = self.env['account.payment'].create(vals_payment) #aplicas un create al modelo de account.payment (modelo de pagos)
            payment_id.action_post() #ejecutas el action_post
            aml_obj = self.env['account.move.line'] #Creas una variable donde puedas entrar/almacenar datos en account.move.line (esto en relacion a la tabla de los apuntes contables)
            for move_line in self.line_ids: #Aplicas un for en la tabla de los apuntes contables
                if move_line.account_id.account_type == 'liability_payable': #Entras a la cuenta y entras al campo "tipo", si el tipo de cuenta es "Por pagar"
                    aml_obj += move_line #Entonces almacenas el resultado en la variable aml_obj
            for move_line in payment_id.line_ids: #aplicas lo mismo en la parte de pagos
                if move_line.account_id.account_type == 'liability_payable':
                    aml_obj += move_line
            aml_obj.reconcile() #al final mandas llamar la conciliacion
        return res
