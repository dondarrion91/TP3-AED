import os.path
from envios import Envio


def country(cp):
    n = len(cp)
    if n < 4 or n > 9:
        return 'Otro'

    # ¿es Argentina?
    if n == 8:
        if cp[0].isalpha() and cp[0] not in 'IO' and cp[1:5].isdigit() and cp[5:8].isalpha():
            return 'Argentina'
        else:
            return 'Otro'

    # ¿es Brasil?
    if n == 9:
        if cp[0:5].isdigit() and cp[5] == '-' and cp[6:9].isdigit():
            return 'Brasil'
        else:
            return 'Otro'

    if cp.isdigit():
        # ¿es Bolivia?
        if n == 4:
            return 'Bolivia'

        # ¿es Chile?
        if n == 7:
            return 'Chile'

        # ¿es Paraguay?
        if n == 6:
            return 'Paraguay'

        # ¿es Uruguay?
        if n == 5:
            return 'Uruguay'

    # ...si nada fue cierto, entonces sea lo que sea, es otro...
    return 'Otro'


def check_dir(direccion):
    cl = cd = 0
    td = False
    ant = " "
    for car in direccion:
        if car in " .":
            # fin de palabra...
            # un flag si la palabra tenia todos sus caracteres digitos...
            if cl == cd:
                td = True

            # resetear variables de uso parcial...
            cl = cd = 0
            ant = " "

        else:
            # en la panza de la palabra...
            # contar la cantidad de caracteres de la palabra actual...
            cl += 1

            # si el caracter no es digito ni letra, la direccion no es valida... salir con False...
            if not car.isdigit() and not car.isalpha():
                return False

            # si hay dos mayusculas seguidas, la direccion no es valida... salir con False...
            if ant.isupper() and car.isupper():
                return False

            # contar digitos para saber si hay alguna palabra compuesta solo por digitos...
            if car.isdigit():
                cd += 1

            ant = car

    # si llegamos acá, es porque no había dos mayusculas seguidas y no habia caracteres raros...
    # ... por lo tanto, habria que salir con True a menos que no hubiese una palabra con todos digitos...
    return td


def final_amount(cp, destino, tipo, pago):
    # determinación del importe inicial a pagar.
    importes = (1100, 1800, 2450, 8300, 10900, 14300, 17900)
    monto = importes[tipo]

    if destino == 'Argentina':
        inicial = monto
    else:
        if destino == 'Bolivia' or destino == 'Paraguay' or (destino == 'Uruguay' and cp[0] == '1'):
            inicial = int(monto * 1.20)
        elif destino == 'Chile' or (destino == 'Uruguay' and cp[0] != '1'):
            inicial = int(monto * 1.25)
        elif destino == 'Brasil':
            if cp[0] == '8' or cp[0] == '9':
                inicial = int(monto * 1.20)
            else:
                if cp[0] == '0' or cp[0] == '1' or cp[0] == '2' or cp[0] == '3':
                    inicial = int(monto * 1.25)
                else:
                    inicial = int(monto * 1.30)
        else:
            inicial = int(monto * 1.50)

    # determinación del valor final del ticket a pagar.
    # asumimos que es pago en tarjeta...
    final = inicial

    # ... y si no lo fuese, la siguiente será cierta y cambiará el valor...
    if pago == 1:
        final = int(0.9 * inicial)

    return final

