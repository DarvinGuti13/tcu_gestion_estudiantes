from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
from lxml import etree

_logger = logging.getLogger(__name__)

class TCUEstudiante(models.Model):
    _name = 'tcu.estudiante'
    _description = 'Registro de Estudiantes del TCU'

    name = fields.Char(string='Nombre Completo', required=True)
    identificacion = fields.Char(string='Identificación', required=True)
    carnet = fields.Char(string='Carnet', required=True)
    correo = fields.Char(string='Correo Electrónico')
    telefono = fields.Char(string='Teléfono')

    lugar_tcu = fields.Char(string='Lugar del TCU')
    encargado_estudiante = fields.Char(string='Encargado del Estudiante')
    fecha_solicitud = fields.Date(string='Fecha de Solicitud')

    periodo_id = fields.Many2one('tcu.periodo', string='Periodo')

    estado_solicitud = fields.Selection(
        selection=[
            ('revision', 'En Revisión'),
            ('pendiente', 'Pendiente'),
            ('rechazado', 'Rechazado'),
            ('aprobado', 'Aprobado'),
        ],
        string='Estado de la Solicitud',
        default='revision'
    )

    observaciones = fields.Text(string='Observaciones')
    carta_aceptacion = fields.Binary(string='Carta de Aceptación')
    nombre_carta = fields.Char(string='Nombre del Archivo')

    edicion_manual = fields.Boolean(
        string="Edición Manual",
        default=lambda self: not self.env.context.get('default_edicion_manual', False)
    )

    mostrar_boton_envio = fields.Boolean(
        string="Mostrar botón de notificación",
        compute="_compute_mostrar_boton_envio",
        store=True
    )

    _sql_constraints = [
        ('unique_carnet', 'UNIQUE(carnet)', 'Ya existe un estudiante con este carnet.'),
        ('unique_identificacion', 'UNIQUE(identificacion)', 'Ya existe un estudiante con esta identificación.')
    ]

    @api.depends('estado_solicitud')
    def _compute_mostrar_boton_envio(self):
        for rec in self:
            rec.mostrar_boton_envio = bool(rec.id) and rec.estado_solicitud in ['aprobado', 'rechazado']

    @api.onchange('estado_solicitud')
    def _onchange_estado_solicitud(self):
        if self.estado_solicitud in ['pendiente', 'rechazado'] and not self.observaciones:
            return {
                'warning': {
                    'title': "Observaciones requeridas",
                    'message': "Debe indicar un motivo en observaciones si la solicitud está pendiente o rechazada."
                }
            }

    @api.constrains('estado_solicitud', 'observaciones')
    def _check_observaciones_estado(self):
        for record in self:
            if record.estado_solicitud in ['pendiente', 'rechazado'] and not record.observaciones:
                raise ValidationError("Debe ingresar una observación si el estado es pendiente o rechazado.")

    def enviar_correo_estado(self):
        for estudiante in self:
            _logger.info(f"[TCU] Enviando correo a {estudiante.name} - {estudiante.correo}")

            if not estudiante.id:
                raise UserError("Debe guardar el estudiante antes de enviar una notificación.")

            if not estudiante.correo:
                raise UserError("El estudiante no tiene un correo electrónico asignado.")

            template = self.env.ref('tcu_estudiantes.tcu_estudiante_estado_mail_template')
            if not template:
                raise UserError("No se encontró la plantilla de correo.")

            template.send_mail(estudiante.id, force_send=True)

    def habilitar_edicion_manual(self):
        for record in self:
            if not record.id:
                raise UserError("Debe guardar el estudiante antes de habilitar la edición manual.")
            record.edicion_manual = True

    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for field in doc.xpath("//field[@name]"):
                nombre = field.get("name")
                # Estos campos no deben tocarse (porque no deben ser readonly)
                if nombre in ['estado_solicitud', 'observaciones', 'carta_aceptacion', 'nombre_carta', 'edicion_manual']:
                    continue
                # Si no tiene ya atributos readonly definidos, se los aplicamos dinámicamente
                modifiers = field.get("modifiers")
                if not modifiers:
                    field.set("modifiers", '{"readonly": [["edicion_manual", "=", false]]}')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res














