"""
This files handle the truth table permutation 
as describe in the base article.

Author: BiancaCristina

Base article citation:
Chaum D., Damgård I.B., van de Graaf J. (1988) Multiparty Computations Ensuring Privacy of Each Party’s Input and Correctness of the Result. 
In: Pomerance C. (eds) Advances in Cryptology — CRYPTO ’87. CRYPTO 1987. Lecture Notes in Computer Science, vol 293. Springer, Berlin, Heidelberg. 
https://doi.org/10.1007/3-540-48184-2_7
"""

from brownie import *
import brownie 
import random
import hashlib
import numpy as np

"""
Convert an list of lists into a linear list
"""
def getLinearTable(TT: list):
    linearTable=[]
    for row in TT:
        linearTable.extend(row)
    return linearTable
"""
Define an and function
"""
def function_and(a: bool, b: bool):
    return a and b

"""
Define an or function
"""
def function_or(a: bool, b: bool):
    return a or b

"""
Define a greater function
"""
def function_greater(a: bool, b: bool):
    return (a==1) and (b==0)

"""
Shuffle the table provided as argument
"""
def shuffle(T: list):
    rows_position = [0,1,2,3]
    random.shuffle(rows_position)
    shuffleT =[]
    for position in rows_position:
        shuffleT.append([_ for _ in T[position]])
    return (shuffleT,rows_position)

"""
Execute the inversion of columns as described 
in point 1.2 of the base article protocol
"""
def inversion(T: list, column: int):
    inversion_bit = bool(random.getrandbits(1))
    for row in T:
        row[column] = row[column]^inversion_bit
    return inversion_bit

"""
Get a random boolean choice
"""
def getChoice():
    choice = bool(random.getrandbits(1))
    return choice

"""
Generate a random permutation of the truth table
as described in the point 1.1 of the base article protocol
"""
def randomPermutation(TT: list):
    (TT_permuted, rows_position) = shuffle(TT)
    return TT_permuted

"""
Execute the inversion of columns as described 
in point 1.2 of the base article protocol
"""
def inversionOfColumns(TT: list, firstColumn: int, secondColumn: int):
    firstInversionBit = inversion(TT, firstColumn)
    secondInversionBit = inversion(TT, secondColumn)
    return (firstInversionBit, secondInversionBit, TT)

"""
Get the rows indicated by the inversion bit
"""
def getRows(TT: list, inversionBit: bool, choice: bool):
    rows = [0,0]
    index = 0

    for i in range(len(TT)):
        if (TT[i][1]^inversionBit) == choice: 
            rows[index] = i 
            index = index + 1

    return rows

"""
Print the truth table provided as argument
"""
def showTruthTable(TT: list):
    for row in TT: print(row)

"""
Generate a commit using the nonce and the 
bits provided as arguments
"""
def generateCommit(nonce: str, b1: bool, b3: bool):
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(b1))
    commit.update(bytes(b3))
    return "0x" + commit.hexdigest()

"""
Generate a nonce using the string provided
"""
def generateNonce(randomString: str):
    nonce = hashlib.sha256()
    nonce.update(randomString)
    return nonce.hexdigest()

"""
Deploy the contract using the account 
provided as argument 
"""
def deployContract(A: brownie.network.account.Account):
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    return SMC[0]

"""
Generate the truth table of entity A (first one)
"""
def generate_TTA(contract: brownie.network.contract.ProjectContract, A: brownie.network.account.Account, TruthTable: list):
    TT_A = randomPermutation(TruthTable)
    (b1_A, b3_A, TT_A) = inversionOfColumns(TT_A, 0, 2)
    nonce = generateNonce(b'nonceA')
    commit = generateCommit(nonce, b1_A, b3_A)
    A_choice = getChoice()
    A_rows = getRows(TT_A, b1_A, A_choice)
    contract.firstCommit(commit, TT_A, A_rows, {'from': A})
    return A_choice, b3_A

"""
Generate the truth table of entity B (second one)
"""
def generate_TTB(contract: brownie.network.contract.ProjectContract, A: brownie.network.account.Account, B: brownie.network.account.Account):
    TT_A = contract.getCommit.call(A.address, {'from': B})[3]
    TT_B = randomPermutation(TT_A)
    (b2_B, b3_B, TT_B) = inversionOfColumns(TT_B, 1, 2)
    nonce = generateNonce(b'nonceB')
    commit = generateCommit(nonce, b2_B, b3_B)
    B_choice = getChoice()
    B_rows = getRows(TT_B, b2_B, B_choice)
    contract.secondCommit(A.address, commit, TT_B, B_rows, {'from': B})
    return B_choice, b3_B