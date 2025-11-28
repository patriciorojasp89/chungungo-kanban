# 🦦 Chungungo Kanban // http://35.192.220.54/

Chungungo Kanban es una aplicación web tipo **tablero Kanban** (similar a Trello) para organizar tareas en tableros y columnas.  
Está pensada como proyecto final de un **bootcamp Fullstack** y como pieza de **portafolio profesional**.

Permite:

- Crear tableros personales
- Organizar tareas en columnas (To Do, Doing, Done, etc.)
- Asignar prioridad, fecha límite y etiquetas a cada tarea
- Mover tareas entre columnas con **drag & drop**, guardando los cambios en la base de datos
- Filtrar tareas por **prioridad, etiqueta y vencimiento** en tiempo real

---

## ⭐ Características principales

- Autenticación de usuarios (registro / login / logout)
- CRUD completo de:
  - Tableros
  - Columnas
  - Tareas
  - Etiquetas (tags) desde la interfaz (sin usar admin)
- Tablero Kanban:
  - Columnas en scroll horizontal
  - Tarjetas de tareas con:
    - Prioridad (Alta/Media/Baja) con colores
    - Fecha límite
    - Etiquetas con color
  - Drag & drop:
    - Mover tareas entre columnas
    - Reordenar tareas dentro de la misma columna
    - Cambios persistentes en la base de datos
- Filtros de tareas (sin recargar la página):
  - Por prioridad
  - Por etiqueta
  - Por vencimiento:
    - Vencidas
    - Para hoy
    - Futuras
    - Sin fecha
- Panel de administración de Django para gestión avanzada
- Diseño responsive con **Bootstrap 5**
- Código organizado y modular (apps, views genéricas, templates heredados)

---

## 🧰 Stack tecnológico

**Backend**

- Python 3.x
- Django 3.2
- MySQL como base de datos
- ORM de Django

**Frontend**

- HTML5, CSS3
- Bootstrap 5
- Bootstrap Icons
- JavaScript (ES6): drag & drop, filtros dinámicos

**Infraestructura / Deployment**

- Servidor en Google Cloud (Linux)
- `virtualenv` / `venv` para entorno virtual
- Configuración preparada para servir archivos estáticos

---

## 🏗️ Arquitectura general

- Proyecto Django: `chungungo`
- App principal: `boards`

Modelos principales (resumen):

- `Board`
  - `name`, `description`, `owner (User)`
- `Column`
  - `name`, `position`, `board (FK)`
- `Tag`
  - `name`, `color`, `owner (User)`
- `Task`
  - `title`, `description`
  - `priority` (H/M/L)
  - `due_date`
  - `position`
  - `column (FK)`
  - `tags (ManyToMany)`

Vistas:

- Class-based views para CRUD (ListView, CreateView, UpdateView, DeleteView)
- Vista `move_task` (API simple tipo JSON) para recibir drag & drop

Frontend:

- Templates organizados en `templates/boards/`
- `base.html` como layout principal
- `static/js/kanban.js` para drag & drop y filtros

---

## 🚀 Puesta en marcha (desarrollo local)

### 1. Clonar repositorio

```bash
git clone https://github.com/patriciorojasp89/chungungo-kanban
cd chungungo-kanban/backend
