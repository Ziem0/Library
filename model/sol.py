from model.mol import Mol

class Sol(Mol):

    def __init__(self, *args):
        super().__init__(*args)
        self.borrowed_journals = []

