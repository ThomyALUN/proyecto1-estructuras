from lectura import leerCSV

listEtiquetas=[]
diccionarioEtiquetas={}

#crea las etiquetas 
def crearEtiquetas(nombreEtiqueta):
    if nombreEtiqueta in listEtiquetas:
        print('La etiqueta ya existe')
        pass
    else:
        listEtiquetas.append(nombreEtiqueta)
    return listEtiquetas

#modificar las etiquetas
def modificarEtiquetas(oldEtiqueta,newEtiqueta):
    if oldEtiqueta in listEtiquetas:
        if (newEtiqueta in listEtiquetas):
            print('la etiqueta ya existe')
            pass
        else:
            listEtiquetas[listEtiquetas.index(oldEtiqueta)]=newEtiqueta
    else:
        print('La etiqueta que desea modificar no existe')
        pass
    return listEtiquetas

#eliminar las etiquetas
def eliminarEtiquetas(etiquetaEliminar):
    if etiquetaEliminar in listEtiquetas:
        listEtiquetas.remove(etiquetaEliminar)
    else:
        print('La etiqueta que desea eliminar no existe')
    return listEtiquetas

#llenar las etiquetas con los canales
def llenarEtiquetas(etiqueta,numeros):
    suscripciones=leerCSV("suscripciones.csv")[0]
    separarCanales=numeros.split(" ")
    #convierte la lista de strings a lista de numeros
    for a in range(len(separarCanales)):
        separarCanales[a]=int(separarCanales[a])  
        #llena un diccionario -> etiqueta(key) : canales(valores)
    diccionarioEtiquetas.update({etiqueta:suscripciones.loc[separarCanales,('URL del canal','Título del canal')]})
    return diccionarioEtiquetas

if __name__=="__main__":     
    print(crearEtiquetas('salud'))
    print(crearEtiquetas('cosina'))
    print(crearEtiquetas('depirtes'))
    print(modificarEtiquetas('cosina','cocina'))
    print(modificarEtiquetas('depirtes','deportes'))
    print(eliminarEtiquetas('salud'))
    print(llenarEtiquetas('cocina','1 2 3 4'))
