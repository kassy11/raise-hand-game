from transitions import Machine


# TODO: 図を生成する
class StateMachine(object):
    STATES = ("BothDown", "BothUp", "OnlyRightUp", "OnlyLeftUp")
    TRANSITIONS = [
        # when current state is BothDown
        {"trigger": "RightDown", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "LeftDown", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "RightNotUp", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "LeftNotUp", "source": "BothDown", "dest": "BothDown"},
        {"trigger": "RightUp", "source": "BothDown", "dest": "OnlyRightUp"},
        {"trigger": "RightNotDown", "source": "BothDown", "dest": "OnlyRightUp"},
        {"trigger": "LeftUp", "source": "BothDown", "dest": "OnlyLeftUp"},
        {"trigger": "LeftNotDown", "source": "BothDown", "dest": "OnlyLeftUp"},
        # when current state is OnlyRightUp
        {"trigger": "RightDown", "source": "OnlyRightUp", "dest": "BothDown"},
        {"trigger": "RightNotUp", "source": "OnlyRightUp", "dest": "BothDown"},
        {"trigger": "LeftDown", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
        {"trigger": "LeftNotUp", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
        {"trigger": "RightUp", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
        {"trigger": "RightNotDown", "source": "OnlyRightUp", "dest": "OnlyRightUp"},
        {"trigger": "LeftUp", "source": "OnlyRightUp", "dest": "BothUp"},
        {"trigger": "LeftNotDown", "source": "OnlyRightUp", "dest": "BothUp"},
        # when current state is OnlyLeftUp
        {"trigger": "LeftDown", "source": "OnlyLeftUp", "dest": "BothDown"},
        {"trigger": "LeftNotUp", "source": "OnlyLeftUp", "dest": "BothDown"},
        {"trigger": "RightUp", "source": "OnlyLeftUp", "dest": "BothUp"},
        {"trigger": "RightNotDown", "source": "OnlyLeftUp", "dest": "BothUp"},
        {"trigger": "RightDown", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
        {"trigger": "RightNotUp", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
        {"trigger": "LeftUp", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
        {"trigger": "LeftNotDown", "source": "OnlyLeftUp", "dest": "OnlyLeftUp"},
        # when current state is BothUp
        {"trigger": "RightDown", "source": "BothUp", "dest": "OnlyLeftUp"},
        {"trigger": "RightNotUp", "source": "BothUp", "dest": "OnlyLeftUp"},
        {"trigger": "LeftDown", "source": "BothUp", "dest": "OnlyRightUp"},
        {"trigger": "LeftNotUp", "source": "BothUp", "dest": "OnlyRightUp"},
        {"trigger": "RightUp", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "RightNotDown", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "LeftUp", "source": "BothUp", "dest": "BothUp"},
        {"trigger": "LeftNotDown", "source": "BothUp", "dest": "BothUp"},
    ]

    def __init__(self) -> None:
        self.machine = Machine(
            model=self,
            states=self.STATES,
            transitions=self.TRANSITIONS,
            initial="BothDown",
            auto_transitions=False,
        )
