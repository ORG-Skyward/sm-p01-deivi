# 🚀 Guía de Aprendizaje - Sprint 1: Fundamentos y MVP de Inventario

**Proyecto:** TiendaStock - Gestión de Inventarios  
**Duración del Sprint:** 2 Semanas  
**Objetivo del Sprint:** Construir el núcleo del sistema (Creación de base de datos, API REST básica de Productos e interfaz UI para listar y crear inventario).

---

## 🧠 1. Conceptos Clave que el Equipo Debe Dominar

### 🛠️ Control de Versiones y Flujo de Trabajo
- **Git Flow:** Ramas `main`, `develop`, y ramas de características `feature/nombre-tarea`.
- **Pull Requests (PR):** Ningún código entra a `develop` sin la aprobación de al menos 1 compañero de equipo. hola

### 🗄️ Base de Datos y Modelo Entidad-Relación
- Principios de diseño de tablas: `Productos`, `Categorías`, `Proveedores`, `Ventas`, `DetalleVentas`.
- Integridad referencial (Claves primarias y foráneas).

### 🌐 Desarrollo de API REST (Backend)
- Métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`).
- Respuestas en formato JSON y códigos de estado HTTP (200 OK, 201 Created, 400 Bad Request, 404 Not Found).

### 🎨 Interfaz de Usuario (Frontend)
- Componentes reutilizables (Tablas, Modales de registro, Formularios con validación).
- Consumo de API mediante cliente HTTP (`fetch` / `axios`).

---

## 🗺️ 2. Plan Paso a Paso para las 4 Personas

### 🟢 Paso 1: Configuración Inicial (Días 1 - 2) — *Todo el equipo*
1. Crear el repositorio en GitHub/GitLab.
2. Definir la estructura del proyecto (Monorepo o repositorios separados Backend/Frontend).
3. Acordar la pila tecnológica (Ejemplo: React/Vue en Frontend, Node.js/Python en Backend, PostgreSQL/MySQL/MongoDB en DB).

### 🟡 Paso 2: Modelo de Datos y Servidor Base (Días 3 - 5)
- **Integrante 3 (DB/DevOps):** Diseñar el script SQL o esquema ODM para las tablas `Productos` y `Categorias`.
- **Integrante 2 (Backend):** Crear el servidor base y conectar a la DB. Implementar endpoints `GET /api/productos` y `POST /api/productos`.

### 🟠 Paso 3: Construcción de la Interfaz (Días 5 - 8)
- **Integrante 1 (Frontend):** Diseñar la pantalla de inventario con tabla de productos y modal para "Agregar Producto".
- **Integrante 4 (QA/Fullstack):** Implementar la lógica de validación de formularios en el cliente y manejo de alertas de error.

### 🔴 Paso 4: Integración y Pruebas (Días 9 - 10)
1. Conectar la interfaz del Frontend con la API REST del Backend.
2. Probar el flujo completo de creación y consulta de productos.
3. Preparar la Demo del Sprint 1.

---

## 💡 3. Distribución Recomendada de Roles

| Integrante | Rol Principal | Tareas Clave Sprint 1 |
| :--- | :--- | :--- |
| **Persona 1** | Frontend Lead | Creación de componentes UI (Tabla de productos, Formularios). |
| **Persona 2** | Backend Lead | Endpoints de API REST, controladores y lógica de negocio. |
| **Persona 3** | DB & DevOps | Diseño de Base de Datos, migraciones y entorno local (Docker/Scripts). |
| **Persona 4** | QA & Integración | Validaciones, pruebas de la API (Postman), redacción de DoD y Demo. |