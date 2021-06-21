# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import uuid

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OddoorKey(models.Model):
    _name = "oddoor.key"
    _description = "Oddoor Key"
    _rec_name = "unique_virtual_key"

    name = fields.Char()
    unique_virtual_key = fields.Char(
        readonly=True, default="/", required=True,
    )
    expiration_date = fields.Datetime()
    group_ids = fields.Many2many("oddoor.group", string="Groups")
    action_ids = fields.One2many("oddoor.key.action", inverse_name="key_id")
    active = fields.Boolean(default=True)
    res_id = fields.Integer(index=True)
    res_model = fields.Char(index=True)

    _sql_constraints = [
        (
            "unique_virtual_key_uniq",
            "UNIQUE(unique_virtual_key)",
            "Key must be unique",
        ),
    ]

    @api.model
    def _get_unique_virtual_key(self, vals):
        """Hook that can be used to define the key according to needs"""
        return uuid.uuid4()

    @api.model
    def create(self, vals):
        if vals.get("unique_virtual_key", "/") == "/":
            vals["unique_virtual_key"] = self._get_unique_virtual_key(vals)
        return super().create(vals)

    def view_actions(self):
        self.ensure_one()
        action = self.env.ref("oddoor.oddoor_key_action_act_window").read()[0]
        action["domain"] = [("key_id", "=", self.id)]
        return action

    def get_oddoor_values(self):
        result = []
        for key in self:
            result.append(key._get_oddoor_values())
        return result

    def _get_oddoor_values(self):
        return {
            "expiration_date": self.expiration_date,
            "unique_virtual_key": self.unique_virtual_key,
            "id": self.id,
        }

    @api.model
    def _get_unique_key_models(self):
        return []

    @api.constrains("res_model", "res_id")
    def _constrain_key_model(self):
        unique_models = self._get_unique_key_models()
        for record in self:
            if record.res_model not in unique_models:
                continue
            if self.with_context(active_test=False).search(
                [
                    ("id", "!=", record.id),
                    ("res_id", "=", record.res_id),
                    ("res_model", "=", record.res_model),
                ],
                limit=1,
            ):
                raise ValidationError(
                    _("Only one key can be assigned to this model")
                )


class OddoorKeyMixin(models.AbstractModel):
    _name = "oddoor.key.mixin"
    _description = "Mixin for relation between record and Oddoor Keys"

    oddoor_key_ids = fields.One2many(
        "oddoor.key",
        inverse_name="res_id",
        domain=lambda r: [("res_model", "=", r._name)],
    )
    oddoor_key_count = fields.Integer(compute="_compute_oddoor_key_count")

    @api.depends("oddoor_key_ids")
    def _compute_oddoor_key_count(self):
        for record in self:
            record.oddoor_key_count = len(record.oddoor_key_ids)

    def action_view_oddoor_key(self):
        self.ensure_one()
        action = self.env.ref("oddoor.oddoor_key_act_window").read()[0]
        action["domain"] = [
            ("res_id", "=", self.id),
            ("res_model", "=", self._name),
        ]
        action["context"] = {
            "default_res_id": self.id,
            "default_res_model": self._name,
        }
        return action
