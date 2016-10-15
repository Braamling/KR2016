from qr_instance import QRInstance


class Inflow(QRInstance):

    quantities = ["0", "+"]

    def __init__(self, quantity, div):
        self.cur_quantity = quantity
        self.cur_div = div

    def __eq__(self, other):
        return (self.get_quantity() is other.get_quantity() and
                self.get_derivitive() is other.get_derivitive())
