# 🏁 Definition of Done (DoD) - Criterios de Aceptación Globales

Para que cualquier **Historia de Usuario (HU)** o **Tarea** del proyecto **TiendaStock** sea considerada **"HECHA" (Done)**, debe cumplir obligatoriamente con el siguiente checklist:

---

## 🛠️ 1. Código y Calidad
- [ ] El código cumple con las guías de estilo acordadas por el equipo (Linter ejecutado sin errores).
- [ ] No existen variables no utilizadas, bloques de código comentado ni `console.log` / `print` de depuración.
- [ ] No hay credenciales, contraseñas o llaves secretas escritas directamente en el código fuente (se utilizan archivos `.env`).

## 🗄️ 2. Base de Datos e Integración
- [ ] Los cambios en esquemas de Base de Datos cuentan con su correspondiente script de migración o SQL documentado.
- [ ] Las consultas están optimizadas y no generan cuellos de botella al filtrar productos o calcular totales de venta.

## 🧪 3. Pruebas y Validación
- [ ] La funcionalidad se probó localmente en diferentes escenarios (casos de éxito y datos de entrada erróneos).
- [ ] Las rutas de la API fueron probadas con Postman/Insomnia y retornan los códigos de estado HTTP correctos.
- [ ] Todos los formularios del frontend validan los datos de entrada antes de realizar peticiones al servidor.

## 🔀 4. Control de Versiones (Git)
- [ ] El código se subió a una rama con nombre descriptivo (`feature/HU-01-registro-productos`).
- [ ] Se creó un **Pull Request (PR)** hacia la rama `develop` con una explicación clara de los cambios realizados.
- [ ] El PR fue revisado y aprobado por al menos **un (1) compañero de equipo** diferente al autor.
- [ ] Se resolvieron todos los conflictos de fusión (merge conflicts) antes del cierre.

## 📑 5. Documentación y Despliegue
- [ ] La documentación de la API / Endpoints (Swagger, Postman collection o README) fue actualizada si se agregaron o cambiaron rutas.
- [ ] La funcionalidad desplegada funciona correctamente en el entorno de desarrollo local o producción.
- [ ] La Historia de Usuario fue verificada frente a sus criterios de aceptación en presencia de al menos 2 miembros del equipo.