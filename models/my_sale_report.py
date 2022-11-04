from odoo import fields, models, api
from datetime import datetime


class SaleReport(models.Model):
    _name = 'my.sale.report'
    _description = 'Description'

    sale_team_id = fields.Many2one('crm.team')
    real_revenue = fields.Float(compute='_compute_real_revenue')
    sale_diff = fields.Float(compute='_compute_sale_diff')
    cron_id = fields.Many2one('my.cron')

    @api.depends('sale_team_id')
    def _compute_real_revenue(self):
        for team in self:
            def filter_month(f_rec):
                return f_rec.create_date.month == datetime.today().month

            opportunity_data = self.env['crm.lead'].search(
                [('type', '=', 'opportunity'), ('team_id', '=', team.sale_team_id.id)]).filtered(
                filter_month)
            if len(opportunity_data) == 0:
                team.real_revenue = 0
            else:
                for rec in opportunity_data:
                    team.real_revenue += sum(rec.order_ids.mapped('amount_total'))

    @api.depends('real_revenue', 'sale_team_id.invoiced_target')
    def _compute_sale_diff(self):
        for team in self:
            team.sale_diff = team.real_revenue - team.sale_team_id.invoiced_target
