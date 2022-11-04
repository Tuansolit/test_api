import odoo
import logging
import json

_logger = logging.getLogger(__name__)
from odoo.http import request, Response


class MyAPI(odoo.http.Controller):
    @odoo.http.route('/foo', auth='public')
    def foo_handler(self):
        return "Welcome to 'foo' API!"

    @odoo.http.route('/bar', auth='none', type='http', methods=['POST'], csrf=False)
    def bar_handler(self, token, month=None, year=None):
        if not all([token, month, year]):
            data = json.dumps({'error': 'thieu du lieu'})
        elif token != 'odooneverdie':
            data = json.dumps({'error': 'loi token'})
        else:
            rec = request.env['my.cron'].sudo().search([('month', '=', int(month)), ('year', '=', int(year))], limit=1)

            data = json.dumps({
                "sale": [
                    {
                        "sale_team_name": x.sale_team_id.name,
                        "real_revenue": x.real_revenue,
                        "diff": x.sale_diff
                    } for x in rec.sale_report_ids
                ],
                "purchase": [
                    {
                        "department_name": x.department_id.name,
                        "real_cost": x.real_cost,
                        "diff": x.target_diff
                    } for x in rec.purchase_report_ids
                ]
            })
        return request.make_response(data, headers=[('Content-Type', 'application/json')])
