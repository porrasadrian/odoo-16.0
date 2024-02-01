# -*- coding: utf-8 -*-
{
    'name': "Dispensario Medico Jamay",
    'summary': """
        Module for the Jamay Medical Dispensary""",
    'description': """
        Module to record the clinical history and medical notes of patients treated at the dispensary
        doctor.
    """,
    'author': "Adrian Porras",
    'website': "",
    'category': 'Health',
    'version': '16.0',
    'depends': ['base','mail'],
    'data': [
        'data/secuencia_recetas_medicas.xml',
        'data/secuencia_notas_medicas.xml',
        'data/secuencia_pacientes.xml',
        'report/medical_note_paper_format.xml',
        'report/medical_note_print_button.xml',
        'report/medical_note_template.xml',
        'report/prescription.xml',
        'report/prescription_report.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/prescription.xml',
        'views/patients_view.xml',
        'views/medic_note_view.xml',
        'views/diagnostic_view.xml',
        'views/res_users_view.xml',
    ],
}
