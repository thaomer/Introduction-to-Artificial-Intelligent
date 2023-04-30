class State:
    def __init__(self):
        self.percept = None
        self.time = 0
        self.current_vertex = None
        self.observation = None

    def set_current_vertex(self, vertex):
        self.current_vertex = vertex

    def set_percept(self, percept):
        self.percept = percept

    def set_observation(self, observation):
        self.observation = observation


