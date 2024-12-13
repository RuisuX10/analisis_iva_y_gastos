# Proyecto de Integración de Datos: Gastos e IVA

## Descripción

Este proyecto tiene como objetivo integrar y comparar dos archivos de Excel que contienen datos relacionados con gastos e IVA. Los archivos provienen de dos fuentes diferentes:

- **gastos.xlsx**: contiene información sobre los gastos realizados por la empresa.
- **iva-compras.xlsx**: contiene detalles sobre las compras y el IVA correspondiente.

El proyecto utiliza la librería `pandas` para cargar, procesar y comparar los datos de ambos archivos, con el fin de crear un archivo de salida que refleje la relación entre estos dos conjuntos de datos.

## Objetivos

1. **Cargar los archivos de Excel**: Leer los datos de las hojas de Excel correspondientes a los gastos e IVA.
2. **Renombrar las columnas**: Asegurar que los DataFrames de ambos archivos tengan nombres de columnas consistentes para facilitar la comparación.
3. **Limpiar los datos**: Asegurar que las columnas de los comprobantes tengan un formato consistente (eliminación de espacios y guiones).
4. **Verificar fechas y comprobar existencia de comprobantes**: Añadir columnas que indiquen si un comprobante de gastos está relacionado con un comprobante de IVA y viceversa.
5. **Generar un archivo de salida**: Guardar los resultados en un nuevo archivo Excel que contenga los datos procesados y las nuevas columnas.

## Pasos del Proyecto

1. **Carga de los DataFrames**:
   - El archivo `gastos.xlsx` es cargado en un DataFrame (`df1`) con la hoja `Sheet1`, comenzando desde la fila 10 (para omitir encabezados innecesarios).
   - El archivo `iva-compras.xlsx` es cargado en otro DataFrame (`df2`) con la hoja `Sheet1`, comenzando desde la fila 7.
   
2. **Renombrado de columnas**:
   - Se asignan nombres de columnas consistentes en ambos DataFrames para facilitar su análisis y comparación.

3. **Conversión de la columna 'Comprobante' a tipo cadena**:
   - Se asegura que la columna `Comprobante` de ambos DataFrames sea del tipo `str` (cadena de texto) para facilitar la comparación entre ambos archivos.

4. **Normalización de los valores en la columna 'Comprobante'**:
   - Se eliminan espacios y guiones de los valores en la columna `Comprobante` para asegurar que las comparaciones sean precisas.

5. **Verificación de fechas válidas**:
   - Se implementa una función que verifica si las fechas en el campo `Fecha` son válidas. Si una fecha es válida, se realiza la comparación entre los comprobantes de gastos e IVA.

6. **Creación de nuevas columnas**:
   - En `df1` (gastos), se crea una nueva columna llamada `en iva`, que indica si el comprobante de ese gasto tiene una correspondencia en el archivo de IVA.
   - En `df2` (IVA), se crea una columna llamada `en gastos`, que indica si el comprobante de IVA tiene una correspondencia en el archivo de gastos.

7. **Guardar los resultados en un nuevo archivo Excel**:
   - Los DataFrames modificados se guardan en un nuevo archivo Excel llamado `gastos_iva.xlsx`, con dos hojas: una para los datos de gastos y otra para los datos de IVA.

## Código

```python
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

# Función para verificar si un valor es una fecha válida
def es_fecha_valida(fecha):
    try:
        pd.to_datetime(fecha, errors='raise')
        return True
    except:
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
