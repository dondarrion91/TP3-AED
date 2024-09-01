class Envio:
    def __init__(self, cp, direccion, tipo, pago):
        self.cp = cp
        self.direccion = direccion
        self.tipo = tipo
        self.pago = pago

    def __str__(self):
        envio = "Código Postal: " + self.cp
        envio += " - Dirección: " + self.direccion
        envio += " - Tipo de envio: " + str(self.tipo)
        envio += " - Forma de Pago: " + str(self.tipo)
        return envio