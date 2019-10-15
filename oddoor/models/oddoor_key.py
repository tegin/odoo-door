# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import uuid


class OddoorKey(models.Model):
    _name = 'oddoor.key'
    _description = 'Oddoor Key'
    _rec_name = 'unique_virtual_key'

    name = fields.Char()
    unique_virtual_key = fields.Char(
        readonly=True, default='/',
        required=True,
    )
    expiration_date = fields.Datetime()
    group_ids = fields.Many2many(
        'oddoor.group',
        string="Groups",
    )
    action_ids = fields.One2many(
        'oddoor.key.action',
        inverse_name='key_id',
    )
    active = fields.Boolean(default=True, required=True)

    @api.model
    def _get_unique_virtual_key(self, vals):
        """Hook that can be used to define the key according to needs"""
        return uuid.uuid4()

    @api.model
    def create(self, vals):
        if vals.get('unique_virtual_key', '/') == '/':
            vals['unique_virtual_key'] = self._get_unique_virtual_key(vals)
        return super().create(vals)

    def view_actions(self):
        self.ensure_one()
        action = self.env.ref('oddoor.oddoor_key_action_act_window').read()[0]
        action['domain'] = [('key_id', '=', self.id)]
        return action

    def get_oddoor_values(self):
        result = []
        for key in self:
            result.append(key._get_oddoor_values())
        return result

    def _get_oddoor_values(self):
        return {
            'expiration_date': self.expiration_date,
            'unique_virtual_key': self.unique_virtual_key,
            'id': self.id,
        }
