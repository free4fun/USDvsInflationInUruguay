import requests
import pandas as pd
import locale

# Establecer el locale en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# URLs de los archivos
url_ipc = "https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/SERIES%20Y%20OTROS/IPC/Base%20Octubre%202022=100/IPC%20gral%20y%20variaciones_base%202022.xls"
url_cotizacion = "https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/SERIES%20Y%20OTROS/Cotización%20monedas/Cotización%20monedas.xlsx"

# Descargar y guardar el archivo IPC
response_ipc = requests.get(url_ipc)
file_path_ipc = "IPC_gral_y_variaciones_base_2022.xls"
with open(file_path_ipc, 'wb') as file:
    file.write(response_ipc.content)

# Descargar y guardar el archivo de cotización de monedas
response_cotizacion = requests.get(url_cotizacion)
file_path_cotizacion = "Cotizacion_monedas.xlsx"
with open(file_path_cotizacion, 'wb') as file:
    file.write(response_cotizacion.content)

# Leer el archivo XLS de IPC con pandas
xls_ipc = pd.ExcelFile(file_path_ipc)
df_ipc = pd.read_excel(xls_ipc, sheet_name=xls_ipc.sheet_names[0])

# Ajusta el acceso a las columnas si es necesario
fecha_col_ipc = df_ipc.columns[0]
ipc_col = df_ipc.columns[1]

# Convertir la columna de fechas a tipo datetime especificando el formato
df_ipc[fecha_col_ipc] = pd.to_datetime(df_ipc[fecha_col_ipc], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Asegurarse de que la columna de IPC es de tipo float
df_ipc[ipc_col] = pd.to_numeric(df_ipc[ipc_col], errors='coerce')

# Eliminar filas que no se pudieron convertir a números o fechas
df_ipc = df_ipc.dropna(subset=[fecha_col_ipc, ipc_col])

# Leer el archivo XLSX de cotización de monedas con pandas
xls_cotizacion = pd.ExcelFile(file_path_cotizacion)
df_cotizacion = pd.read_excel(xls_cotizacion, sheet_name=xls_cotizacion.sheet_names[0])

# Asegurarse de que las columnas de fecha están en el formato correcto
fecha_col_cotizacion = df_cotizacion.columns[0]
dolar_ebrou_venta_col = df_cotizacion.columns[3]  # Cuarto campo: "Dólar eBROU Venta"

# Convertir la columna de fechas a tipo datetime
df_cotizacion[fecha_col_cotizacion] = pd.to_datetime(df_cotizacion[fecha_col_cotizacion], errors='coerce', dayfirst=True)

# Convertir la columna de dólar eBROU Venta a numérico
df_cotizacion[dolar_ebrou_venta_col] = pd.to_numeric(df_cotizacion[dolar_ebrou_venta_col], errors='coerce')

# Eliminar filas que no se pudieron convertir a fechas o números
df_cotizacion = df_cotizacion.dropna(subset=[fecha_col_cotizacion, dolar_ebrou_venta_col])

# Calcular el cambio mensual del dólar y compararlo con la inflación
meses_con_aumento_dolar_mayor = []

for i in range(1, 61):
    # Fecha del mes actual
    fecha_mes_actual = df_ipc.iloc[-i][fecha_col_ipc]
    
    # Fecha del mes anterior
    fecha_mes_anterior = fecha_mes_actual - pd.DateOffset(months=1)
    
    # Calcular el promedio del dólar eBROU Venta del mes actual y anterior
    cotizaciones_mes_actual = df_cotizacion[(df_cotizacion[fecha_col_cotizacion] >= fecha_mes_anterior) & (df_cotizacion[fecha_col_cotizacion] < fecha_mes_actual)]
    promedio_dolar_mes_actual = cotizaciones_mes_actual[dolar_ebrou_venta_col].mean()
    
    cotizaciones_mes_anterior = df_cotizacion[(df_cotizacion[fecha_col_cotizacion] >= fecha_mes_anterior - pd.DateOffset(months=1)) & (df_cotizacion[fecha_col_cotizacion] < fecha_mes_anterior)]
    promedio_dolar_mes_anterior = cotizaciones_mes_anterior[dolar_ebrou_venta_col].mean()
    
    # Calcular el cambio porcentual del dólar
    if promedio_dolar_mes_anterior > 0:
        cambio_dolar = ((promedio_dolar_mes_actual - promedio_dolar_mes_anterior) / promedio_dolar_mes_anterior) * 100
    else:
        cambio_dolar = None
    
    # Calcular la inflación del mes actual
    IPC_MesAnterior = df_ipc.iloc[-i-1][ipc_col]
    IPC_MesActual = df_ipc.iloc[-i][ipc_col]
    inflacion_mensual = ((IPC_MesActual - IPC_MesAnterior) / IPC_MesAnterior) * 100
    
    # Comparar el cambio del dólar con la inflación
    if cambio_dolar is not None and cambio_dolar > inflacion_mensual:
        meses_con_aumento_dolar_mayor.append(fecha_mes_actual.strftime('%B %Y'))
    
    # Imprimir detalles para cada mes
    print(f"Mes: {fecha_mes_actual.strftime('%B %Y')}")
    print(f"Cambio del dólar: {cambio_dolar:.2f}%")
    print(f"Inflación: {inflacion_mensual:.2f}%")
    print()

# Imprimir los meses donde el aumento del dólar fue mayor que la inflación
print("Meses donde el aumento del dólar fue mayor que la inflación:")
for mes in meses_con_aumento_dolar_mayor:
    print(mes)
