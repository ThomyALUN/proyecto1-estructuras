from archivoejemplo import archivo
import pandas as pd
#Recibir un dataframe
def convertir(df):
    df.to_csv("canales_noind.csv", index=False)
    return df
df=archivo()
print(convertir(df))

