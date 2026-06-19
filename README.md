# RevOps Customer Health Alert Automation / Automatización de Alertas de Salud de Clientes

A lightweight, automated alerting pipeline designed to monitor B2B customer activity, identify sudden drops in product usage, and trigger proactive Slack notifications for Customer Success / Account Managers. Developed as a technical proposal for the **Operations Technologist - RevOps** position at Factorial HR.

Una solución ligera y automatizada para monitorear la actividad de clientes B2B, identificar caídas repentinas en el uso del producto e iniciar notificaciones proactivas en Slack para los Account Managers (AM). Desarrollado como propuesta técnica para la posición de **Operations Technologist - RevOps** en Factorial HR.

---

## 🇺🇸 English Version

### Purpose & Business Impact
In SaaS businesses like Factorial, customer retention and expansion are vital. A sudden drop in active users or interactions is the strongest leading indicator of churn risk. This script acts as an early warning system:
- **Reduces Churn:** Alerts Account Managers *before* a customer decides to cancel their subscription.
- **Speeds Up Response Time:** Eliminates manual data audits by pushing alerts directly to Slack with teammate tagging.
- **Empowers Customer Success:** Arms team members with clear percentages of usage reduction to guide their outreach conversations.

### Key Features
1. **Raw SQL Query Optimization:** Uses a single, efficient CTE (Common Table Expression) query to compute weekly differences, avoiding memory overhead.
2. **Dynamic Relative Windows:** Compares the last 7 days of activity against the previous 7 days (days 7-13) to account for daily seasonality.
3. **Slack Tagging & Integration:** Automatically formats Slack mentions utilizing the Account Manager's Slack User ID (`<am_slack_id>`) for direct accountability.
4. **Environment Configuration:** Securely separates credentials and thresholds (`.env`) from core business logic.

---

### Project Structure
- `/db/schema.sql`: Contains the database DDL for SQLite tables (`clients` and `usage_logs`).
- `/scripts/health_monitor.py`: The main automation script containing the ETL pipeline, logic, and Slack alert dispatcher.
- `/.env`: Environment configuration file (Webhook URL, Drop Threshold, Database Path).

### Database Schema
- **`clients`**: Stores customer profiles, including names and their designated Account Manager's Slack ID.
- **`usage_logs`**: Stores daily activity logs mapped to clients.

---

### Setup & Usage

#### 1. Initialize Database & Seed Data
You can create the SQLite database and seed it using Python or SQLite CLI.
```bash
sqlite3 db/revops.db < db/schema.sql
```

#### 2. Configure Environment
Rename or edit the `.env` file at the root:
```ini
WEBHOOK_URL=https://hooks.slack.com/services/T000.../B000.../XXXX...
DROP_THRESHOLD=40
DATABASE_PATH=db/revops.db
```

#### 3. Run the Monitor Script
Make sure to install the `requests` library before running the script:
```bash
pip install requests
python scripts/health_monitor.py
```

---

## 🇪🇸 Versión en Español

### Propósito e Impacto de Negocio
En modelos SaaS B2B como el de Factorial, la retención y la satisfacción del cliente son fundamentales. Una caída repentina en el volumen de uso es el predictor más fuerte de riesgo de cancelación (churn). Este script actúa como un sistema de alerta temprana:
- **Reduce el Churn:** Alerta a los Account Managers *antes* de que el cliente decida dar de baja su suscripción.
- **Optimiza Tiempos de Respuesta:** Elimina las auditorías de datos manuales enviando alertas instantáneas a Slack con menciones directas.
- **Habilita el Éxito del Cliente:** Proporciona datos precisos (porcentajes de caída) para guiar la conversación de contacto.

### Características Clave
1. **Optimización con SQL Puro:** Emplea una consulta estructurada con CTEs (Common Table Expressions) para calcular la diferencia de uso semanal directamente en base de datos.
2. **Ventanas Relativas Dinámicas:** Compara los últimos 7 días con los 7 días anteriores (días 7 al 13) para neutralizar la estacionalidad diaria.
3. **Menciones Directas en Slack:** Genera notificaciones enriquecidas etiquetando al AM correspondiente utilizando su Slack User ID.
4. **Parámetros en .env:** Aísla de forma segura credenciales, umbrales y rutas de base de datos del código del negocio.

---

### Configuración y Uso

#### 1. Inicializar Base de Datos
Crea la estructura de tablas SQLite ejecutando el esquema:
```bash
sqlite3 db/revops.db < db/schema.sql
```

#### 2. Configurar Variables de Entorno
Edita las variables del archivo `.env`:
```ini
WEBHOOK_URL=https://hooks.slack.com/services/T000.../B000.../XXXX...
DROP_THRESHOLD=40
DATABASE_PATH=db/revops.db
```

#### 3. Ejecutar el Monitor
Asegúrate de instalar la biblioteca de dependencias `requests`:
```bash
pip install requests
python scripts/health_monitor.py
```
