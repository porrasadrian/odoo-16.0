# -*- coding: utf-8 -*-
# from odoo import http


# class DispensarioJamay(http.Controller):
#     @http.route('/dispensario_jamay/dispensario_jamay', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dispensario_jamay/dispensario_jamay/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dispensario_jamay.listing', {
#             'root': '/dispensario_jamay/dispensario_jamay',
#             'objects': http.request.env['dispensario_jamay.dispensario_jamay'].search([]),
#         })

#     @http.route('/dispensario_jamay/dispensario_jamay/objects/<model("dispensario_jamay.dispensario_jamay"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dispensario_jamay.object', {
#             'object': obj
#         })