def crear_envios(fd):
    # control de existencia...
    if not os.path.exists(fd):
        print('El archivo', fd, 'no existe...')
        print('Revise, y reinicie el programa...')
        exit(1)

    # procesamiento del archivo de entrada...
    # apertura del archivo...
    m = open(fd, 'rt')

    # procesamento de la línea de timestamp...
    # Resultado 1...
    line = m.readline()
    control = 'Soft Control'
    if 'HC' in line:
        control = 'Hard Control'

    # Reset array de envios
    envios = []

    # procesamiento de los envios registrados...
    while True:
        # ...intentar leer la linea que sigue...
        line = m.readline()

        # ...si se obtuvo una cadena vacia, cortar el ciclo y terminar...
        if line == '':
            break

        if line[-1] == "\n":
            line = line[0:-1]

        # ...procesar la línea leída si el ciclo no cortó...
        # ... obtener cada dato por separado, y en el tipo correcto...
        # ... no es necesario en este caso eliminar el "\n" del final,
        # porque la linea no se va a mostrar en pantalla, y porque las
        # instrucciones que siguen toman cada dato en forma directa,
        # prescindiendo del "\n"...
        cp = line[0:9].strip().upper()
        direccion = line[9:29].strip()
        tipo = int(line[29])
        pago = int(line[30])

        # # importe final a pagar en ese envio...
        # final = final_amount(cp, pais, tipo, pago)
        nuevo_envio = Envio(cp, direccion, tipo, pago)
        
        envios.append(nuevo_envio)

    # cierre del archivo...
    m.close()
    
    return envios, control
    
def validar_tipo(mensaje="Ingrese un valor:"):
    nvo_tipo = int(input(mensaje))
    while nvo_tipo < 0 or nvo_tipo > 6:
        print("Error, debe ingresar un valor entre 0 y 6!")
        nvo_tipo = int(input(mensaje))
    return nvo_tipo

def validar_pago(mensaje="Ingrese un valor:"):
    nvo_pago = int(input(mensaje))
    while nvo_pago not in (1, 2):
        print("Error, debe ingresar un valor igual a 1 o un valor igual a 2!")
        nvo_pago = int(input(mensaje))
    return nvo_pago

def select_sort_cp(v):
    n = len(v)
    for i in range(n-1):
        for j in range(i+1, n):
            if v[i].cp > v[j].cp:
                v[i], v[j] = v[j], v[i]

def main():
    menu = '\nMenú de Opciones - TP3 G148\n' \
           '1. Cargar vector de envio\n' \
           '2. Cargar nuevo envio por teclado\n' \
           '3. Mostrar todos los envios ordenados por codigo postal, de menor a mayor\n' \
           '0. SALIR\n' \
           'Ingrese su opción: '

    envios = None
    control = None
    opcion = -1

    while opcion != 0:
        opcion = int(input(menu))
        if opcion == 1:
            # nombre del archivo de texto de entrada...
            # ... se asume que está en la misma carpeta del proyecto...
            fd = 'envios-tp3.txt'

            envios, control = crear_envios(fd)

            print(len(envios), "envios cargados exitosamente!")

        elif opcion in (2, 3, 4, 5):
            if envios is not None:
                if opcion == 2:
                    # ---------------------------------------------
                    msg_tipo = "Tipo de envío (un número entero entre 0 y 6): "
                    msg_pago = "Forma de pago (un número entero (1:efectivo, 2: tarjeta de crédito)): "

                    nuevo_cp = input("Código postal: ")
                    nueva_direccion = input("Dirección: ")
                    nuevo_tipo = validar_tipo(msg_tipo)
                    nuevo_fpago = validar_pago(msg_pago)

                    nuevo_envio = Envio(nuevo_cp, nueva_direccion, nuevo_tipo, nuevo_fpago)
                    
                    envios.append(nuevo_envio);
                    
                    print("Nuevo envio agregado con exito!")
                    print(nuevo_envio)
                    print(len(envios), "envios actualmente cargados en la lista!")

                    # ---------------------------------------------
                elif opcion == 3:
                    # ---------------------------------------------
                    m = int(input("Seleccionar la cantidad de registros a mostrar: "))
                    select_sort_cp(envios)

                    for envio in envios[:m]:
                        pais = country(envio.cp)
                        print("País: ", pais, "-", envio)
                    # ---------------------------------------------
                elif opcion == 4:
                    # ---------------------------------------------
                    pass
                    # ---------------------------------------------
                elif opcion == 5:
                    # ---------------------------------------------
                    pass
                    # ---------------------------------------------
            else:
                print('\nPrimero debe generar envios!')
        elif opcion == 0:
            pass
        else:
            print('\nOpción inválida!')

# script principal...
if __name__ == '__main__':
    main()