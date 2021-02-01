# Copyright 2020 Druidoo - Iván Todorovich
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    cr.execute(
        "SELECT id, oddoor_key_id FROM hr_employee where oddoor_key_id IS NOT NULL"
    )
    for data in cr.fetchall():
        key = env["oddoor.key"].browse(data[1])
        key.write({"res_model": "hr.employee", "res_id": data[0]})
