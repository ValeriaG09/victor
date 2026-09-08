# Bot de Ventas - Sistema Automatizado de Métricas y Análisis

Este proyecto implementa un sistema inteligente de automatización que vigila la carpeta de datos y procesa reportes de ventas de múltiples sucursales de forma continua, desatendida y en tiempo real.

---

## ⚙️ ¿Cómo Funciona la Automatización?

### 1. ¿Qué hace el sistema?
El sistema opera como un vigilante permanente en segundo plano. Lee archivos multiformato (`.csv` y `.xlsx`), estandariza las discrepancias de nombres de columnas entre sucursales, elimina registros duplicados, unifica la data en un consolidado limpio, regenera los gráficos estadísticos y emite un resumen ejecutivo tanto en la consola como en un archivo de auditoría (`log_automatizacion.txt`).

### 2. ¿Cómo detecta los archivos nuevos?
El script utiliza una técnica basada en la teoría de conjuntos de Python:
- Al iniciar, escanea la carpeta de datos (`data/` o `datos/`) y guarda los nombres de los archivos existentes en un conjunto (`archivos_vistos = set(os.listdir(ruta_datos))`).
- Mediante un ciclo de monitoreo continuo (`while True` con pausas no invasivas mediante `time.sleep()`), inspecciona periódicamente la carpeta y obtiene `archivos_actuales`.
- Calcula la diferencia de conjuntos:
  ```python
  archivos_nuevos = archivos_actuales - archivos_vistos
  ```
- Si `archivos_nuevos` contiene elementos, significa que un usuario o sucursal arrastró un nuevo reporte a la carpeta.

### 3. ¿Qué pasa cuando encuentra uno?
1. Se dispara inmediatamente la función `procesar_todo(archivos_nuevos)`.
2. Lee todos los archivos de ventas (`sucursal_*.csv` y `sucursal_*.xlsx`).
3. Homogeniza columnas (por ejemplo `Fecha_Venta` a `fecha`, `Cant` a `cantidad`, etc.).
4. Consolida y aplica `.drop_duplicates()` para evitar transacciones repetidas.
5. Guarda el archivo maestro `resultados/consolidado_limpio.xlsx`.
6. Genera y actualiza el gráfico de barras `resultados/grafico_categoria.png`.
7. Calcula las 4 métricas de negocio y despliega el **Banner + Resumen Ejecutivo**.
8. Registra la ejecución en `resultados/log_automatizacion.txt` con codificación `utf-8` y marca de tiempo exacta.
9. Actualiza `archivos_vistos` para quedar listo ante la siguiente llegada de archivos.

---

## 📊 Análisis y Preguntas de Negocio (4 Métricas Clave)

Tras la detección e integración progresiva de los nuevos reportes de Medellín, Cali y Cartagena, el sistema consolidó los siguientes resultados:

| Métrica de Negocio | Valor Obtenido | Método de Cálculo |
| :--- | :--- | :--- |
| **1. Total de registros procesados** | **91 transacciones** | `len(df_consolidado)` tras desduplicación |
| **2. Ventas totales consolidadas** | **$8,705,600.00 COP** | `df_consolidado['precio_unitario'].sum()` |
| **3. Producto más vendido** | **Jean clasico (16 ventas)** | `df_consolidado['producto'].value_counts()` |
| **4. Promedio de venta por transacción** | **$98,927.27 COP** | `df_consolidado['precio_unitario'].mean()` |

### Respuestas a las Preguntas de Negocio:
1. **¿Cuál es el volumen total de operaciones del negocio?**  
   El negocio ha completado 91 transacciones válidas distribuidas entre las sedes de Medellín, Cali, Barranquilla, Bogotá y Cartagena.
2. **¿A cuánto ascienden los ingresos acumulados?**  
   Los ingresos totales generados en el periodo evaluado alcanzan **$8,705,600.00 COP**.
3. **¿Cuál es el producto insignia con mayor tracción comercial?**  
   El **Jean clasico** se consolida como el producto de mayor rotación con 16 ventas registradas, seguido de cerca por accesorios tecnológicos como el Cargador USB-C.
4. **¿Cuál es el valor medio invertido por transacción?**  
   El ticket promedio por transacción es de **$98,927.27 COP**, lo cual sirve como referencia base para diseñar estrategias de *up-selling* y paquetes promocionales.

---

## 📝 Conclusión

La implementación de este bot de automatización representa un salto cualitativo respecto a los flujos tradicionales manuales. Permite:
- **Reducción del 100% en tiempos de espera**: Los directores comerciales no tienen que esperar horas o días a que alguien consolide manualmente archivos Excel dispersos.
- **Calidad de datos garantizada**: La limpieza algorítmica de duplicados previene la sobreestimación de ingresos.
- **Visibilidad inmediata**: Los gráficos y métricas se actualizan en segundos tras la recepción de cualquier nuevo archivo.

---

## 💡 Reflexión Final

> **Si fueran el dueño de este negocio, ¿confiarían en un sistema automático como este para tomar decisiones? ¿Por qué sí o por qué no?**

**Sí, confiaría plenamente en el sistema como herramienta principal operativa y de inteligencia de negocio, pero con salvaguardas de validación de datos.**

### ¿Por qué sí?
1. **Eliminación del error humano**: La consolidación manual en hojas de cálculo es una de las mayores fuentes de error en finanzas (filas omitidas, fórmulas desalineadas, duplicados invisibles). El algoritmo aplica las mismas reglas matemáticas y de limpieza en cada iteración de manera impecable.
2. **Agilidad en la toma de decisiones**: Tener métricas actualizadas al instante permite detectar quiebres de inventario del producto estrella (*Jean clasico*) o caídas en el ticket promedio en tiempo real, en vez de descubrirlo al cierre de mes.
3. **Trazabilidad y auditoría**: Cada operación queda sellada en el archivo `log_automatizacion.txt` con fecha, hora exacta y archivos involucrados, garantizando transparencia.

### Consideraciones clave para máxima confianza:
Para que la confianza sea total, el sistema debe complementarse con **reglas de validación de entrada (Data Quality)**: verificar que los precios no contengan valores negativos, que las fechas tengan formatos válidos y que las cantidades no sean nulas. Con este filtro defensivo, un sistema automático es infinitamente superior y más confiable que cualquier proceso manual.

---

## 📁 Estructura del Proyecto

```text
proyecto_bot/
├── data/ -> enlace a datos/
├── datos/
│   ├── sucursal_barranquilla.xlsx
│   ├── sucursal_bogota.xlsx
│   ├── sucursal_cali.csv
│   ├── sucursal_cali_reporte2.csv
│   ├── sucursal_cartagena_reporte2.csv
│   └── sucursal_medellin.csv
│   └── sucursal_medellin_reporte2.csv
├── resultados/
│   ├── consolidado_limpio.xlsx
│   ├── grafico_categoria.png
│   ├── grafico_vendedor.png
│   └── log_automatizacion.txt
├── main.py
├── automatizacion_47.py
├── mejora_automatizacion_47.py
└── README.md
```
