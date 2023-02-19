import pandas as pd 
sp= pd.read_csv('suscripciones.csv')
# .head() --> carga las primeras 5 lineas
#print(suscripciones)
sp.to_numpy().tolist()
i='True'
listEtiquetas=[]
listCanales=[]
print('Crea tus etiquetas')
while i=='True':
        etiquetas = input('Etiqueta : ')
        listEtiquetas.append(etiquetas)
        print('Si desea agregar otra etiqueta digite True \nSi NO desea agregar otra etiqueta digite False')
        i=input('--> ')
print(listEtiquetas)
for i in listEtiquetas:
    print('Elija los canales que desea etiquetar en la etiqueta ',i)
    print(suscripciones.head())
    agregar=int(input('Digite el número del canal que desea agregar a la etiqueta : '))
    listCanales.append(suscripciones[agregar])
for i in listEtiquetas:
    for a in i:
        print(i,' --> ',a)
        

