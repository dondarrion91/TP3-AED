import os.path
from envios import Envio

def crear_envios(fd):
    if not os.path.exists(fd):
        print('El archivo', fd, 'no existe...')
        print('Revise, y reinicie el programa...')
        exit(1)

    m = open(fd, 'rt')

    line = m.readline()
    control = 'Soft Control'
    if 'HC' in line:
        control = 'Hard Control'

    envios = []

    while True:
        line = m.readline()

        if line == '':
            break

        if line[-1] == "\n":
            line = line[0:-1]

        cp = line[0:9].strip().upper()
        direccion = line[9:29].strip()
        tipo = int(line[29])
        pago = int(line[30])

        nuevo_envio = Envio(cp, direccion, tipo, pago)
        
        envios.append(nuevo_envio)

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
           '6. Mostar cantidad de envios por tipo de envio.\n' \
           '7. Mostrar importe final acumulado por tipo de envio.\n' \
           '8. Obtener tipo de envio con mayor importe acumulado.\n' \
           '9. Calcular y mostrar importe final promedio.\n' \
           '0. SALIR\n' \
           'Ingrese su opción: '

    envios = []
    cantidades, importes = None, None
    control = "Hard Control"
    opcion = -1

    while opcion != 0:
        opcion = int(input(menu))
        if opcion == 1:
            # nombre del archivo de texto de entrada...
            # ... se asume que está en la misma carpeta del proyecto...
            msg = "Al realizar esta operación, los envios previamente cargados seran eliminados!\n" \
            + "Si desea cancelar esta acción, ingrese el valor 0, en caso de proseguir, presione cualquier tecla: "
            notsure = input(msg)

            fd = 'envios-tp3.txt'
            
            if notsure == '0':
                print("Accion cancelada!\nCantidad de envios cargados:", len(envios))
            else:
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

            if len(envios) == 0:
                print("------------------------------------------------")
                print("No hay envios cargados! Ingresar opciones 1 ó 2")
                print("------------------------------------------------")
            else:
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

            if index_d_e != -1:
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

            if index_cp != -1:
                envio_cp = envios[index_cp]
                envio_cp.cambiar_forma_pago()
                print(envio_cp)
                
            else:
                print("No existen envios con código postal:", nuevo_cp)

            print("-------------------------------------")
            # ---------------------------------------------
        elif opcion == 6:
            # ---------------------------------------------
            cantidades = 7 * [0]

            for envio in envios:
                if control == "Hard Control":
                    direccion_is_valid = envio.check_direccion()

                    if direccion_is_valid:
                        cantidades[envio.tipo] += 1
                else:
                    cantidades[envio.tipo] += 1

            print("-------------------------------------")
            print("Carta Simple - Peso menor a 20g:", cantidades[0], "envios.")
            print("Carta Simple - Peso entre 20g y 150g:", cantidades[1], "envios.")
            print("Carta Simple - Peso entre 150g y 500g:", cantidades[2], "envios.")
            print("Carta Certificada - Peso menor a 150g:", cantidades[3], "envios.")
            print("Carta Certificada - Peso entre 150g y 500g:", cantidades[4], "envios.")
            print("Carta Expresa - Peso menor a 150g:", cantidades[5], "envios.")
            print("Carta Expresa - Peso entre 150g y 500g:", cantidades[6], "envios.")
            print("-------------------------------------")
            # ---------------------------------------------
        elif opcion == 7:
            # ---------------------------------------------
            importes = 7 * [0]
            
            for envio in envios:
                import_final = envio.calcular_importe_final()

                if control == "Hard Control":
                    direccion_is_valid = envio.check_direccion()

                    if direccion_is_valid:
                        importes[envio.tipo] += import_final
                else:
                    importes[envio.tipo] += import_final

            print("-------------------------------------")
            print("Importe final - Carta Simple - Peso menor a 20g: $", importes[0])
            print("Importe final - Carta Simple - Peso entre 20g y 150g: $", importes[1])
            print("Importe final - Carta Simple - Peso entre 150g y 500g: $", importes[2])
            print("Importe final - Carta Certificada - Peso menor a 150g: $", importes[3])
            print("Importe final - Carta Certificada - Peso entre 150g y 500g: $", importes[4])
            print("Importe final - Carta Expresa - Peso menor a 150g: $", importes[5])
            print("Importe final - Carta Expresa - Peso entre 150g y 500g: $", importes[6])
            print("-------------------------------------")
            # ---------------------------------------------
        elif opcion == 8:
            # ---------------------------------------------
            if not importes:
                print("\n-------------------------------------")
                print("Error: No existe la lista de importes acumulados, por favor ingresar opción 7.")
                print("-------------------------------------")
            else:
                mayor_importe, tipo_index = None, None
                total = 0
                porcentaje = 0

                for i in range(len(importes)):
                    total += importes[i]

                    if mayor_importe is None or importes[i] > mayor_importe:
                        tipo_index = i
                        mayor_importe = importes[i]

                if total != 0:
                    porcentaje = (mayor_importe * 100) / total

                print("Tipo de envio con con mayor importe acumulado:", tipo_index)
                print("Importe acumulado:", mayor_importe)
                print("Porcentaje respecto al monto total: %", round(porcentaje, 2))
            # ---------------------------------------------
        elif opcion == 9:
            # ---------------------------------------------
            total_importe_final = 0
            total_menor_promedio = 0
            promedio = 0

            for envio in envios:
                importe_final = envio.calcular_importe_final()
                total_importe_final += importe_final

            if len(envios) != 0:
                promedio = int(total_importe_final / len(envios))
            
            for envio in envios:
                importe_final = envio.calcular_importe_final()

                if importe_final < promedio:
                    total_menor_promedio += 1

            print("Importe total promedio:", promedio)
            print("Cantidad de envios que tuvieron importe menor al promedio:", total_menor_promedio)
            # ---------------------------------------------
        elif opcion == 0:
            pass
        else:
            print('\nOpción inválida!')

# script principal...
if __name__ == '__main__':
    main()