import random
import hashlib

def generate_random_bit():
    return bool(random.getrandbits(1))

def shuffle(TT: list):
    rows_position = [0,1,2,3]
    random.shuffle(rows_position)
    shuffleT =[]
    for position in rows_position:
        shuffleT.append([_ for _ in TT[position]])
    return (shuffleT,rows_position)

def inversion_of_columns(TT: list, firstColumn: int, secondColumn: int):
    firstInversionBit = column_inversion(TT, firstColumn)
    secondInversionBit = column_inversion(TT, secondColumn)
    return (TT, [firstInversionBit, secondInversionBit])

def column_inversion(TT: list, column: int):
    inversionBit = generate_random_bit()
    for row in TT:
        row[column] = row[column]^inversionBit
    return inversionBit

def encryption_of_output_column(TT: list):
    bitPosition = 0
    output_column = 2
    encryption_bits = []
    for i in range(len(TT)):
        encryption_bits.append(generate_random_bit())
    for row in TT:
        row[output_column] = row[output_column]^encryption_bits[bitPosition]
        bitPosition = bitPosition + 1
    return (TT, encryption_bits)

def generate_commit(nonce: str, inversion_bits: list, encryption_bits: list):
    commit = hashlib.new('sha256', nonce.encode())
    for bit in inversion_bits: 
        commit.update(bytes(bit))
    for bit in encryption_bits: 
        commit.update(bytes(bit))
    return "0x" + commit.hexdigest()

def generate_nonce(random_string: str):
    nonce = hashlib.sha256()
    nonce.update(random_string)
    return nonce.hexdigest()

def generate_transformed_TT(TT: list, nonceString: str):
    TT = shuffle(TT)[0]
    TT, inversion_bits = inversion_of_columns(TT, 0, 2)
    TT, encryption_bits = encryption_of_output_column(TT)
    nonce = generate_nonce(nonceString)
    commit = generate_commit(nonce, inversion_bits, encryption_bits)
    return (TT, commit, nonce, inversion_bits, encryption_bits)