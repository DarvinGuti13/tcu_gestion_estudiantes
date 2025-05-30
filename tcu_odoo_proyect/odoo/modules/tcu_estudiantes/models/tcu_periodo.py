from odoo import models, fields
from datetime import datetime

class PeriodoTCU(models.Model):
    _name = 'tcu.periodo'
    _description = 'Periodo del TCU'

    def _get_year_options(self):
        current_year = datetime.now().year
        return [(str(year), str(year)) for year in range(current_year, current_year + 5)]

    name = fields.Char(string='Nombre del Periodo', required=True)
    activo = fields.Boolean(string='Activo', default=True)
    anio = fields.Selection(
        selection=[(str(year), str(year)) for year in range(2025, 2030)],
        string='Año',
        required=True
    )
    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True)
    fecha_final = fields.Date(string='Fecha Final', required=True)
