class QRInstance:
    quantities = []
    derivitives = ["-", "0", "+"]

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

    def is_inbetween_quantity(self):
        if self.cur_quantity is "+":
            return True
        else:
            return False

    """
    Update the quantity of an instance by issuing its derivitive.
    """
    def update_quantity(self):
        # Get the current index in the quantities list of the instance.
        cur_index = self.quantities.index(self.cur_quantity)

        # Check the derivitive and update the quanitity
        if self.cur_div is "+":
            index = cur_index + 1
            if index is len(self.quantities):
                # Quanity stays the same
                index = cur_index
        elif self.cur_div is "-":
            index = cur_index - 1
            if index < 0:
                # Quanity stays the same
                index = 0
        else:
            # Quanity stays the same
            index = cur_index

        self.cur_quantity = self.quantities[index]

    @classmethod
    def get_quantities(cls):
        return cls.quantities

    def __repr__(self):
        return "[" + str(self.cur_quantity) + ":" + str(self.cur_div) + "] "

    def to_string(self):
        return "[" + str(self.cur_quantity) + ":" + str(self.cur_div) + "] "


    """
    Get the exogenius change options for this instances.
    """
    def get_exogenius_options(self):
        if self.cur_div is None:
            return self.derivitives

        options = [self.cur_div]

        cur_index = self.derivitives.index(self.cur_div)

        if cur_index + 1 < len(self.derivitives):
            options.append(self.derivitives[cur_index + 1])

        if cur_index - 1 >= 0:
            options.append(self.derivitives[cur_index - 1])

        return options

    def __eq__(self, other):
        return (self.get_quantity() is other.get_quantity() and
                self.get_derivitive() is other.get_derivitive())
