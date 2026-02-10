pprint("Este programa captura importes")
info = """

    Calcula tu suma.

    Este programa lleva el conteo de cuantos importes ha introducido un usuario.

    Va acumulando todos los importes que el usuario ingresa.

    Si el usuario desea terminar el programa puede escribir en cualquier momento la palabra exit, quit, terminar.

    Elaborado por Hector.

"""
print(info)
conteo = 0
suma = 0.0
minimo = None
maximo = None

while true
    user_message = """

            Ingresa tu importe (MXN)
        Si quieres dejar de capturar importes puedes ingresar en cualquier momento exit, quit, 

    """

    line = input("user_message").lower()
    if line == "exit" or line == "quit" or line == "terminar":
        break
    try:
        value = float(line)
    except ValueError:
        print("valor invalido, intenta de nuevo ")
conteo += 1 # me dice cuantos importes se han introducido
suma += value # me lleva la acumulacion


print("programa finalizado")
