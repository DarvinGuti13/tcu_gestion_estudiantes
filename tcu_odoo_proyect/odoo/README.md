# 🎓 Módulo Odoo: Gestión de Estudiantes TCU

Este módulo fue desarrollado como parte de una prueba técnica para la gestión y control de solicitudes de estudiantes del Trabajo Comunal Universitario (TCU). Permite registrar estudiantes, asignar periodos, gestionar solicitudes y conectarse con una aplicación externa desarrollada en Django.

---

## 🧩 Características principales

- Registro completo de estudiantes con campos personales y académicos.
- Gestión de periodos del TCU con fechas y año como selección tipo radio.
- Control del estado de la solicitud: En revisión, Pendiente, Rechazado, Aprobado.
- Validación automática de observaciones cuando el estado es pendiente o rechazado.
- Soporte para carga de documentos (ej. carta de aceptación).
- Integración con sistema externo vía API REST.
- Envío de notificaciones por correo electrónico - Parcial
- Funcionalidad de edición manual controlada (solo después de guardar el registro). - Parcial


## 🚀 Requisitos

- Python 3.10 o superior
- PostgreSQL 13+
- Odoo 17
- pip, virtualenv o pipenv

---
## ⚙️ Instalación del módulo Odoo

1. Instala Odoo 17 en tu máquina (no incluido en este repositorio)


## ⚙️ Instalación del entorno Odoo

1. **Ubica este proyecto localmente:**

   cd tcu_odoo_proyect/odoo


## Crea entorno virtual e instala dependencias (opcional):

python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt

## Ejecuta el servidor Odoo
python odoo-bin -r db-user -w dbpassword --addons-path=addons,modules -d db-name

activa el modo desarrollador
Ve a **Aplicaciones** → actualiza la lista de apps
Busca `TCU Estudiantes` y haz clic en **Instalar**
