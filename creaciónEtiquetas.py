from lectura import leerCSV

listEtiquetas=[]
diccionarioEtiquetas={}

#crea las etiquetas 
def crearEtiquetas():
    print('CREA TUS ETIQUETAS')
    i='si'
    while i=='si':
        etiquetas = input('Etiqueta : ')
        listEtiquetas.append(etiquetas)
        i=input('¿Desea agregar otra etiqueta? si/no ')
    return listEtiquetas

#modificar las etiquetas
def modificarEtiquetas():
    print('MODIFICA TUS ETIQUETAS')
    print(listEtiquetas)
    oldEtiqueta=input('Escribe la etiqueta que deseas moficiar : ')
    newEtiqueta=input('Escribe la nueva etiqueta : ')
    listEtiquetas[listEtiquetas.index(oldEtiqueta)]=newEtiqueta
    return listEtiquetas

#eliminar las etiquetas
def eliminarEtiquetas():
    print('ELIMINA TUS ETIQUETAS')
    print(listEtiquetas)
    etiqueta=input('Escribe la etiqueta que deseas eliminar : ')
    listEtiquetas.remove(etiqueta)
    return listEtiquetas

#llenar las etiquetas con los canales
def llenarEtiquetas():
    print('ETIQUETA TUS CANALES')
    suscripciones=leerCSV("suscripciones.csv")[0]
    print('Digita los números de los canales que deseas agregar a la etiqueta \n')
    print(suscripciones)
    for i in listEtiquetas:
        agregar=input(f'{i} : ')
        separarCanales=agregar.split(" ")
        #convierte la lista de strings a lista de numeros
        for a in range(len(separarCanales)):
            separarCanales[a]=int(separarCanales[a])  
        #llena un diccionario -> etiqueta(key) : canales(valores)
        diccionarioEtiquetas.update({i:suscripciones.loc[separarCanales,('URL del canal','Título del canal')]})
    return diccionarioEtiquetas

print(crearEtiquetas())
print(modificarEtiquetas())
print(eliminarEtiquetas())
print(llenarEtiquetas())