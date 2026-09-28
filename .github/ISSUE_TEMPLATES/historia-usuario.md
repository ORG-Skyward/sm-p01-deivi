# 📋 Historias de Usuario - Sistema de Gestión de Inventarios "TiendaStock"

**Proyecto:** Sistema Inteligente de Gestión de Inventarios y Ventas para Tiendas Locales  
**Equipo:** 4 Integrantes  
**Metodología:** Scrum / Kanban  

---

## 📌 Epica 1: Gestión de Productos e Inventario

### HU-01: Registro y Catálogo de Productos
- **Como:** Tendero / Administrador de la tienda
- **Quiero:** Registrar productos con su nombre, categoría, precio de compra, precio de venta y stock inicial
- **Para:** Tener visibilidad digital y controlada de las existencias de mi tienda

#### Criterios de Aceptación:
1. **Dado** que el tendero está en el formulario de creación, **cuando** ingresa todos los datos obligatorios (nombre, código de barras/SKU, precio, stock) y guarda, **entonces** el producto se almacena correctamente y aparece en la lista principal.
2. **Dado** que un tendero intenta registrar un código de barras existente, **cuando** envía el formulario, **entonces** el sistema muestra un mensaje de error impidiendo duplicados.
3. **Dado** que el tendero olvida ingresar un campo obligatorio, **cuando** da clic en "Guardar", **entonces** el sistema resalta los campos faltantes.

- **Estimación:** 5 Puntos de Historia (SP)
- **Responsables sugeridos:** Integrante 1 (Frontend) + Integrante 2 (Backend)

---

### HU-02: Alertas de Stock Mínimo y Reabastecimiento
- **Como:** Tendero / Administrador
- **Quiero:** Configurar un umbral de stock mínimo para cada producto y recibir alertas visuales
- **Para:** Evitar quedarme sin mercancía clave antes de realizar el pedido al proveedor

#### Criterios de Aceptación:
1. **Dado** que un producto llega o cae por debajo del stock mínimo configurado, **cuando** el tendero entra al Dashboard, **entonces** el producto se resalta en un panel de "Alertas de Reabastecimiento" en rojo/amarillo.
2. **Dado** que la tienda se queda sin stock de un producto (stock = 0), **cuando** se consulta el inventario, **entonces** el sistema lo marca explícitamente como "Agotado".

- **Estimación:** 3 Puntos de Historia (SP)
- **Responsables sugeridos:** Integrante 1 (Frontend) + Integrante 3 (DB)

---

## 📌 Épica 2: Registro de Ventas Rápidas

### HU-03: Registro de Ventas y Descuento Automático
- **Como:** Cajero / Tendero
- **Quiero:** Registrar las ventas diarias seleccionando o escaneando productos rápidamente
- **Para:** Actualizar el inventario en tiempo real sin cálculos manuales

#### Criterios de Aceptación:
1. **Dado** que el usuario selecciona 2 unidades del "Producto A" y confirma la venta, **cuando** la transacción finaliza, **entonces** el stock del "Producto A" se reduce automáticamente en 2 unidades.
2. **Dado** que un producto no tiene stock disponible (stock = 0), **cuando** el usuario intenta agregarlo al carrito de venta, **entonces** el sistema impide la acción y advierte la falta de inventario.
3. **Dado** que la venta se completa con éxito, **cuando** se presiona "Finalizar", **entonces** se genera un resumen del total cobrado y el cambio a entregar.

- **Estimación:** 8 Puntos de Historia (SP)
- **Responsables sugeridos:** Integrante 1 (Frontend) + Integrante 2 (Backend)

---

## 📌 Épica 3: Reportes y Métrica Básica

### HU-04: Dashboard de Ventas Diarias y Productos Más Vendidos
- **Como:** Dueño de la tienda
- **Quiero:** Visualizar un resumen diario de ventas totales, ganancias estimadas y productos top
- **Para:** Tomar decisiones de compra basadas en datos reales de ventas

#### Criterios de Aceptación:
1. **Dado** que el dueño accede a la vista de reportes, **cuando** selecciona el filtro "Hoy", **entonces** visualiza el total de ingresos cobrados y la cantidad de transacciones del día.
2. **Dado** que se registran ventas acumuladas, **cuando** se renderiza la gráfica/lista del Dashboard, **entonces** muestra el Top 5 de productos más vendidos del mes.

- **Estimación:** 5 Puntos de Historia (SP)
- **Responsables sugeridos:** Integrante 4 (QA/Fullstack) + Integrante 3 (DB/Backend)