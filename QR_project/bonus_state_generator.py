from inflow import Inflow
from volume import Volume
from outflow import Outflow
from volume import Volume
from pressure import Pressure
from bonus_state import BonusState

import itertools
# import pprint
import copy


class StateGenerator:
    derivitives = ["0", "-", "+"]

    """
    Generate all possible states for Inflow, Volume and Outflow
    """
    def generate(self):
        self.states = []

        # Generate all quantities for each state.
        states_q = itertools.product(Inflow.get_quantities(),
                                     Volume.get_quantities(),
                                     Outflow.get_quantities(),
                                     Volume.get_quantities(),
                                     Pressure.get_quantities())

        # Create objects for each state.
        for state_q in states_q:
            self.states.append(BonusState(Inflow(state_q[0], None),
                                          Volume(state_q[1], None),
                                          Outflow(state_q[2], None),
                                          Volume(state_q[3], None),
                                          Pressure(state_q[4], None)))

        self.remove_inconsistencies()

        self.calc_derives()

        self.unpack_inflow()

        # At this point all valid states are created and should receive an id
        for i, state in enumerate(self.states):
            state.set_id(i)

        self.create_paths()

        return self.states, self.paths

    """
    REWRITE: Remove all states that have inconsistent quantities
    """
    def remove_inconsistencies(self):
        new_states = []

        # Remove all inconsistent states
        for state in self.states:
            if state.get_volume().get_quantity() ==\
                    state.get_outflow().get_quantity():
                new_states.append(state)

        self.states = new_states

    """
    Calculate all the derivitives of all states.
    """
    def calc_derives(self):
        self.calc_volume_derives()

        self.calc_outflow_derives()
        self.calc_height_derives()
        self.calc_pressure_derives()

    """
    TODO
    """
    def calc_height_derives(self):
        pass

    """
    TODO
    """
    def calc_height_derive(self):
        pass

    """
    TODO
    """
    def calc_pressure_derives(self):
        pass

    """
    TODO
    """
    def calc_pressure_derive(self):
        pass

    """
    REWRITE: Calculate a single overflow derivive for a state
    """
    def calc_outflow_derive(self, state):
        influences = []
        influences.append(self.calc_influence(state.get_volume().
                                              get_derivitive(), "+"))

        derivive = self.calc_derive(influences)

        state.get_outflow().set_derivitive(derivive)

        return state

    """
    REWRITE?: Create all paths between differents states.
    """
    def create_paths(self):
        self.paths = []

        for org_state in self.states:
            # Create a temporary state to calculate the next states.
            tmp_state = copy.deepcopy(org_state)

            # Update all the quantities and deritives to the next step.
            tmp_state.update_quantities()
            new_states = self.calc_volume_derive(tmp_state)

            for _state in new_states:
                _state = self.calc_outflow_derive(_state)

                # Match each state to a valid state, mismatches are considered
                # invalid.
                for next_state in self.states:
                    if _state == next_state:
                        self.paths.append((org_state, next_state))
