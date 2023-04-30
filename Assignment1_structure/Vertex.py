class Vertex:
    def __init__(self, id_, people=0, is_brittle=False):
        self.id_ = id_
        self.people = people
        self.is_brittle = is_brittle
        self.is_broken = False

    # def __repr__(self):
    #     return "id=%d people=%d brittle=%s broken=%s\n" % (self.id_,
    #                                                        self.people,
    #                                                        self.is_brittle,
    #                                                        self.is_broken)
    def __repr__(self):
        return "id=%d \n" % (self.id_)
