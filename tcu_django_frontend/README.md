# 🌐 Frontend Django - Solicitud TCU

Este proyecto Django forma parte de una solución fullstack junto con un módulo Odoo. Permite a los estudiantes realizar solicitudes de Trabajo Comunal Universitario (TCU) mediante un formulario web que se comunica directamente con Odoo a través de una API REST.

---

## 🧩 Funcionalidades principales

- Formulario visual amigable para registrar solicitudes de TCU.
- Búsqueda automática del estudiante por carné desde Odoo.
- Precarga de datos personales desde Odoo.
- Consulta de periodos activos de TCU.
- Creación de la solicitud directamente en Odoo.
- Consulta del estado actual de la solicitud.
- Validación visual para estudiantes no registrados.
- Estilo minimalista y claro.


---

## ⚙️ Requisitos

- Python 3.10+
- Django 4.x
- requests (para consumir la API de Odoo)

## Instalación de dependencias:

pip install -r requirements.txt

## Activa tu entorno virtual (opcional pero recomendado):

python -m venv venv
venv\Scripts\activate  # En Windows

## Ejecuta el servidor:

python manage.py runserver

Abre tu navegador en: http://localhost:8000




🔌 Integración con Odoo
Este proyecto se comunica con los siguientes endpoints del módulo Odoo personalizado:

Método	        Endpoint	                Descripción
POST	        /get_estudiante         	Consulta datos del estudiante por carné
GET	            /get_periodo	            Lista de periodos activos de TCU
POST	        /crear_solicitud	        Envío de solicitud al sistema Odoo
POST	        /validar_estado	            Consulta del estado de la solicitud


