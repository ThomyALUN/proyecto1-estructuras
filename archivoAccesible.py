def archivoAccesible(ruta):
    accesible=True

    try:
        file = open(ruta, "r", encoding="utf-8")
        content = file.read()
        file.close()
    except FileNotFoundError:
        print("El archivo no se pudo encontrar")
        accesible=False
    except PermissionError:
        print("No se tienen los permisos necesarios para acceder al archivo")
        accesible=False
    except IOError:
        print("Ocurrió un error de E/S al acceder al archivo")
        accesible=False
    except Exception as e:
        print("Ocurrió un error inesperado:", e)
        accesible=False
    else:
        print("El archivo se leyó correctamente")
    
    return accesible