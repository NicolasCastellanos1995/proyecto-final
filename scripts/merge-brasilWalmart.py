# Aqui voy a hacer un merge de datos brasil y walmart y descartar las columas que no me parecen indispensables.
# tambien revisare que el tipo de datos sea correcto para luego trabajar con ellos

import pandas as pd

# cargo los sets

orders = pd.read_excel("DatosProcesados/walmart_final.xlsx")
hdi = pd.read_excel("DatosProcesados/datosBrasil_final.xlsx")

# selecciono las columnas que me parecen interesantes para trabajar de cada set
orders = orders[[
    "order_purchase_timestamp", "customer_state", "payment_value", "freight_value",
    "payment_type", "payment_installments", "price", "product category",
    "order_approved_at","order_delivered_carrier_date","order_delivered_customer_date",
]]

# de datos brasil solo tomares los valores de 2017 porque son contemporaneos a los otros datos
hdi = hdi[[
    "UF", "HDI 2017", "HDI Education 2017", "HDI Wealth 2017", "HDI Health 2017",
    "Population", "Demographic Density", "GDP", "GDP rate", "Poverty",
    "Region", "Latitude", "Longitude"
]]

# merge

df_datosBrasil = pd.merge(
    orders,
    hdi,
    left_on="customer_state",
    right_on="UF",
    how="inner"   # coincidencia
)

## correccion del tipo de dato segun el tipo de variable   
# Date/Fecha
df_datosBrasil['order_purchase_timestamp'] = pd.to_datetime(df_datosBrasil['order_purchase_timestamp'])
df_datosBrasil['order_approved_at'] = pd.to_datetime(df_datosBrasil['order_approved_at'])
df_datosBrasil['order_delivered_carrier_date'] = pd.to_datetime(df_datosBrasil['order_delivered_carrier_date'])
df_datosBrasil['order_delivered_customer_date'] = pd.to_datetime(df_datosBrasil['order_delivered_customer_date'])

# numericos
df_datosBrasil['payment_value'] = df_datosBrasil['payment_value'].astype(float)
df_datosBrasil['freight_value'] = df_datosBrasil['freight_value'].astype(float)
df_datosBrasil['payment_installments'] = df_datosBrasil['payment_installments'].astype(int)
df_datosBrasil['price'] = df_datosBrasil['price'].astype(float)

# variables categoricas
df_datosBrasil['customer_state'] = df_datosBrasil['customer_state'].astype('category')
df_datosBrasil['payment_type'] = df_datosBrasil['payment_type'].astype('category')
df_datosBrasil['product category'] = df_datosBrasil['product category'].astype('category')
df_datosBrasil['UF'] = df_datosBrasil['UF'].astype('category')
df_datosBrasil['Region'] = df_datosBrasil['Region'].astype('category')

# variables economicas
for col in [
    'HDI 2017', 'HDI Education 2017', 'HDI Wealth 2017', 'HDI Health 2017',
    'Population', 'Demographic Density', 'GDP', 'GDP rate', 'Poverty',
    'Latitude', 'Longitude'
]:
    df_datosBrasil[col] = pd.to_numeric(df_datosBrasil[col], errors='coerce')
    
print(df_datosBrasil.dtypes)

# cambio la categoria product category a product_category 

df_datosBrasil = df_datosBrasil.rename(columns={'product category': 'product_category'})

# elimino filas duplicadas

df_datosBrasil = df_datosBrasil.drop_duplicates()

# checkeo de valores imposibles 
check = {
    "payment_value_neg": (df_datosBrasil['payment_value'] < 0).sum(), 
    "freight_value_neg": (df_datosBrasil['freight_value'] < 0).sum(),
    "price_neg": (df_datosBrasil['price'] < 0).sum(),
    "installments_min1": (df_datosBrasil['payment_installments'] < 1).sum() if 'payment_installments' in orders.columns else 0,
}
print(check)

# elimino los que me dieron fuera de rango 

eliminar = df_datosBrasil["payment_installments"].notna() & (df_datosBrasil["payment_installments"] < 1)
df_datosBrasil.drop(index=df_datosBrasil.index[eliminar], inplace=True)


