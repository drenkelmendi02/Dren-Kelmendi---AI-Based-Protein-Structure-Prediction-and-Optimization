


VALID_AMINO_ACIDS = {
    'A', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'K', 'L',
    'M', 'N', 'P', 'Q', 'R',
    'S', 'T', 'V', 'W', 'Y'
}


def validate_sequence(sequence):
    

    if not isinstance(sequence, str):
        raise TypeError("Protein sequence must be a string")

    
    sequence = sequence.upper().strip()

    if not sequence:
        raise ValueError("Protein sequence cannot be empty")

    # Check every amino acid
    for amino_acid in sequence:

        if amino_acid not in VALID_AMINO_ACIDS:
            raise ValueError(
                f"Invalid amino acid: {amino_acid}"
            )

    return sequence


def get_sequence_length(sequence):
   

    sequence = validate_sequence(sequence)

    return len(sequence)


def get_amino_acid_count(sequence):


    sequence = validate_sequence(sequence)

    amino_acid_count = {}

    for amino_acid in sequence:

        if amino_acid in amino_acid_count:
            amino_acid_count[amino_acid] += 1

        else:
            amino_acid_count[amino_acid] = 1

    return amino_acid_count
