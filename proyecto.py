import pandas as pd

# Cargar los DataFrames
df1 = pd.read_excel("gastos.xlsx", sheet_name="Sheet1", header=10)
df2 = pd.read_excel("iva-compras.xlsx", sheet_name="Sheet1", header=7)

# Renombrar las columnas para asegurar que coincidan
df1.columns = ['Fecha', 'Comprobante', 'Proveedor - Concepto', 'Neto s/imp.', 'Neto c/imp.', 'Total c/IVA']
df2.columns = ['Fecha', 'Comprobante', 'Proveedor', 'Tipo/Nro.Doc.', 'Neto', 'IVA', 'Sin créd.fis.', 'No Gravado', 'Ret./Per.', 'Exentas', 'Total']

# Verificar las primeras filas de ambos DataFrames
print("Primeras filas de df1:", df1.head())
print("Primeras filas de df2:", df2.head())

# Asegurarse de que las columnas 'Comprobante' estén como cadenas
df1['Comprobante'] = df1['Comprobante'].astype(str)
df2['Comprobante'] = df2['Comprobante'].astype(str)

# Normalizar los valores de 'Comprobante' para comparar correctamente
df1['Comprobante'] = df1['Comprobante'].str.replace(" ", "").str.replace("-", "")
df2['Comprobante'] = df2['Comprobante'].str.replace(" ", "").str.replace("-", "")

# Eliminar filas de df1 donde la columna 'Fecha' contenga la cadena 'Total del concepto:'
df1 = df1[~df1['Fecha'].str.contains("Total del concepto:", na=False)]

# Función para verificar si un valor es una fecha válida
def es_fecha_valida(fecha):
    try:
        # Intentar convertir a fecha
        pd.to_datetime(fecha, errors='raise')
        return True
    except:
        # Si no es posible convertir, es un texto u otro valor no válido
        return False

# Crear la columna 'en iva' en df1 solo si 'Fecha' es una fecha válida
df1['en iva'] = df1.apply(
    lambda row: 'Sí' if es_fecha_valida(row['Fecha']) and row['Comprobante'] in df2['Comprobante'].values else ('No' if es_fecha_valida(row['Fecha']) else ''),
    axis=1
)

# Crear la columna 'en gastos' en df2
df2['en gastos'] = df2['Comprobante'].apply(lambda x: 'Sí' if x in df1['Comprobante'].values else 'No')

# Guardar los DataFrames modificados de nuevo en el Excel utilizando openpyxl
with pd.ExcelWriter("gastos_iva.xlsx", engine='openpyxl') as writer:
    df1.to_excel(writer, sheet_name="gastos", index=False)
    df2.to_excel(writer, sheet_name="iva", index=False)

print("Archivos modificados y guardados correctamente.")
