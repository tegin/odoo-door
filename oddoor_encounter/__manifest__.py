# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Oddoor Encounter',
    'description': """
        Integration of Encounters wiht odoo door""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Creu Blanca',
    'website': 'www.creublanca.es',
    'depends': [
        'oddoor',
        'medical_administration_encounter',
    ],
    'data': [
        'data/oddoor_groups_data.xml',
        'views/medical_encounter.xml',
    ],
}
