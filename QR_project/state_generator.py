from inflow import Inflow
from volume import Volume
from outflow import Outflow
from state import State

import itertools
# import pprint
import copy


import logging


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
                                     Outflow.get_quantities())

        # Create objects for each state.
        for state_q in states_q:
            self.states.append(State(Inflow(state_q[0], None),
                                     Volume(state_q[1], None),
                                     Outflow(state_q[2], None)))
        print "[trace] - Generate states - remove constraints"
        self.remove_inconsistencies()

        print "[trace] - Generate states - Calculate derivitives"
        self.calc_derives()

        print "[trace] - Generate states - Unpack the inflow derivitives"
        self.unpack_inflow()

        print "[trace] - Generate states - Set state ids"
        # At this point all valid states are created and should receive an id
        for i, state in enumerate(self.states):
            state.set_id(i)

        print "[trace] - Create paths - Start"
        self.create_paths()
        print "[trace] - Create paths - End"

        return self.states, self.paths

    """
    Expand the inflow states to all possible derivitives
    """
    def unpack_inflow(self):
        new_states = []

        for state in self.states:
            # inflow with quantity 0 will be expanded to 0 and +
            if state.get_inflow().get_quantity() is "0":
                state_0 = copy.deepcopy(state)
                state_0.get_inflow().set_derivitive("0")
                state.get_inflow().set_derivitive("+")

                new_states.append(state_0)
                new_states.append(state)
            # Inflow with quantity + will be expanted to all
            # possible derivitives
            else:
                for deriv in self.derivitives:
                    tmp_state = copy.deepcopy(state)
                    tmp_state.get_inflow().set_derivitive(deriv)
                    new_states.append(tmp_state)

        self.states = new_states

    """
    Remove all states that have inconsistent quantities
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

    """
    Calculate the volume derivive for all states
    """
    def calc_volume_derives(self):
        new_states = []

        for state in self.states:
            tmp_states = self.calc_volume_derive(state)
            for _state in tmp_states:
                new_states.append(_state)

        self.states = new_states

    """
    Calculate all volume derivive for a state
    """
    def calc_volume_derive(self, state):
        tmp_states = []
        influences = []
        influences.append(self.calc_influence(state.get_inflow().
                                              get_quantity(), "+"))
        influences.append(self.calc_influence(state.get_outflow().
                                              get_quantity(), "-"))

        derivive = self.calc_derive(influences)

        # if the derivitive is uncertain, create all possible states
        if derivive is "?":
            for deriv in state.get_volume().get_exogenius_options():
                tmp_state = copy.deepcopy(state)
                tmp_state.get_volume().set_derivitive(deriv)
                tmp_states.append(tmp_state)
                print tmp_state
        else:
            state.get_volume().set_derivitive(derivive)
            tmp_states.append(state)

        return tmp_states

    """
    Calculate the overflow derivive for all states
    """
    def calc_outflow_derives(self):
        for state in self.states:
            state = self.calc_outflow_derive(state)

    """
    Calculate a single overflow derivive for a state
    """
    def calc_outflow_derive(self, state):
        influences = []
        influences.append(self.calc_influence(state.get_volume().
                                              get_derivitive(), "+"))

        derivive = self.calc_derive(influences)

        state.get_outflow().set_derivitive(derivive)

        return state

    """
    Calculate the influence of a certain value given its influence.
    i.e. 0 with a positive influence is 0 and + with a negetive influence is -
    """
    def calc_influence(self, value, influence):
        if value is "?":
            return "?"

        # If the value is zero, the influence is zero
        if value is "0":
            return "0"

        # If the influence is negative with a non zero value
        # The influence is negative
        if influence is "-":
            if value is "-":
                return "+"
            if value in ["max", "+"]:
                return "-"

        # If the influence is positive with a non zero value
        # The influence is positive
        if influence is "+":
            if value is "-":
                return "-"
            if value in ["max", "+"]:
                return "+"

    """
    Calculate the derivive of a state based on all its influences.
    """
    def calc_derive(self, influences):
        neg = influences.count("-")
        pos = influences.count("+")
        undis = influences.count("?")

        if (neg > 0 and pos > 0) or undis > 0:
            return "?"

        if neg > 0:
            return "-"

        if pos > 0:
            return "+"

        return "0"


    """
    Create all paths between differents states.
    """
    def create_paths(self):
        self.paths = []

        for org_state in self.states:
            # Create a temporary state to calculate the next states.
            tmp_state = copy.deepcopy(org_state)

            # Update all the quantities and deritives to the next step.
            tmp_state.update_quantities()

            # Get the exogenius derivitives for the inflow and create extra states.
            exogenius_divs = tmp_state.get_inflow().get_exogenius_options()

            # Store all exogenius states
            ext_states = [tmp_state]
            for div in exogenius_divs:
                _state = copy.deepcopy(tmp_state)
                _state.get_inflow().set_derivitive(div)
                ext_states.append(_state)

            # Get all new states based on the new volume derivites
            new_states = []
            for _state in ext_states:
                extra_states = self.calc_volume_derive(_state)
                for new_state in extra_states:
                    new_states.append(new_state)


            for _state in new_states:
                _state = self.calc_outflow_derive(_state)

                # Match each state to a valid state, mismatches are considered
                # invalid.
                for next_state in self.states:
                    if _state == next_state:
                        self.paths.append((org_state, next_state))
