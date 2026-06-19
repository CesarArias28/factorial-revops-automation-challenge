# RevOps Customer Health Alert

## 1. El Problema de Negocio
Factorial necesita identificar caídas de actividad en cuentas clave para mitigar el churn de forma proactiva.

## 2. La Solución Técnica
Automatización en Python. Base de datos SQLite (logs de uso). Integración HTTP/Webhook (Slack/Discord). Manejo de errores con logs locales y simulación de CRON.

## 3. Cómo Ejecutarlo
```bash
# 1. Clonar el repositorio e ingresar al directorio
git clone https://github.com/CesarArias28/RevOps_SlackAlerts.git
cd RevOps_SlackAlerts

# 2. Configurar entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar variables de entorno (.env)
# Crear archivo .env en la raíz con el formato:
# WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../X...
# DROP_THRESHOLD=40
# DATABASE_PATH=db/revops.db

# 4. Inicializar base de datos (si aplica)
sqlite3 db/revops.db < db/schema.sql

# 5. Ejecutar planificador de tareas (CRON daemon)
python scripts/scheduler.py
```
