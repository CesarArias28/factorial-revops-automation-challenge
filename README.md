# RevOps Customer Health Alert System

An automated alerting pipeline designed to monitor B2B customer activity, detect usage drops, and trigger proactive Slack notifications for Customer Success Managers (CSMs) to mitigate churn.

---

## 1. El Problema de Negocio (Business Context)
En las empresas SaaS como **Factorial HR**, la retención de clientes es la base del crecimiento sostenible. Identificar de manera reactiva que un cliente ha dejado de usar la plataforma suele ser demasiado tarde (cuando ya ha decidido cancelar su suscripción). 

**El Reto:** Factorial necesita identificar caídas de actividad en cuentas clave para mitigar el churn de forma proactiva. 
**El Impacto:** Este sistema permite a los Account Managers actuar en la "ventana de rescate", transformando alertas de uso en llamadas de soporte proactivas, protegiendo el *MRR (Monthly Recurring Revenue)* y mejorando el *Net Revenue Retention (NRR)*.

---

## 2. La Solución Técnica (Technical Architecture)

La solución está construida sobre un stack ligero y portable de Python, diseñado para simular un pipeline de producción de RevOps:

```
[ usage_logs (SQLite) ] 
       │ (Raw SQL Query - 7-day vs 7-day comparison)
       ▼
[ health_monitor.py ] ──(If Drop >= Threshold)──► [ Slack Webhook ]
       ▲
       │ (Every Monday @ 08:00)
[ scheduler.py (Daemon) ] ◄── [ logging (error.log) ]
```

* **Base de datos SQLite:** Almacena de forma estructurada los datos históricos de uso de la plataforma.
* **Consulta SQL Optimizada:** Utiliza CTEs (*Common Table Expressions*) para realizar agrupaciones agregadas y cálculo de desviaciones directamente en el motor de base de datos, evitando sobrecarga en la memoria de Python.
* **Manejo de Errors de Producción:** Todo el flujo (conexiones, consultas y peticiones HTTP) está encapsulado en bloques de control de excepciones que registran errores detallados en un archivo `error.log` local para auditorías y debugging inmediato, manteniendo el servicio en ejecución.
* **Simulador de CRON Integrado:** Ejecuta la rutina como un demonio en segundo plano todos los lunes a las 08:00 AM usando la biblioteca `schedule`.

---

## 3. Cómo Ejecutarlo (Setup & Execution)

### Requisitos Previos
Asegúrate de tener instalado Python 3.8+ y SQLite3 en tu sistema.

### Instalación y Configuración

```bash
# 1. Clonar el repositorio e ingresar al directorio
git clone https://github.com/CesarArias28/factorial-revops-automation-challenge.git
cd factorial-revops-automation-challenge

# 2. Configurar el entorno virtual de Python
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar las dependencias de producción
pip install -r requirements.txt

# 4. Inicializar la base de datos local
sqlite3 db/revops.db < db/schema.sql
```

### Configuración del Entorno (`.env`)
Crea un archivo `.env` en la raíz del proyecto para configurar las credenciales y umbrales de alerta:
```ini
WEBHOOK_URL=https://hooks.slack.com/services/T0000/B0000/XXXXXX
DROP_THRESHOLD=40
DATABASE_PATH=db/revops.db
```

### Ejecución del Programador
Para iniciar el servicio en segundo plano (daemon) que ejecuta la alerta cada semana:
```bash
python scripts/scheduler.py
```

---

## 4. Próximos Pasos para Producción (Production Scaling Roadmap)
Como **Operations Technologist**, la escalabilidad del sistema es prioridad. Para implementar este MVP a escala empresarial en Factorial, se propone el siguiente roadmap:
1. **Migración del Data Stack:** Migrar las consultas de SQLite a un Data Warehouse como **Snowflake** u **Oracle**, integrando el cálculo de alertas en los modelos de datos existentes con **dbt**.
2. **Sincronización con CRM (HubSpot/Salesforce):** En lugar de IDs de Slack estáticos, consultar dinámicamente el dueño de la cuenta (*Account Owner*) desde la API del CRM en tiempo real.
3. **Orquestación en la Nube:** Ejecutar el script dentro de contenedores Docker orquestados por **Apache Airflow** o **AWS ECS/Lambda** para monitoreo y escalado automático.
