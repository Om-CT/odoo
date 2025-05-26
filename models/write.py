from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        if 'x_custom_note' in vals:
            print(f"Updating custom note to: {vals['x_custom_note']}")

        result = super().write(vals)

        print("Write method called successfully.")

        return result
