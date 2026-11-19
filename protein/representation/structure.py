
class ProteinStructure:

    def __init__(self, hp_sequence, coordinates=None):
        self.hp_sequence = hp_sequence

        if coordinates is None:
            self.coordinates = self._create_initial_structure()
        else:
            self.coordinates = coordinates

    def _create_initial_structure(self):
        coordinates = []

        for i in range(len(self.hp_sequence)):
            coordinates.append((i, 0, 0))

        return coordinates

    def get_length(self):
        return len(self.hp_sequence)

    def get_coordinate(self, index):
        return self.coordinates[index]

    def get_amino_acid_type(self, index):
        return self.hp_sequence[index]
