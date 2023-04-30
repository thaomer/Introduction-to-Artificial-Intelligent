class Vertex:
    def __init__(self, id_, bloc=0):
        self.id_ = id_
        self.bloc = bloc

    def __lt__(self, other):
        return self.id_ < other.id_

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)

    def get_bloc(self):
        return self.bloc

    def __repr__(self):
        return f"V{self.id_, self.bloc}"