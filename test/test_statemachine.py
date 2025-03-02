"""Test execution for state machine abstraction functionality"""

# Copyright 2024 René Fischer - renefischer@fischer-homenet.de
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from intermediate.statemachine import StateMachine
from intermediate.statemachine import InitialTransition
from intermediate.statemachine import FinalTransition
from intermediate.statemachine import Transition
from intermediate.statemachine import State

#
# Transition tests
#

def test_transition_dangling():
    """Test if a newly created transition is dangling"""

    transition = Transition()
    assert transition.is_dangling()

def test_initial_transition_connected():
    """
    Test if a initial transition with end state is connected. 
    This implies that Transition is also connected because one end point is connected to a state
    """

    transition1 = InitialTransition(State("State1"))
    assert not transition1.is_dangling()

def test_final_transition_connected():
    """
    Test if a final transition with start state is connected. 
    This implies that Transition is also connected because one the two end points are connected to a state
    """

    transition1 = FinalTransition(State("State1"))
    assert not transition1.is_dangling()

def test_transition_state_connection():
    """
    Test if start state is connected. 
    """
    state = State("test")
    final_transition = FinalTransition(state)
    initial_transition = InitialTransition(state)
    
    assert final_transition.start_state == state
    assert final_transition.end_state is None
    assert initial_transition.start_state is None
    assert initial_transition.end_state == state
#
# states
#

def test_state_insert_one_transition():
    """
    Test if states can be inserted
    """
    state_first = State("first")
    state_second = State("second")
    transition_first_second = Transition(state_second)

    state_first.transitions.append(transition_first_second)

    assert state_first.transitions.pop() == transition_first_second
    
def test_state_insert_outgoing_transition_to_two_states():
    """
    Test if states can be inserted
    """
    state_first = State("first")
    state_second = State("second")
    state_third = State("third")

    transition_first_second = Transition(state_first, state_second)
    transition_first_third = Transition(state_first, state_third)

    assert state_first.transitions ==  [ transition_first_second , transition_first_third ]

#
# fsm tests
#

def test_statemachine_name():
    """Test the name property of state machine"""

    statemachine = StateMachine("TestStatemachine")
    assert statemachine.name == "TestStatemachine"

def test_statemachine_empty():
    """Test the empty state of statemachine"""

    statemachine = StateMachine("test")
    assert statemachine.get_initial_transition() is None

def test_statemachine_insert_initial_transition_should_return_the_initial_transition():
    """Test if initial transition can be inserted"""

    statemachine = StateMachine("test")
    statemachine.insert_initial_transition(InitialTransition())
    assert statemachine.get_initial_transition().is_initial_transition()

def test_statemachine_insert_second_initial_transition_should_return_the_last_inserted():
    """Test if last inserted initial transition is active"""

    statemachine = StateMachine("test")
    transition1 = InitialTransition()
    transition2 = InitialTransition()
    statemachine.insert_initial_transition(transition1)
    statemachine.insert_initial_transition(transition2)
    assert statemachine.get_initial_transition() == transition2
    assert statemachine.get_initial_transition() != transition1

#
#   Traversing state machine
#
def test_traversing_empty_statemachine_returns_no_state():
    """Test the empty state of statemachine"""

    statemachine = StateMachine("test")
    assert len(statemachine.get_states()) == 0

def test_traversing_statemachine_with_one_state_returns_one_state():
    """Test the statemachine with one state"""

    state = State("one")
    transition1 = InitialTransition(state)
    statemachine = StateMachine("test")
    statemachine.insert_initial_transition(transition1)

    assert len(statemachine.get_states()) == 1
    assert statemachine.get_states() == [ state ]

def test_traversing_statemachine_with_three_states_returns_three_state():
    """Test the statemachine with three state"""

    # +-------------------+
    # |                   |
    # |                   |
    # |                   |
    # +---------+---------+
    #           |          
    #           |          
    #           |          
    # +---------v---------+
    # |                   |
    # |                   |
    # |                   |
    # +---------+---------+
    #           |          
    #           |          
    #           |          
    # +---------v---------+
    # |                   |
    # |                   |
    # |                   |
    # +-------------------+

    state1 = State("one")
    state2 = State("two")
    state3 = State("three")
    transition1 = InitialTransition(state1)
    Transition(state1,state2)
    Transition(state2,state3)
    statemachine = StateMachine("test")
    statemachine.insert_initial_transition(transition1)

    assert len(statemachine.get_states()) == 3
    assert statemachine.get_states() == [ state1 , state2 , state3 ]
