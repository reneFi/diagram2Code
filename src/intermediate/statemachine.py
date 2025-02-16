""" This file contains all classes needed for representing a statemachine"""
class NamedObject:
    """ This class is the base for all named objects within the state machine representation"""
    def __init__(self, name):
        self._name = name  # Set the name of the object

    @property
    def name(self):
        """
        This method returns the name of the object
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """Set the name of the state machine."""
        self._name = name

    

class State(NamedObject):
    """ 
    This class represents a state in a statemachine 
    """
    def __init__(self,name):
        super().__init__(name)
        self.transitions = []
    
    def getConnectedStates(self):
        states = []
        for transition in self.transitions:
            states.append(transition.end_state)
            connected_states = transition.end_state.getConnectedStates()
            for state in connected_states:
                states.append(state)
        return states   
    
class Transition:
    """ This class represents a transition between two states"""
    def __init__(self,start_state = None, end_state = None, trigger = None, action = None):
        self.start_state = start_state
        if not start_state is None:
            start_state.transitions.append(self)
        self.end_state = end_state
        self.trigger = trigger
        self.action = action
    
    
    def is_dangling(self):
        """
        Tests if transition is initial transisition
        """
        return self.start_state is None and self.end_state is None

   
    def is_initial_transition(self):
        """
        Tests if transition is initial transisition
        """
        return self.start_state is None
    
    @property
    def is_final_state(self):
        """
        Tests if transition is final transition
        """
        return self.end_state is None

class InitialTransition(Transition):
    """ This class represents the initial transition. 
        This class can only be used as starting transition and only once in a statemachine. 
        An initial transition has only a transition end and no fireing event
    """
    def __init__(self,end_state = None,action = None):
        super().__init__(None,end_state,None,action)

class FinalTransition(Transition):
    """ This class represents the final transition. 
        A final transition is the end point in a FSM. 
        Final transitions can be occure multiple times but do not have an end state. 
        So after reaching this state no way back to other states is allowed.
    """
    def __init__(self,start_state = None,trigger = None,action = None):
        super().__init__(start_state,None,trigger,action)

class StateMachine(NamedObject):
    """ 
    This class conains the statemachine 
    """
    def __init__(self, name):
        super().__init__(name)
        self.initial_transition = None

    def get_initial_transition(self):
        """
        This method returns the initial transition as starting point for traversing the statemachine
        """
        return self.initial_transition

    def insert_initial_transition(self,transition):
        """
        This function changes the initial transition of the state machine. 
        As usual, only one initial transition is allowed.
        """
        self.initial_transition = transition

    def get_states(self):
        """
        This function returns a list of state objects. 
        Traversing will be started at initial transitions.
        """
        states = []
        if not self.initial_transition is None:
            states.append(self.initial_transition.end_state)
            connected_states = self.initial_transition.end_state.getConnectedStates()
            for state in connected_states:
                states.append(state)
        return states
