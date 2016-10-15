class QRInstance:
    quantities = []

    def __init__(self, quantity, div):
        self.cur_quantity = quantity
        self.cur_div = div

    def get_quantity(self):
        return self.cur_quantity

    def get_derivitive(self):
        return self.cur_div

    def set_quantity(self, quantity):
        self.cur_quantity = quantity

    def set_derivitive(self, derivitive):
        self.cur_div = derivitive

    def update_quantity(self):
        cur_index = self.quantities.index(self.cur_quantity)
        print len(self.quantities)
        if self.cur_div is "+":
            index = cur_index + 1
            if index is len(self.quantities):
                index = cur_index
        elif self.cur_div is "-":
            index = cur_index - 1
            if index < 0:
                index = 0
        else:
            index = cur_index

        self.cur_quantity = self.quantities[index]

    @classmethod
    def get_quantities(cls):
        return cls.quantities

    def __repr__(self):
        return "[" + str(self.cur_quantity) + ", " + str(self.cur_div) + "]"

    def to_string(self):
        return "[" + str(self.cur_quantity) + ", " + str(self.cur_div) + "]"

    def __eq__(self, other):
        return (self.get_quantity() is other.get_quantity() and
                self.get_derivitive() is other.get_derivitive())
