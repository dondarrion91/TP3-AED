class Envio:
    def __init__(self, cp, direccion, tipo, pago):
        self.cp = cp
        self.direccion = direccion
        self.tipo = tipo
        self.pago = pago

    def __str__(self):
        pais = self.get_pais()

        envio = "Código Postal: " + self.cp
        envio += " - Pais: " + pais
        envio += " - Dirección: " + self.direccion
        envio += " - Tipo de envio: " + self.get_tipo()
        envio += " - Forma de Pago: " + self.get_pago()
        return envio

    def cambiar_forma_pago(self):
        if self.pago == 1:
            self.pago = 2
        elif self.pago == 2:
            self.pago = 1

    def get_pago(self):
        if self.pago == 1:
            return "Efectivo"
        elif self.pago == 2:
            return "Tarjeta de crédito"

        return "Forma de pago desconocida"

    def get_tipo(self):
        if self.tipo in (0, 1, 2):
            return "Carta Simple"
        elif self.tipo in (3, 4):
            return "Carta Certificada"
        elif self.tipo in (5, 6):
            return "Carta Expresa"

        return "Tipo de carta desconocido"
    
    def calcular_importe_final(self):
        destino = self.get_pais()
        cp, tipo, pago = self.cp, self.tipo, self.pago

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

    def check_direccion(self):
        direccion = self.direccion
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

    def get_pais(self):
        cp = self.cp
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