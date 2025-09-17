# aqui hare un merge con los datos de walmart y revisare que no contengan nulos y vacios
import pandas as pd
import numpy as np

 ## Cargo todos los datos
 
customers = pd.read_csv("Datos-walmart/customers.csv")
geolocation = pd.read_csv("Datos-walmart/geolocation.csv")
order_items = pd.read_csv("Datos-walmart/order_items.csv")
orders = pd.read_csv("Datos-walmart/orders.csv")
payments = pd.read_csv("Datos-walmart/payments.csv")
products = pd.read_csv("Datos-walmart/products.csv")
sellers = pd.read_csv("Datos-walmart/sellers.csv")


dataframes = {
    "customers": customers,
    "geolocation": geolocation,
    "order_items": order_items,
    "orders": orders,
    "payments": payments,
    "products": products,
    "sellers": sellers,
}


for name, df in dataframes.items():
    print(f"\n{name.upper()}")

    # Contar nulos (NaN)
    nulls = df.isnull().sum()

    # Contar strings vacíos ("")
    empty_strings = (df == "").sum()

    # Unir ambos resultados
    combined = pd.DataFrame({
        'Nulos (NaN)': nulls,
        'Vacíos ("")': empty_strings,
        'Total vacíos': nulls + empty_strings
    })

    print(combined[combined['Total vacíos'] > 0])  # Mostrar solo columnas con vacíos
    
    print(orders.columns)
    
    ## Elimino todas los nulos en productos

products = products.replace("", np.nan)
products = products.dropna()

## repito lo mismo para los orders que contienen nulos y vacios
orders = orders.replace("", np.nan)
orders = orders.dropna(subset=[
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date'
])

for name, df in dataframes.items():
    print(f"\n{name.upper()} HEAD:")
    print(df.head(1))

# Merge 1: orders + customers
df = orders.merge(customers, on='customer_id', how='inner')

# Merge 2: 1 + order_items
df = df.merge(order_items, on='order_id', how='inner')

# Merge 3: 2 + products
df = df.merge(products, on='product_id', how='inner')

# Merge 4: 3 + payments
df = df.merge(payments, on='order_id', how='inner')

# Merge 5: 4 + sellers
df = df.merge(sellers, on='seller_id', how='inner')

# Geolocation no tengo manera de unirlo pero tampoco lo necesito


# Ver la fecha minima y maxima para saber en que rango de fechas son mis datos 
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])  # Asegurar que la columna es datetime
print("Fecha mínima:", df["order_purchase_timestamp"].min())
print("Fecha máxima:", df["order_purchase_timestamp"].max())

# Guardar el DataFrame en un nuevo CSV
df.to_excel("DatosProcesados/walmart_final.xlsx", index=False,engine="openpyxl")