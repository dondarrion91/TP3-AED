import os.path
from envios import Envio

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

def validar_m(total, mensaje="Ingrese un valor:"):
    m = int(input(mensaje))
    while m < -1 or m > total:
        print("Error, debe ingresar un valor entre -1 y", total)
        m = int(input(mensaje))
    return m

def select_sort_cp(v):
    n = len(v)
    for i in range(n-1):
        for j in range(i+1, n):
            if v[i].cp > v[j].cp:
                v[i], v[j] = v[j], v[i]

def buscar_envio_por_dir_tipo(v, direccion, tipo):
    for i in range(len(v)):
        match_dir = direccion == v[i].direccion
        match_tipo = tipo == v[i].tipo

        if match_dir and match_tipo:
            return i
    return -1

def buscar_envio_por_cp(v, cp):
    for i in range(len(v)):
        if cp == v[i].cp:
            return i
    return -1

def main():
    menu = '\nMenú de Opciones - TP3 G148\n' \
           '1. Cargar vector de envio\n' \
           '2. Cargar nuevo envio por teclado\n' \
           '3. Mostrar todos los envios ordenados por codigo postal, de menor a mayor\n' \
           '4. Buscar envio por dirección y tipo de envio\n' \
           '5. Buscar envio por código postal y cambiar tipo de envio\n' \
           '0. SALIR\n' \
           'Ingrese su opción: '

    envios = []
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
            # ---------------------------------------------
        elif opcion == 2:
            # ---------------------------------------------
            msg_tipo = "Tipo de envío (un número entero entre 0 y 6): "
            msg_pago = "Forma de pago (un número entero (1:efectivo, 2: tarjeta de crédito)): "

            nuevo_cp = input("Código postal: ")
            nueva_direccion = input("Dirección: ")
            nuevo_tipo = validar_tipo(msg_tipo)
            nuevo_fpago = validar_pago(msg_pago)

            nuevo_envio = Envio(nuevo_cp, nueva_direccion, nuevo_tipo, nuevo_fpago)
            envios.append(nuevo_envio)

            print("Nuevo envio agregado con exito!")
            print(nuevo_envio)
            print(len(envios), "envios actualmente cargados en la lista!")

            # ---------------------------------------------
        elif opcion == 3:
            # ---------------------------------------------
            total = len(envios)
            msg_m = "Seleccionar la cantidad de registros a mostrar (Ingresar -1 para mostrar todos): "

            m = validar_m(total, msg_m)

            if m == -1:
                m = total

            select_sort_cp(envios)

            for envio in envios[:m]:
                print(envio)

            # ---------------------------------------------
        elif opcion == 4:
            # ---------------------------------------------
            msg_tipo = "Tipo de envío (un número entero entre 0 y 6): "

            d = input("Dirección: ")
            e = validar_tipo(msg_tipo)
            
            index_d_e = buscar_envio_por_dir_tipo(envios, d, e)
            
            print("\n-------------------------------------")

            if (index_d_e != -1):
                print(envios[index_d_e])
            else:
                print("No existen envios con dirección:", d, "y tipo de envio:", e)

            print("-------------------------------------")
            # ---------------------------------------------
        elif opcion == 5:
            # ---------------------------------------------
            nuevo_cp = input("Código postal: ")
            
            index_cp = buscar_envio_por_cp(envios, nuevo_cp)
            
            print("\n-------------------------------------")

            if (index_cp != -1):
                envio_cp = envios[index_cp]
                envio_cp.cambiar_forma_pago()
                print(envio_cp)
                
            else:
                print("No existen envios con código postal:", nuevo_cp)

            print("-------------------------------------")
            # ---------------------------------------------
        elif opcion == 0:
            pass
        else:
            print('\nOpción inválida!')

# script principal...
if __name__ == '__main__':
    main()