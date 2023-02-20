import pandas as pd
#.read:csv -> lee el archivo .csv
suscripciones = pd.read_csv("proyecto1-estructuras\suscripciones.csv")
listEtiquetas=[]
diccionarioEtiquetas={}
#while -> llena una lista con las etiquetas que desea crear el usuario
i='si'
print('Crea tus etiquetas')
while i=='si':
        etiquetas = input('Etiqueta : ')
        listEtiquetas.append(etiquetas)
        print('Si desea agregar otra etiqueta digite si \nSi NO desea agregar otra etiqueta digite no')
        i=input('--> ')
#for -> llena un diccionario con 1 canal por etiqueta (por ahora)
for i in listEtiquetas:
    print('Elija los canales que desea etiquetar en la etiqueta ',i)
    print(suscripciones)
    agregar=int(input('Digite el número del canal que desea agregar a la etiqueta : '))
    diccionarioEtiquetas.update({i:suscripciones.iloc[agregar,1:3]})
#for -> imprime la etiqueta con su respestivo canal (por ahora)
for i in diccionarioEtiquetas:
    print(i,'--> ',diccionarioEtiquetas[i])



