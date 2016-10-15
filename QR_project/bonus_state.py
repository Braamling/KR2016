from state import State


class BonusState(State):

    def __init__(self, inflow, volume, outflow, height, pressure):
        self.inflow = inflow
        self.volume = volume
        self.outflow = outflow
        self.height = height
        self.pressure = pressure

    def update_quantities(self):
        self.inflow.update_quantity()
        self.volume.update_quantity()
        self.outflow.update_quantity()
        self.height.update_quantity()
        self.pressure.update_quantity()

    def __repr__(self):
        return (str(self.id) + ": " + self.inflow.to_string() +
                self.volume.to_string() +
                self.outflow.to_string() +
                self.height.to_string() +
                self.pressure.to_string())

    def __eq__(self, other):
        return (self.inflow == other.inflow and
                self.volume == other.volume and
                self.height == other.height and
                self.pressure == other.pressure and
                self.outflow == other.outflow)
