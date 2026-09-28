# 📐 Rúbrica de Evaluación del Proyecto - Sistema TiendaStock

**Métrica de Puntuación Total:** 100 Puntos (o Calificación de 1.0 a 5.0)

---

## 📑 Tabla de Criterios y Ponderación

| Criterio de Evaluación | Peso (%) | Excelente (90-100%) | Sólido (70-89%) | Necesita Mejora (50-69%) | Insuficiente (<50%) |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **1. Funcionalidad del MVP** | **30%** | Permite CRUD completo de productos, alertas de stock en tiempo real y registro impecable de ventas. | La funcionalidad principal sirve, pero hay errores menores de interfaz o refresco de datos. | Falta una función clave (ej. no descuenta stock en ventas o no valida duplicados). | El proyecto no ejecuta la lógica básica de inventario. |
| **2. Calidad de Código y Arquitectura** | **25%** | Código limpio, modular, comentado, estructurado en capas (MVC/Clean Arch) y sin credenciales expuestas. | Estructura comprensible, aunque existe código duplicado o falta consistencia en estilos. | Mala separación de responsabilidades (ej. consultas a DB directamente en la vista). | Código desorganizado, imposible de mantener o propenso a fallas críticas. |
| **3. Prácticas Ágiles y Git** | **20%** | Commits frecuentes, uso correcto de ramas (`feature/*`), Pull Requests documentados y división equitativa en los 4 miembros. | Buen uso de Git, pero algunos integrantes tienen pocos commits o merged sin revisión. | Trabajo concentrado a última hora en la rama `main` sin usar ramas secundarias. | No se evidencia trabajo colaborativo en Git; todo lo subió una sola persona. |
| **4. Pruebas y Robustez** | **15%** | Manejo de excepciones elegante (HTTP 4xx/5xx), validaciones frontend/backend e inclusión de pruebas unitarias/integración. | Manejo básico de errores; la aplicación no colapsa con datos inválidos comunes. | La aplicación se rompe o muestra pantallas en blanco al ingresar datos incorrectos. | Sin validaciones de ningun tipo; falla al menor uso inesperado. |
| **5. Documentación y Presentación** | **10%** | README profesional con guía de instalación, diagramas de arquitectura/DB y presentación con demo fluida. | Documentación completa con instrucciones claras para ejecutar el proyecto en local. | README incompleto o con pasos faltantes para poder levantar el proyecto. | Sin documentación o imposibilidad de ejecutar la aplicación para evaluación. |