## como tengo muchos productos con categorias similares, voy a agruparlos en categorias nuevas.
df_datosBrasil["product_category"] = (
    df_datosBrasil["product_category"]
    .astype(str)
    .str.strip()
    .str.lower()
)
map_categorias_macro = {
    # automotive permanece igual
    # sport leisure permanece igual
    
    #  art
    "art": "arts",
    "arts and crafts": "arts",
    "cds music dvds": "arts",
    "blu ray dvds": "arts",
    "song": "arts",           
   
     
    # categoria fashion
    "bags accessories": "fashion",
    "fashion bags and accessories": "fashion",
    "fashion calcados": "fashion",
    "fashion men's clothing": "fashion",
    "fashion women's clothing": "fashion",
    "fashion children's clothing": "fashion",
    "fashion underwear and beach fashion": "fashion",
    "fashion sport": "fashion",
    
    # home
    "furniture": "home",
    "furniture decoration": "home",
    "furniture kitchen service area dinner and garden": "home",
    "furniture office": "home",
    "room furniture": "home",
    "citte and uphack furniture": "home",
    "house comfort": "home",
    "house comfort 2": "home",
    "house pastals oven and cafe": "home",
    "bed table bath": "home",
    "housewares": "home",
    "home appliances": "home",
    "casa construcao": "home",
    "garden tools": "home",
    
    # construcction
    "construction tools": "construction",
    "construction tools construction": "construction",
    "construction tools garden": "construction",
    "construction tools illumination": "construction",
    "construction tools tools": "construction",
    "signalization and safety": "construction",
    "construction security tools": "construction",
    
    # electronics
    "electronics": "electronics",
    "electrostile": "electronics",
    "electrices 2": "electronics",
    "image import tablets": "electronics",
    "cine photo": "electronics",
    "computers": "electronics",
    "pc gamer": "electronics",
    "pcs": "electronics",
    "fixed telephony": "electronics",
    "telephony": "electronics",
    "climatization": "electronics",
    "audio": "electronics",
    "games consoles": "electronics",
    
    # books
    "books": "books",
    "general interest books": "books",
    "technical books": "books",
    "imported books": "books",
    
    # food
    "drinks": "food",
    "drink foods": "food",
    "foods": "food",
    "kitchen portable and food coach": "food",
    "la cuisine": "food",
    
    # toys
    "babies": "toys",
    "hygiene diapers": "toys",
    "toys": "toys",
    
    # pets
    "pet shop": "pets",
    
    # health_beauty
    "health beauty": "health_beauty",
    "perfumery": "health_beauty",
    
    # gifts
    "flowers": "gifts",
    "watches present": "gifts",
    
    # other
    "party articles": "others",
    "christmas articles": "others",
    "stationery": "others",
    "stationary store": "others",
    "cool stuff": "others",
    "musical instruments": "others",
    
    # services
    "insurance and services": "services",
    "industry commerce and business": "services",
    "market place": "services",
    "agro industria e comercio": "services"
}

df_datosBrasil["product_category"] = (
    df_datosBrasil["product_category"]
    .replace(map_categorias_macro)
)

# chequeo las categorias finales
print(sorted(df_datosBrasil["product_category"].unique()))
print("Número de categorías finales:", df_datosBrasil["product_category"].nunique())


### borrar fechas inconsistentes (aprobacion antes de compra, etc etc)

#mis condiciones invalidas
cond_aprobacion_antes_compra = df_datosBrasil["order_approved_at"] < df_datosBrasil["order_purchase_timestamp"]
cond_entrega_antes_carrier = df_datosBrasil["order_delivered_customer_date"] < df_datosBrasil["order_delivered_carrier_date"]
cond_entrega_antes_aprobacion = df_datosBrasil["order_delivered_customer_date"] < df_datosBrasil["order_approved_at"]

# junto todo 
cond_invalida = cond_aprobacion_antes_compra | cond_entrega_antes_carrier | cond_entrega_antes_aprobacion

# lo borro
df_datosBrasil = df_datosBrasil.loc[~cond_invalida].copy()


## borro duplicados 
df_datosBrasil=df_datosBrasil.drop_duplicates()

# Guardar el DataFrame en un nuevo CSV
df_datosBrasil.to_excel("DatosProcesados/Merge_BrasilWalmart.xlsx", index=False,engine="openpyxl")