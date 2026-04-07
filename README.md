# Stack DevOps de HESK + Zabbix

Este repositorio implementa una plataforma de help desk basada en HESK, con monitoreo mediante Zabbix y automatización utilizando GitHub Actions.

La solución permite:

- gestionar tickets con HESK  
- monitorear disponibilidad y performance del sistema  
- automatizar la creación de categorías mediante control de versiones (GitOps simple)  

---

## Resumen de la arquitectura

El stack está compuesto por los siguientes servicios:

- db: base de datos MySQL utilizada por HESK  
- hesk-web: aplicación HESK (PHP + Apache)  
- zabbix-db: base de datos de Zabbix  
- zabbix-server: backend de monitoreo  
- zabbix-web: interfaz web de Zabbix  
- zabbix-agent: agente de monitoreo  

Todos los servicios se comunican a través de una red Docker interna (internal-net).

---

## Flujo de ejecución

1. El usuario accede a HESK en: http://localhost:8080  
2. HESK se conecta a MySQL (db)  
3. Zabbix monitorea la aplicación desde: http://localhost:8081  
4. GitHub Actions sincroniza categorías hacia la base de datos  

---

## Estructura del repositorio

.
|-- .github/workflows/sync-categories.yml  
|-- docker-compose.yml  
|-- docker/hesk/Dockerfile  
|-- hesk/  
|-- scripts/sync_categories.py  
|-- categories.txt  
|-- .env  

---

## Prerrequisitos

- Docker  
- Docker Compose  
- Git  

---

## Variables de entorno

Archivo `.env`:

HESK_DB_NAME=hesk_db  
HESK_DB_USER=hesk_user  
HESK_DB_PASSWORD=hesk_pass  
MYSQL_ROOT_PASSWORD=root  

ZABBIX_DB_NAME=zabbix  
ZABBIX_DB_USER=zabbix  
ZABBIX_DB_PASSWORD=zabbix_pass  

---

## Instrucciones de despliegue

git clone <repo>  
cd <repo>  
docker compose up --build  

Accesos:

- HESK → http://localhost:8080  
- Zabbix → http://localhost:8081  

---

## Usuarios y claves por defecto

Base de datos:

- MySQL root: root  
- HESK DB: hesk_user / hesk_pass  
- Zabbix DB: zabbix / zabbix_pass  

Aplicación:

- HESK: se crea en la instalación inicial  
- Zabbix:  
  Usuario: Admin  
  Password: zabbix  

---

## URI monitoreada

La URL monitoreada por Zabbix es:

http://hesk-web/admin/

Se eligió porque:

- valida disponibilidad real del sistema  
- implica funcionamiento de Apache + PHP + MySQL  
- simula acceso de usuario real  

---

## Monitoreo con Zabbix

Se implementó monitoreo activo mediante Zabbix utilizando un HTTP agent.

Métricas monitoreadas:

- Código HTTP  
- Tiempo de respuesta  
- Disponibilidad del servicio  

---

## Definición de umbrales

Disponibilidad:

- HTTP debe ser 200  
- cualquier otro código → ERROR  

Timeout:

- Timeout configurado: 3 segundos  
- si la respuesta tarda más → ERROR  

Performance:

- Trigger si response time > 2 segundos  

Resumen:

- HTTP != 200 → Error  
- Timeout > 3s → Error  
- Response time > 2s → Alerta  

---

## Ejemplo de comportamiento validado

Al ejecutar:

docker stop hesk-web  
docker start hesk-web  

Se observa:

- aumento de latencia  
- disparo de trigger (>2s)  
- recuperación automática  

---

## Automatización de categorías

Las categorías se definen en:

categories.txt  

Pipeline:

1. Se hace push  
2. GitHub Actions ejecuta workflow  
3. Script Python conecta a MySQL  
4. Inserta categorías nuevas  

---

## Resultado del pipeline

En logs:

- [SKIP] → categoría ya existe  
- [CREATE] → categoría creada  

---

## Cómo disparar pipeline

Se dispara automáticamente con cambios en:

- categories.txt  
- scripts/sync_categories.py  
- .github/workflows/sync-categories.yml  

---

## Arquitectura explicada

Capa aplicación:

- HESK  
- MySQL  

Capa monitoreo:

- Zabbix Server  
- HTTP agent  

Capa automatización:

- GitHub Actions  
- Script Python  

Flujo:

Usuario → HESK → MySQL  
Zabbix → HTTP check → HESK  
GitHub → pipeline → MySQL  

---

## Supuestos adoptados

- Monitoreo mediante HTTP 
- La URL monitoreada representa el estado real del sistema  
- Runner self-hosted con acceso a la base de datos  
- Entorno local (sin TLS)  
- No hay balanceo ni alta disponibilidad  

---

## Comandos útiles

docker compose up --build  
docker compose down  
docker compose down -v  
docker compose logs -f  

---

## Resumen

La solución integra:

- HESK (help desk)  
- Zabbix (monitoreo)  
- GitHub Actions (automatización)  

Permite:

- monitoreo de disponibilidad  
- detección de degradación  
- sincronización declarativa  

---
