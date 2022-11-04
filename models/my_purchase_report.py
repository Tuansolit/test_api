from odoo import fields, models, api
from datetime import datetime


class PurchaseReport(models.Model):
    _name = 'my.purchase.report'
    _description = 'Description'

    department_id = fields.Many2one('hr.department')
    real_cost = fields.Float(compute='_compute_real_cost')
    target_diff = fields.Float(compute='_compute_target_diff')
    cron_id = fields.Many2one('my.cron')

    @api.depends('department_id')
    def _compute_real_cost(self):
        for dep in self:
            def filter_month(f_rec):
                return f_rec.create_date.month == datetime.today().month

            opportunity_data = self.env['purchase.order'].search(
                [('state', '=', 'purchase'), ('department_id', '=', dep.department_id.id)]).filtered(
                filter_month)
            if len(opportunity_data) == 0:
                dep.real_cost = 0
            else:
                for rec in opportunity_data:
                    dep.real_cost += sum(rec.mapped('amount_total'))

    @api.depends('real_cost', 'department_id.monthly_spending_limit')
    def _compute_target_diff(self):
        for dep in self:
            dep.target_diff = dep.real_cost - dep.department_id.monthly_spending_limit
