# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Oddoor",
    "summary": """
        Odoo Lock System for Doors""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "www.creublanca.es",
    "depends": ["base"],
    "data": [
        "wizards/oddoor_key_wizard.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/oddoor_key_action.xml",
        "views/oddoor_menu.xml",
        "views/oddoor_group.xml",
        "views/oddoor_key.xml",
        "views/oddoor_lock.xml",
        "views/res_partner.xml",
    ],
    "demo": [
        "security/security_demo.xml",
        "demo/oddoor_group_demo.xml",
        "demo/oddoor_lock_demo.xml",
        "demo/oddoor_key_demo.xml",
    ],
}
