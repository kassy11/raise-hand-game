from transitions import Machine


# TODO: 図を生成する
class StateMachine(object):
    STATES = ("BothDown", "BothUp", "OnlyRaiseRight", "OnlyRaiseLeft")
    TRANSITIONS = [
        # when current state is BothDown
        {"trigger": "LowerRight", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "LowerLeft", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "DoNotRaiseRight", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "DoNotRaiseLeft", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "RaiseRight", "source": "BothDown", "dest": "OnlyRaiseRight"},
        {"trigger": "DoNotLowerRight", "source": "BothDown", "dest": "OnlyRaiseRight"},
        {"trigger": "RaiseLeft", "source": "BothDown", "dest": "OnlyRaiseLeft"},
        {"trigger": "DoNotLowerLeft", "source": "BothDown", "dest": "OnlyRaiseLeft"},
        # when current state is OnlyRaiseRight
        {"trigger": "LowerRight", "source": "OnlyRaiseRight", "dest": "BothDown"},
        {"trigger": "DoNotRaiseRight", "source": "OnlyRaiseRight", "dest": "BothDown"},
        {"trigger": "LowerLeft", "source": "OnlyRaiseRight", "dest": "OnlyRaiseRight"},
        {
            "trigger": "DoNotRaiseLeft",
            "source": "OnlyRaiseRight",
            "dest": "OnlyRaiseRight",
        },
        {"trigger": "RaiseRight", "source": "OnlyRaiseRight", "dest": "OnlyRaiseRight"},
        {
            "trigger": "DoNotLowerRight",
            "source": "OnlyRaiseRight",
            "dest": "OnlyRaiseRight",
        },
        {"trigger": "RaiseLeft", "source": "OnlyRaiseRight", "dest": "BothUp"},
        {"trigger": "DoNotLowerLeft", "source": "OnlyRaiseRight", "dest": "BothUp"},
        # when current state is OnlyRaiseLeft
        {"trigger": "LowerLeft", "source": "OnlyRaiseLeft", "dest": "BothDown"},
        {"trigger": "DoNotRaiseLeft", "source": "OnlyRaiseLeft", "dest": "BothDown"},
        {"trigger": "RaiseRight", "source": "OnlyRaiseLeft", "dest": "BothUp"},
        {"trigger": "DoNotLowerRight", "source": "OnlyRaiseLeft", "dest": "BothUp"},
        {"trigger": "LowerRight", "source": "OnlyRaiseLeft", "dest": "OnlyRaiseLeft"},
        {
            "trigger": "DoNotRaiseRight",
            "source": "OnlyRaiseLeft",
            "dest": "OnlyRaiseLeft",
        },
        {"trigger": "RaiseLeft", "source": "OnlyRaiseLeft", "dest": "OnlyRaiseLeft"},
        {
            "trigger": "DoNotLowerLeft",
            "source": "OnlyRaiseLeft",
            "dest": "OnlyRaiseLeft",
        },
        # when current state is BothUp
        {"trigger": "LowerRight", "source": "BothUp", "dest": "OnlyRaiseLeft"},
        {"trigger": "DoNotRaiseRight", "source": "BothUp", "dest": "OnlyRaiseLeft"},
        {"trigger": "LowerLeft", "source": "BothUp", "dest": "OnlyRaiseRight"},
        {"trigger": "DoNotRaiseLeft", "source": "BothUp", "dest": "OnlyRaiseRight"},
        {"trigger": "RaiseRight", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "DoNotLowerRight", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "RaiseLeft", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "DoNotLowerLeft", "source": "BothUp", "dest": "BothUp"},
    ]

    def __init__(self) -> None:
        self.machine = Machine(
            model=self,
            states=self.STATES,
            transitions=self.TRANSITIONS,
            initial="BothDown",
            auto_transitions=False,
        )
