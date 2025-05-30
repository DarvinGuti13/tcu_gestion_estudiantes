from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class TCUEstudianteAPI(http.Controller):

    @http.route('/get_estudiante', type='http', auth='public', methods=['POST'], csrf=False)
    def get_estudiante(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
            carnet = data.get('carnet')
            estudiante = request.env['tcu.estudiante'].sudo().search([('carnet', '=', carnet)], limit=1)

            if estudiante:
                return Response(
                    json.dumps({
                        'nombre': estudiante.name,
                        'correo': estudiante.correo,
                        'telefono': estudiante.telefono,
                        'identificacion': estudiante.identificacion,
                        'estado_solicitud': estudiante.estado_solicitud,
                    }),
                    content_type='application/json'
                )

            return Response(
                json.dumps({'error': 'Estudiante no encontrado'}),
                status=404,
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'error': f'Error interno: {str(e)}'}),
                status=500,
                content_type='application/json'
            )

    @http.route('/crear_solicitud', type='json', auth='public', methods=['POST'], csrf=False)
    def crear_solicitud(self):
        try:
            kwargs = json.loads(request.httprequest.data)

            carnet = kwargs.get('carnet')
            if not carnet:
                raise ValueError("Carnet no recibido o es vacío")

            periodo_raw = kwargs.get('periodo')
            periodo_id = int(periodo_raw) if periodo_raw and str(periodo_raw).isdigit() else False

            estudiante = request.env['tcu.estudiante'].sudo().search([('carnet', '=', carnet)], limit=1)

            if estudiante:
                estudiante.sudo().write({
                    'lugar_tcu': kwargs.get('lugar_tcu'),
                    'encargado_estudiante': kwargs.get('encargado_estudiante'),
                    'fecha_solicitud': kwargs.get('fecha_solicitud'),
                    'estado_solicitud': 'revision',
                    'periodo_id': periodo_id,
                })
                return {'status': 'actualizado', 'id': estudiante.id}
            else:
                name = kwargs.get('name')
                correo = kwargs.get('correo')
                telefono = kwargs.get('telefono')
                identificacion = kwargs.get('identificacion')

                if not all([name, correo, telefono, identificacion]):
                    raise ValueError("Faltan datos requeridos para crear nuevo estudiante")

                nuevo_estudiante = request.env['tcu.estudiante'].sudo().create({
                    'name': name,
                    'identificacion': identificacion,
                    'carnet': carnet,
                    'correo': correo,
                    'telefono': telefono,
                    'lugar_tcu': kwargs.get('lugar_tcu'),
                    'encargado_estudiante': kwargs.get('encargado_estudiante'),
                    'fecha_solicitud': kwargs.get('fecha_solicitud'),
                    'estado_solicitud': 'revision',
                    'periodo_id': periodo_id,
                })
                return {'status': 'creado', 'id': nuevo_estudiante.id}

        except Exception as e:
            _logger.error("[TCU] Error en /crear_solicitud: %s", str(e))
            return {'error': f'Error al procesar la solicitud: {str(e)}'}

    @http.route('/get_periodos', type='http', auth='public', methods=['GET'], csrf=False)
    def get_periodos(self):
        try:
            periodos = request.env['tcu.periodo'].sudo().search([('activo', '=', True)])

            data = []
            for periodo in periodos:
                data.append({
                    'id': periodo.id,
                    'nombre': periodo.name,
                    'anio': periodo.anio,
                    'fecha_inicio': str(periodo.fecha_inicio),
                    'fecha_final': str(periodo.fecha_final),
                })

            return Response(
                json.dumps({'periodos': data}),
                content_type='application/json'
            )
        except Exception as e:
            _logger.error("[TCU] Error en /get_periodos: %s", str(e))
            return Response(
                json.dumps({'error': f'Error interno: {str(e)}'}),
                content_type='application/json',
                status=500
            )

    @http.route('/validar_estado/<int:estudiante_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def validar_estado(self, estudiante_id):
        estudiante = request.env['tcu.estudiante'].sudo().browse(estudiante_id)
        if estudiante.exists():
            return Response(
                json.dumps({
                    'estado': estudiante.estado_solicitud,
                    'observaciones': estudiante.observaciones or ''
                }),
                content_type='application/json'
            )
        return Response(
            json.dumps({'error': 'Solicitud no encontrada'}),
            content_type='application/json'
        )






