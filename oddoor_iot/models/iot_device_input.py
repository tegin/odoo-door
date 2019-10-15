# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IotDeviceInput(models.Model):
    _inherit = 'iot.device.input'

    lock_id = fields.Many2one(
        'oddoor.lock'
    )

    def call_lock(self, value):
        result = self.lock_id.check_access_unique_virtual_key(value)
        return {
            'access_granted': result
        }

    def call_lock_values(self, value):
        return {'keys': self.lock_id.get_virtual_keys()}
