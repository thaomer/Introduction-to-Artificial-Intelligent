class Vertex:
    def __init__(self, id_, people=0, is_brittle=False):
        self.id_ = id_
        self.people = people
        self.is_brittle = is_brittle
        self.is_broken = False

    def __lt__(self, other):
        return self.id_ < other.id_

    def __eq__(self, other):
        return self.id_ == other.id_

    def __hash__(self):
        return hash(self.id_)


    def get_brittle(self):
        return self.is_brittle

    def get_broken(self):
        return self.is_broken

    def __repr__(self):
        return f"V{self.id_}"
