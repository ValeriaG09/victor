# ============================================
# AUTOMATIZACIÓN - Bot de Ventas
# Este script vigila la carpeta de datos y cuando detecta 
# un archivo nuevo, procesa todo automáticamente:
# lee, consolida, limpia, analiza y guarda un registro del proceso
# ============================================
import sys
import time
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Asegurar codificación utf-8 en salida estándar para compatibilidad con Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Directorio de datos (soporta data/ o datos/)
ruta_datos = "data/" if os.path.exists("data") else "datos/"
archivos_vistos = set(os.listdir(ruta_datos))


def procesar_todo(archivo_nuevo):
    """
    Lee todos los archivos de sucursales, los consolida, 
    limpia duplicados, genera un gráfico de ventas por categoría,
    calcula métricas de negocio y guarda un registro (log) del proceso.
    """
    archivos_csv = glob.glob(f"{ruta_datos}sucursal_*.csv")
    archivos_xlsx = glob.glob(f"{ruta_datos}sucursal_*.xlsx")
    lista_informes = []
    
    for archivo in archivos_csv:
        lista_informes.append(pd.read_csv(archivo))
    for archivo in archivos_xlsx:
        lista_informes.append(pd.read_excel(archivo, engine='openpyxl'))
    
    if not lista_informes:
        print("No se encontraron archivos de ventas para procesar.")
        return

    # Estandarizar columnas
    for i, df in enumerate(lista_informes):
        if 'Fecha_Venta' in df.columns:
            lista_informes[i] = df.rename(columns={
                'Fecha_Venta': 'fecha',
                'Producto': 'producto',
                'Categoria': 'categoria',
                'Cant': 'cantidad',
                'Valor_Unitario': 'precio_unitario',
                'Vendedor': 'vendedor',
                'Pago': 'metodo_pago'
            })
    
    df_consolidado = pd.concat(lista_informes, ignore_index=True)
    df_consolidado = df_consolidado.drop_duplicates()
    
    os.makedirs("resultados", exist_ok=True)
    df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)
    
    # Generar gráfico de ventas por categoría
    ventas_categoria = df_consolidado.groupby('categoria')['precio_unitario'].sum()
    plt.figure(figsize=(10, 6))
    ventas_categoria.plot(kind='bar', color='skyblue', title='Ventas por Categoría')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ylabel('Ventas totales (COP)')
    plt.xlabel('Categoría')
    plt.tight_layout()
    plt.savefig("resultados/grafico_categoria.png")
    plt.close()
    
    # ============================================
    # BANNER + RESUMEN EJECUTIVO (4 MÉTRICAS DE NEGOCIO)
    # 1. Total de registros procesados
    # 2. Total de ventas acumuladas
    # 3. Producto más vendido (con value_counts())
    # 4. Promedio de venta por transacción (con mean())
    # ============================================
    total_registros = len(df_consolidado)
    total_ventas = df_consolidado['precio_unitario'].sum()
    
    # Métrica nueva 1: Producto más vendido usando value_counts()
    conteo_productos = df_consolidado['producto'].value_counts()
    producto_mas_vendido = conteo_productos.idxmax()
    unidades_producto_mas_vendido = conteo_productos.max()
    
    # Métrica nueva 2: Promedio de venta por transacción usando mean()
    promedio_venta = df_consolidado['precio_unitario'].mean()
    
    # Banner y Resumen Ejecutivo en consola
    print("\n" + "=" * 60)
    print("        BANNER: SISTEMA AUTOMATIZADO DE REPORTES")
    print("=" * 60)
    print(f"[*] Archivo(s) nuevo(s) detectado(s): {archivo_nuevo}")
    print("-" * 60)
    print("RESUMEN EJECUTIVO DE NEGOCIO:")
    print(f"  1. Total de registros procesados       : {total_registros}")
    print(f"  2. Total de ventas consolidadas        : ${total_ventas:,.2f} COP")
    print(f"  3. Producto más vendido                : {producto_mas_vendido} ({unidades_producto_mas_vendido} transacciones)")
    print(f"  4. Promedio de venta por transacción   : ${promedio_venta:,.2f} COP")
    print("=" * 60)
    
    # Guardar en log_automatizacion.txt con encoding="utf-8"
    with open("resultados/log_automatizacion.txt", "a", encoding="utf-8") as f:
        f.write("============================================================\n")
        f.write("RESUMEN EJECUTIVO - BOT DE VENTAS\n")
        f.write(f"Proceso ejecutado                  : {pd.Timestamp.now()}\n")
        f.write(f"Archivo(s) detectado(s)            : {archivo_nuevo}\n")
        f.write(f"Total de registros procesados      : {total_registros}\n")
        f.write(f"Total de ventas consolidadas       : ${total_ventas:,.2f} COP\n")
        f.write(f"Producto más vendido               : {producto_mas_vendido} ({unidades_producto_mas_vendido} transacciones)\n")
        f.write(f"Promedio de venta por transacción  : ${promedio_venta:,.2f} COP\n")
        f.write("============================================================\n\n")
    
    print("[+] Proceso completado exitosamente - Archivos actualizados en resultados/\n")


if __name__ == "__main__":
    print("=" * 60)
    print("BOT DE VENTAS ACTIVO - VIGILANDO CARPETA DE DATOS")
    print(f"Monitoreando: '{ruta_datos}' (Ctrl+C para detener)")
    print("=" * 60)
    
    while True:
        archivos_actuales = set(os.listdir(ruta_datos))
        archivos_nuevos = archivos_actuales - archivos_vistos
        
        if archivos_nuevos:
            print(f"\n[ALERTA] Nuevo archivo detectado: {archivos_nuevos}")
            procesar_todo(archivos_nuevos)
            archivos_vistos = archivos_actuales
        
        time.sleep(3)