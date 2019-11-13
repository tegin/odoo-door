# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    oddoor_key_id = fields.Many2one(
        'oddoor.key',
        readonly=True
    )

    def generate_oddoor_key(self):
        self.ensure_one()
        if not self.oddoor_key_id and self.rfid_card_code:
            self.oddoor_key_id = self.env['oddoor.key'].create({
                'unique_virtual_key': self.rfid_card_code,
                'name': _('Key of %s') % self.display_name
            })
        return {}

    def write(self, vals):
        result = super().write(vals)
        if vals.get('rfid_card_code'):
            for record in self:
                if record.oddoor_key_id:
                    record.oddoor_key_id.unique_virtual_key = vals.get(
                        'rfid_card_code')
        return result
