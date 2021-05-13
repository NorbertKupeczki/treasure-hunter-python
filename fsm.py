class FSM:

    def __init__(self):
        self.current_state = None

    def setstate(self, state):
        self.current_state = state

    def update(self):
        if self.current_state is not None:
            self.current_state()
