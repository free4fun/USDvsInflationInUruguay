import requests
import pandas as pd
import matplotlib.pyplot as plt
import locale

# Set locale to Spanish
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# URLs for the files
url_ipc = "https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/SERIES%20Y%20OTROS/IPC/Base%20Octubre%202022=100/IPC%20gral%20y%20variaciones_base%202022.xls"
url_cotizacion = "https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/SERIES%20Y%20OTROS/Cotización%20monedas/Cotización%20monedas.xlsx"

# Download and save the IPC file
response_ipc = requests.get(url_ipc)
file_path_ipc = "IPC_gral_y_variaciones_base_2022.xls"
with open(file_path_ipc, 'wb') as file:
    file.write(response_ipc.content)

# Download and save the currency exchange file
response_cotizacion = requests.get(url_cotizacion)
file_path_cotizacion = "Cotizacion_monedas.xlsx"
with open(file_path_cotizacion, 'wb') as file:
    file.write(response_cotizacion.content)

# Read the IPC XLS file with pandas
xls_ipc = pd.ExcelFile(file_path_ipc)
df_ipc = pd.read_excel(xls_ipc, sheet_name=xls_ipc.sheet_names[0])

# Adjust column access if necessary
fecha_col_ipc = df_ipc.columns[0]
ipc_col = df_ipc.columns[1]

# Convert date column to datetime specifying the format
df_ipc[fecha_col_ipc] = pd.to_datetime(df_ipc[fecha_col_ipc], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Ensure IPC column is of type float
df_ipc[ipc_col] = pd.to_numeric(df_ipc[ipc_col], errors='coerce')

# Drop rows that could not be converted to numbers or dates
df_ipc = df_ipc.dropna(subset=[fecha_col_ipc, ipc_col])

# Read the currency exchange XLSX file with pandas
xls_cotizacion = pd.ExcelFile(file_path_cotizacion)
df_cotizacion = pd.read_excel(xls_cotizacion, sheet_name=xls_cotizacion.sheet_names[0])

# Ensure date columns are in the correct format
fecha_col_cotizacion = df_cotizacion.columns[0]
dolar_ebrou_compra_col = df_cotizacion.columns[2]  # Third field: "Dólar eBROU Compra"

# Convert date column to datetime
df_cotizacion[fecha_col_cotizacion] = pd.to_datetime(df_cotizacion[fecha_col_cotizacion], errors='coerce', dayfirst=True)

# Convert the "Dólar eBROU Compra" column to numeric
df_cotizacion[dolar_ebrou_compra_col] = pd.to_numeric(df_cotizacion[dolar_ebrou_compra_col], errors='coerce')

# Drop rows that could not be converted to dates or numbers
df_cotizacion = df_cotizacion.dropna(subset=[fecha_col_cotizacion, dolar_ebrou_compra_col])

# Calculate monthly dollar change and compare it to inflation
months = []
dollar_changes = []
inflations = []
colors = []

for i in range(1, 61):
    # Current month's date
    current_month_date = df_ipc.iloc[-i][fecha_col_ipc]

    # Previous month's date
    previous_month_date = current_month_date - pd.DateOffset(months=1)

    # Calculate the average "Dólar eBROU Compra" for the current and previous months
    current_month_rates = df_cotizacion[(df_cotizacion[fecha_col_cotizacion] >= previous_month_date) & (df_cotizacion[fecha_col_cotizacion] < current_month_date)]
    average_dollar_current_month = current_month_rates[dolar_ebrou_compra_col].mean()

    previous_month_rates = df_cotizacion[(df_cotizacion[fecha_col_cotizacion] >= previous_month_date - pd.DateOffset(months=1)) & (df_cotizacion[fecha_col_cotizacion] < previous_month_date)]
    average_dollar_previous_month = previous_month_rates[dolar_ebrou_compra_col].mean()

    # Calculate the percentage change in dollar
    if average_dollar_previous_month > 0:
        dollar_change = ((average_dollar_current_month - average_dollar_previous_month) / average_dollar_previous_month) * 100
    else:
        dollar_change = 0

    # Calculate the inflation for the current month
    previous_month_ipc = df_ipc.iloc[-i-1][ipc_col]
    current_month_ipc = df_ipc.iloc[-i][ipc_col]
    monthly_inflation = ((current_month_ipc - previous_month_ipc) / previous_month_ipc) * 100

    # Add to lists
    months.append(current_month_date.strftime('%b %Y'))
    dollar_changes.append(dollar_change)
    inflations.append(monthly_inflation)

    # Determine the color of the bar
    if dollar_change > monthly_inflation:
        colors.append('green')
    elif dollar_change < monthly_inflation:
        colors.append('red')
    else:
        colors.append('white')

# Reverse lists so the oldest is on the left
months.reverse()
dollar_changes.reverse()
colors.reverse()

# Create the bar chart
plt.figure(figsize=(12, 8))
plt.bar(months, dollar_changes, color=colors)
plt.xticks(rotation=90, color='#D3D3D3')  # Light gray color for labels
plt.yticks(color='#D3D3D3')  # Light gray color for Y-axis labels
plt.title('Monthly Dollar Change vs. Inflation (Last 5 Years)', color='#D3D3D3')
plt.xlabel('Month', color='#D3D3D3')
plt.ylabel('Change (%)', color='#D3D3D3')

# Set a nearly black background
plt.gca().set_facecolor('#222222')
plt.gcf().set_facecolor('#222222')

# Change the color of the axis borders
plt.gca().spines['bottom'].set_color('#D3D3D3')
plt.gca().spines['left'].set_color('#D3D3D3')

# Save the chart as a PNG file
plt.tight_layout()
plt.savefig('cambio_dolar_vs_inflacion.png', dpi=300, bbox_inches='tight', facecolor='#222222')

# Close the plot to avoid displaying it
plt.close()
