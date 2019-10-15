# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OddoorKeyAction(models.Model):

    _name = 'oddoor.key.action'
    _description = 'Oddoor Key Action'
    _order = 'create_date DESC'

    key_id = fields.Many2one('oddoor.key')
    unique_virtual_key = fields.Char()
    lock_id = fields.Many2one('oddoor.lock', required=True)
    result = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], required=True)
