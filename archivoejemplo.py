import pandas as pd
def archivo():
#Diccionario de canales
    canales={
    "Tecnologia": ["IsaMarcial", "Tp", "TuTecnoMundo " ],
    "Cocina":["MasterChef", "TulioRecomienda", "Luisito Comunica"],
    "Podcats": ["DiegoDreyfus", "The WildProject", "Juanpis Gonzales"]}
#Sacar dataframe
    df = pd.DataFrame(canales)
    return df
