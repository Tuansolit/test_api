from odoo import fields, models, api
from datetime import datetime


class MyCron(models.Model):
    _name = 'my.cron'
    _description = 'Description'

    sale_report_ids = fields.One2many('my.sale.report', 'cron_id')
    purchase_report_ids = fields.One2many('my.purchase.report', 'cron_id')
    month = fields.Integer(default=fields.Date.today().month)
    year = fields.Integer(default=fields.Date.today().year)

    def _cron_send_mail(self):
        email_values = {
            'email_cc': False,
            'auto_delete': True,
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
            'email_from': 'silerspirit2001@gmail.com',
            'email_to': 'silerspirit2001@gmail.com',
        }
        report = self.create(
            {'sale_report_ids': [(5, 0)] + [(0, 0, {'sale_team_id': member.id}) for member in
                                            self.env['crm.team'].search([])],
             'purchase_report_ids': [(5, 0)] + [(0, 0, {'department_id': member.id}) for member in
                                                self.env['hr.department'].search([])]})
        mail_template = self.env.ref('test_api.mail_template_cron_email_report')
        mail_template.send_mail(report.id, force_send=True, raise_exception=True, email_values=email_values)
