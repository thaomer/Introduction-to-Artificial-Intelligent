class BooleanProb:
    def __init__(self, probs):
        self.probs = probs

    def add_prob(self, bool_value, random_var):
        self.probs.append([bool_value, random_var])

    def get_probs(self):
        return self.probs

