
from protein.representation.hp_model import convert_to_hp
from protein.representation.structure import ProteinStructure

sequence = "ACDEFGHIKL"

hp_sequence = convert_to_hp(sequence)

protein = ProteinStructure(hp_sequence)

print("HP Sequence:", hp_sequence)
print("Protein Length:", protein.get_length())
print("Coordinates:")

for i in range(protein.get_length()):
    print(
        i + 1,
        protein.get_amino_acid_type(i),
        protein.get_coordinate(i)
    )
