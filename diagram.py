from transitions.extensions import GraphMachine
from state_machine import StateMachine

TRANSITIONS = [
    {"trigger": "", "source": "OnlyRaiseRight", "dest": "BothDown"},
    {"trigger": "", "source": "BothDown", "dest": "OnlyRaiseRight"},
    {"trigger": "", "source": "OnlyRaiseLeft", "dest": "BothDown"},
    {"trigger": "", "source": "BothDown", "dest": "OnlyRaiseLeft"},
    {"trigger": "", "source": "OnlyRaiseRight", "dest": "BothUp"},
    {"trigger": "", "source": "BothUp", "dest": "OnlyRaiseRight"},
    {"trigger": "", "source": "OnlyRaiseLeft", "dest": "BothUp"},
    {"trigger": "", "source": "BothUp", "dest": "OnlyRaiseLeft"},
    {"trigger": "", "source": "BothDown", "dest": "BothDown"},
    {"trigger": "", "source": "BothUp", "dest": "BothUp"},
    {"trigger": "", "source": "OnlyRaiseLeft", "dest": "OnlyRaiseLeft"},
    {"trigger": "", "source": "OnlyRaiseRight", "dest": "OnlyRaiseRight"},
]


class Test(object):
    pass


m = Test()
model = GraphMachine(
    model=m,
    states=StateMachine.STATES,
    transitions=TRANSITIONS,
    initial="BothDown",
    title="",
)
m.get_graph().draw("state_machine.png", prog="circo")
