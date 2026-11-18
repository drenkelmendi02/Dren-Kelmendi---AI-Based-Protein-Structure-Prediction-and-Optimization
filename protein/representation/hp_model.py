
from protein.representation.sequence import validate_sequence

AMINO_ACID_CLASSIFICATION = {
    'A': 'H',  # Alanine
    'C': 'H',  # Cysteine
    'D': 'P',  # Aspartic acid
    'E': 'P',  # Glutamic acid
    'F': 'H',  # Phenylalanine
    'G': 'P',  # Glycine
    'H': 'P',  # Histidine
    'I': 'H',  # Isoleucine
    'K': 'P',  # Lysine
    'L': 'H',  # Leucine
    'M': 'H',  # Methionine
    'N': 'P',  # Asparagine
    'P': 'P',  # Proline
    'Q': 'P',  # Glutamine
    'R': 'P',  # Arginine
    'S': 'P',  # Serine
    'T': 'P',  # Threonine
    'V': 'H',  # Valine
    'W': 'H',  # Tryptophan
    'Y': 'H'   # Tyrosine
}


def convert_to_hp(sequence):
    sequence = validate_sequence(sequence)

    hp_sequence = ""

    for amino_acid in sequence:
        hp_sequence += AMINO_ACID_CLASSIFICATION[amino_acid]

    return hp_sequence
