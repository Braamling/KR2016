from inflow import Inflow
from volume import Volume
from outflow import Outflow
from height import Height
from pressure import Pressure
from bonus_state import BonusState
from state_generator import StateGenerator

import pprint
import itertools
import copy


class BonusStateGenerator(StateGenerator):
    derivitives = ["0", "-", "+"]

    """
    Generate all possible states for Inflow, Volume and Outflow
    """
    def generate(self):
        self.states = []

        print "\n[trace] - Generate states - Generate quantity combinations:"
        # Generate all quantities for each state.
        states_q = itertools.product(Inflow.get_quantities(),
                                     Volume.get_quantities(),
                                     Outflow.get_quantities(),
                                     Height.get_quantities(),
                                     Pressure.get_quantities())

        # Create objects for each state.
        for state_q in states_q:
            self.states.append(BonusState(Inflow(state_q[0], None),
                                          Volume(state_q[1], None),
                                          Outflow(state_q[2], None),
                                          Height(state_q[3], None),
                                          Pressure(state_q[4], None)))

        pprint.pprint(self.states)
        print "[trace] - Generate states - " +\
            str(len(self.states)) + " current states"

        print "\n[trace] - Generate states - remove constraints:"
        self.remove_inconsistencies()
        pprint.pprint(self.states)
        print "[trace] - Generate states - " +\
            str(len(self.states)) + " current states"

        print "\n[trace] - Generate states - Calculate derivitives:"
        self.calc_derives()
        pprint.pprint(self.states)
        print "[trace] - Generate states - " +\
            str(len(self.states)) + " current states"

        print "\n[trace] - Generate states - Unpack the inflow derivitives"
        self.unpack_inflow()

        print "\n[trace] - Generate states - Set state ids"
        # At this point all valid states are created and should receive an id
        for i, state in enumerate(self.states):
            state.set_id(i)

        pprint.pprint(self.states)
        print "[trace] - Generate states - " +\
            str(len(self.states)) + " current states"

        print "\n[trace] - Create paths - Start"
        self.create_paths()
        pprint.pprint(self.paths)
        print "[trace] - Generate states - " +\
            str(len(self.paths)) + " current paths"
        print "[trace] - Create paths - End\n"

        return self.states, self.paths

    """
    REWRITE: Remove all states that have inconsistent quantities
    """
    def remove_inconsistencies(self):
        new_states = []

        # Remove all inconsistent states
        for state in self.states:
            if (state.get_volume().get_quantity() is
                    state.get_outflow().get_quantity() is
                    state.get_height().get_quantity() is
                    state.get_pressure().get_quantity()):
                new_states.append(state)

        self.states = new_states

    """
    Calculate all the derivitives of all states.
    """
    def calc_derives(self):
        self.calc_volume_derives()
        self.calc_height_derives()
        self.calc_pressure_derives()
        self.calc_outflow_derives()

    """
    Calculate the height derives based on the volume (P+)
    """
    def calc_height_derives(self):
        for state in self.states:
            state = self.calc_height_derive(state)

    """
    Calculate the height derive based on the volume (P+)
    """
    def calc_height_derive(self, state):
        influences = []
        influences.append(self.calc_influence(state.get_volume().
                                              get_derivitive(), "+"))

        derivive = self.calc_derive(influences)

        state.get_height().set_derivitive(derivive)

        return state

    """
    Calculate the pressure derives based on the height (P+)
    """
    def calc_pressure_derives(self):
        for state in self.states:
            state = self.calc_pressure_derive(state)

    """
    Calculate the pressure derive based on the height (P+)
    """
    def calc_pressure_derive(self, state):
        influences = []
        influences.append(self.calc_influence(state.get_height().
                                              get_derivitive(), "+"))

        derivive = self.calc_derive(influences)

        state.get_pressure().set_derivitive(derivive)

        return state

    """
    REWRITE: Calculate a single overflow derivive for a state
    """
    def calc_outflow_derive(self, state):
        influences = []
        influences.append(self.calc_influence(state.get_pressure().
                                              get_derivitive(), "+"))

        derivive = self.calc_derive(influences)

        state.get_outflow().set_derivitive(derivive)

        return state

    """
    REWRITE?: Create all paths between differents states.
    """
    def create_paths(self):
        self.paths = []

        for source_state in self.states:
            # Create a temporary state to calculate the next states.
            tmp_state = copy.deepcopy(source_state)

            # If the quantity is not at its max or min, it could also
            # stay unchanged.
            source_state_copy = None
            if tmp_state.get_volume().is_inbetween_quantity():
                source_state_copy = copy.deepcopy(source_state)

            # Update all the quantities and deritives to the next step.
            tmp_state.update_quantities()
            # new_states = self.calc_volume_derive(tmp_state)

            # Get the exogenius derivitives for the
            # inflow and create extra states.
            exogenius_divs = tmp_state.get_inflow().get_exogenius_options()

            # Store all exogenius states
            ext_states = [tmp_state]
            for div in exogenius_divs:
                if source_state_copy is not None:
                    _state = copy.deepcopy(source_state_copy)
                    _state.get_inflow().set_derivitive(div)
                    ext_states.append(_state)
                _state = copy.deepcopy(tmp_state)
                _state.get_inflow().set_derivitive(div)
                ext_states.append(_state)

            # Get all new states based on the new volume derivites
            new_states = []
            for _state in ext_states:
                extra_states = self.calc_volume_derive(_state)
                for new_state in extra_states:
                    new_states.append(new_state)

            # print "new stateeessss------"
            # print source_state
            # print ext_states
            # print new_states
            # print "newwww stattesss ------"

            for _state in new_states:
                _state = self.calc_height_derive(_state)
                _state = self.calc_pressure_derive(_state)
                _state = self.calc_outflow_derive(_state)

                # Match each state to a valid state, mismatches are considered
                # invalid.
                for next_state in self.states:
                    if _state == next_state and next_state != source_state:
                        self.paths.append((source_state, next_state))
