class State():

    def __init__(self, inflow, volume, outflow):
        self.inflow = inflow
        self.volume = volume
        self.outflow = outflow

    def get_inflow(self):
        return self.inflow

    def set_id(self, state_id):
        self.id = state_id

    def get_id(self):
        return self.id

    def get_volume(self):
        return self.volume

    def get_outflow(self):
        return self.outflow

    def update_quantities(self):
        self.inflow.update_quantity()
        self.volume.update_quantity()
        self.outflow.update_quantity()

    def __repr__(self):
        return str(self.id) + ": " + self.inflow.to_string() +\
               self.volume.to_string() +\
               self.outflow.to_string()

    def __eq__(self, other):
        return self.inflow == other.inflow and\
                self.volume == other.volume and\
                self.outflow == other.outflow