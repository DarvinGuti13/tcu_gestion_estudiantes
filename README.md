# 🎓 Sistema de Gestión de Estudiantes TCU – Fullstack (Django + Odoo)

Este repositorio contiene una solución fullstack para la gestión de solicitudes del Trabajo Comunal Universitario (TCU), desarrollada como parte de una prueba técnica. El sistema combina:

- 📦 Un **módulo Odoo 17** para administrar la información oficial de los estudiantes y solicitudes.
- 🌐 Una **aplicación web Django** que permite a los estudiantes realizar sus solicitudes de forma interactiva.



---

## 🚀 Tecnologías utilizadas

| Herramienta  | Uso                                     |
|--------------|------------------------------------------|
| **Python 3.10** | Backend de Django y Odoo              |
| **Django 4.x**  | Aplicación web frontend               |
| **Odoo 17**     | Backend ERP y lógica de negocio       |
| **PostgreSQL**  | Base de datos (en Odoo)               |
| **SQLite**      | Base de datos local (en Django)       |
| **REST API**    | Comunicación entre Django y Odoo      |

---

## 🔌 Comunicación Django ↔ Odoo

Django se comunica con Odoo usando peticiones HTTP a los siguientes endpoints públicos:

| Método | Endpoint             | Función                                |
|--------|----------------------|----------------------------------------|
| POST   | `/get_estudiante`    | Buscar datos del estudiante por carné |
| GET    | `/get_periodo`       | Obtener periodos activos              |
| POST   | `/crear_solicitud`   | Crear nueva solicitud                 |
| POST   | `/validar_estado`    | Consultar estado de la solicitud      |

---

## ⚙️ Instrucciones generales de instalación

Cada subproyecto tiene su propio entorno virtual y archivo `README.md` con instrucciones específicas. A continuación una vista general:



