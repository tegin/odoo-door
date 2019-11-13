# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from uuid import uuid4


class IotTemplate(models.Model):
    _inherit = 'iot.template'

    def auto_generate_key(self, serial):
        result = super().auto_generate_key(serial)
        if self == self.env.ref('oddoor_iot.oddoor_template'):
            lock = self.env['oddoor.lock'].create({
                'name': serial
            })
            result.update({
                'key_serial_1': uuid4(),
                'passphrase_1': uuid4(),
                'key_serial_2': uuid4(),
                'passphrase_2': uuid4(),
                'lock_id': lock.id,
            })
        return result
