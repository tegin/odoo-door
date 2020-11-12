# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Oddoor Iot",
    "summary": """
        Oddoor integration through iot""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "Creu Blanca,Odoo Community Association (OCA)",
    "website": "www.creublanca.es",
    "depends": ["oddoor", "iot_template"],
    "data": ["data/oddoor_template.xml", "views/iot_device_input.xml"],
}
