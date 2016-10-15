from qr_instance import QRInstance


class Height(QRInstance):

    quantities = ["0", "+", "max"]

    def __init__(self, quantity, div):
        self.cur_quantity = quantity
        self.cur_div = div
