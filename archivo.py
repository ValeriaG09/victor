import pandas as pd
import glob 

#1.Buscar datos y leer archivos
## df = dataframe

df_medellin = pd.read_csv('sucursal_medellin.csv')
#print(df_medellin)

df_bogota = pd.read_excel('sucursal_bogota.xlsx')
#print(df_bogota)

#print(df_medellin.columns)
#print(df_bogota.columns)

archivos_csv = glob.glob("*.csv")
print(f"Archivos_csv {archivos_csv}")

archivos_xlsx = glob.glob("*.xlsx")
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

#2.Guardar en una lista 