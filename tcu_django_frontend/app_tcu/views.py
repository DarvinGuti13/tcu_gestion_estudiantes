# app_tcu/views.py
import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.views.decorators.cache import never_cache

ODOO_BASE_URL = "http://localhost:8069"

@never_cache
def solicitud_tcu_form(request):
    context = {}

    # Limpiar mensajes anteriores
    storage = get_messages(request)
    for _ in storage:
        pass

    # Obtener periodos desde Odoo
    try:
        response = requests.get(f"{ODOO_BASE_URL}/get_periodos", timeout=10)
        if response.status_code == 200:
            context['periodos'] = response.json().get('periodos', [])
        else:
            context['periodos'] = []
    except Exception:
        context['periodos'] = []

    # Recuperar carnet desde sesión
    if 'buscar_carnet' in request.session:
        carnet = request.session.pop('buscar_carnet')
        context['carnet_actual'] = carnet

        try:
            res = requests.post(f"{ODOO_BASE_URL}/get_estudiante", json={"carnet": carnet})
            data = res.json()
            if res.status_code == 200 and 'error' not in data:
                context['datos_estudiante'] = data
            else:
                context['datos_estudiante'] = None
                messages.warning(request, "Estudiante no registrado en el sistema.")
        except Exception as e:
            context['datos_estudiante'] = None
            messages.warning(request, f"Error de conexión al buscar estudiante: {str(e)}")

    # Procesamiento del formulario
    if request.method == 'POST':
        if 'buscar' in request.POST:
            carnet = request.POST.get("carnet", "").strip()
            request.session['buscar_carnet'] = carnet
            return redirect("solicitud_tcu")

        elif 'enviar' in request.POST:
            periodo = request.POST.get("periodo", "").strip()
            periodos_disponibles = context.get('periodos', [])

            if not periodos_disponibles:
                messages.error(request, "No hay periodos disponibles para realizar la solicitud.")
                return redirect("solicitud_tcu")

            if not periodo:
                messages.warning(request, "Debe seleccionar un periodo.")
                return redirect("solicitud_tcu")

            campos_requeridos = {
                "name": request.POST.get("name"),
                "identificacion": request.POST.get("identificacion"),
                "carnet": request.POST.get("carnet"),
                "correo": request.POST.get("correo"),
                "telefono": request.POST.get("telefono"),
                "lugar_tcu": request.POST.get("lugar_tcu"),
                "encargado_estudiante": request.POST.get("encargado_estudiante"),
                "fecha_solicitud": request.POST.get("fecha_solicitud"),
                "periodo": periodo,
            }

            campos_faltantes = [campo for campo, valor in campos_requeridos.items() if not valor]
            if campos_faltantes:
                messages.error(request, f"Faltan campos requeridos: {', '.join(campos_faltantes)}")
                return redirect("solicitud_tcu")

            try:
                headers = {'Content-Type': 'application/json'}

                res = requests.post(
                    f"{ODOO_BASE_URL}/crear_solicitud",
                    data=json.dumps(campos_requeridos),
                    headers=headers
                )

                try:
                    data = res.json()
                    resultado = data.get("result", {})

                    if res.status_code == 200 and resultado.get("status") in ["creado", "actualizado"]:
                        messages.success(request, "Solicitud enviada correctamente.")
                        return redirect("solicitud_tcu")
                    else:
                        error_msg = resultado.get('error', 'Error desconocido')
                        messages.error(request, f"Error al enviar solicitud: {error_msg}")
                except Exception as e:
                    messages.error(request, f"Error al interpretar la respuesta de Odoo: {str(e)}")

            except Exception as e:
                messages.error(request, f"Error de conexión al enviar solicitud: {str(e)}")

    return render(request, 'solicitud_tcu.html', context)


def validar_estado(request):
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        try:
            res = requests.get(f"{ODOO_BASE_URL}/validar_estado/{estudiante_id}")
            if res.status_code == 200:
                data = res.json()
                if 'error' in data:
                    return render(request, "estado_resultado.html", {"error": data['error']})
                return render(request, "estado_resultado.html", {
                    "estado": data.get("estado"),
                    "observaciones": data.get("observaciones")
                })
            else:
                return render(request, "estado_resultado.html", {
                    "error": f"Error al consultar el estado. Código: {res.status_code} - Respuesta: {res.text}"})
        except Exception as e:
            return render(request, "estado_resultado.html", {"error": f"Conexión fallida: {str(e)}"})



