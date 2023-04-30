class State:
    def __init__(self):
        self.percept = None
        self.time = 0
        self.people_saved = 0
        self.current_vertex = None

    def set_current_vertex(self, vertex):
        self.current_vertex = vertex

    def set_percept(self, percept):
        self.percept = percept


