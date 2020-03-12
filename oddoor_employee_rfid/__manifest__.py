# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Oddoor Employee Rfid',
    'summary': """
        Use employee id as a oddoor key""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca,Odoo Community Association (OCA)',
    'website': 'www.creublanca.es',
    'depends': [
        'hr_attendance_rfid',
        'oddoor',
    ],
    'data': [
        'views/hr_employee.xml',
    ],
    'demo': [
    ],
}
