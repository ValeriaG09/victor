import pandas as pd
import glob 
import matplotlib.pyplot as plt

#1.Buscar datos y leer archivos
## df = dataframe

df_medellin = pd.read_csv('datos/sucursal_medellin.csv')
#print(df_medellin)

df_bogota = pd.read_excel('datos/sucursal_bogota.xlsx')
#print(df_bogota)

# Para leer:
archivos_csv = glob.glob("datos/sucursal_*.csv")
print(f"Archivos_csv {archivos_csv}")

archivos_xlsx = glob.glob("datos/sucursal_*.xlsx")
print(f"archivos_xlsx {archivos_xlsx}")

lista_dataframes = []

for archivo in archivos_csv:
    df = pd.read_csv(archivo)
    lista_dataframes.append(df)
    print(f"Archivo {archivo} - {len(df)} filas leido correctamente")
    
for archivo in archivos_xlsx:
    df = pd.read_excel(archivo)
    lista_dataframes.append(df)
    print(f"Archivo {archivo} - {len(df)} filas leido correctamente")

for i, df in enumerate(lista_dataframes):
    if 'Fecha_Venta' in df.columns:
        lista_dataframes[i] = df.rename(columns={
            'Fecha_Venta': 'fecha',
            'Producto': 'producto',
            'Categoria': 'categoria',
            'Cant': 'cantidad',
            'Valor_Unitario': 'precio_unitario',
            'Vendedor': 'vendedor',
            'Pago': 'metodo_pago'
        })
        
df_consolidado = pd.concat(lista_dataframes,ignore_index=True)

# Para guardar:
df_consolidado.to_excel("resultados/consolidado_limpio.xlsx", index=False)

# Análisis del producto más vendido
print("--- Análisis de producto más vendido ---")
print(df_consolidado['producto'].value_counts())

# Gráficos
plt.figure(figsize=(10,6))
df_consolidado['categoria'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Ventas por Categoría')
plt.tight_layout()
plt.savefig("resultados/grafico_categoria.png")

plt.figure(figsize=(10,6))
df_consolidado['vendedor'].value_counts().plot(kind='bar', color='lightgreen')
plt.title('Ventas por Vendedor')
plt.tight_layout()
plt.savefig("resultados/grafico_vendedor.png")