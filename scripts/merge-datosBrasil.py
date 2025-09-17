# aqui hare un merge con los datos de brasil y revisare que no contengan nulos y vacios
import pandas as pd

# Cargar los datasets 
hdi = pd.read_csv("Datos-Brasil/hdi.csv")
states = pd.read_csv("Datos-Brasil/states.csv")

# Veo primeras filas para explorar para ver donde los puedo unir
print("HDI dataset:")
print(hdi.head(), "\n")

print("States dataset:")
print(states.head(), "\n")

# uno segun el codigo de estado para tener una unica columna
df_datosBrasil = pd.merge(hdi, states, left_on=hdi.columns[0], right_on=states.columns[0])


# Veo cuantos nulos y vacios hay por columna
print(df_datosBrasil.isnull().sum())
print((df_datosBrasil == "").sum())

# guardo en un nuevo archivo pronto para trabajar con el

# Guardar el DataFrame en un nuevo CSV
df_datosBrasil.to_excel("DatosProcesados/datosBrasil_final.xlsx", index=False,engine="openpyxl")


