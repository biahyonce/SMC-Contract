#!/usr/bin/python3.6

from brownie import *
import brownie 
import random
import hashlib
import numpy as np

def getLinearTable(TT):
    linearTable=[]
    for row in TT:
        linearTable.extend(row)
    return linearTable

def function_and(a,b):
    return a and b

def function_or(a,b):
    return a or b

def function_greater(a,b):
    return (a==1) and (b==0)

def shuffle(T):
    rows_position = [0,1,2,3]
    random.shuffle(rows_position)
    shuffleT =[]
    for position in rows_position:
        shuffleT.append([_ for _ in T[position]])
    return (shuffleT,rows_position)

def inversion(T,column):
    inversion_bit = bool(random.getrandbits(1))
    for row in T:
        row[column] = row[column]^inversion_bit
    return inversion_bit

def getChoice():
    choice = bool(random.getrandbits(1))
    return choice

def randomPermutation(TT):
    (TT_permuted, rows_position) = shuffle(TT)
    return TT_permuted

def inversionOfColumns(TT, firstColumn, secondColumn):
    firstInversionBit = inversion(TT, firstColumn)
    secondInversionBit = inversion(TT, secondColumn)
    return (firstInversionBit, secondInversionBit, TT)

def getRows(TT, inversionBit, choice):
    rows = [0,0]
    index = 0

    for i in range(len(TT)):
        if (TT[i][1]^inversionBit) == choice: 
            rows[index] = i 
            index = index + 1

    return rows

def showTruthTable(TT):
    for row in TT: print(row)

def generateCommit(nonce, b1, b3):
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(b1))
    commit.update(bytes(b3))
    return "0x" + commit.hexdigest()

def generateNonce(randomString):
    nonce = hashlib.sha256()
    nonce.update(randomString)
    return nonce.hexdigest()

def deployContract(A):
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    return SMC[0]

def generate_TTA(contract, A, TruthTable):
    ## 1.1: Random permutation (A)
    TT_A = randomPermutation(TruthTable)

    ## 1.2: Inversion of columns 
    (b1_A, b3_A, TT_A) = inversionOfColumns(TT_A, 0, 2)
    print('\n\n>>>FINAL TT_A<<<')
    showTruthTable(TT_A)

    print('\n\n>>>SEND TT_A TO SMART CONTRACT<<<')
    nonce = generateNonce(b'nonceA')
    commit = generateCommit(nonce, b1_A, b3_A)
    contract.firstCommit(commit, TT_A, {'from': A})

def generate_TTB(contract, A, B):
    TT_A = contract.getCommit.call(A.address, {'from': B})[3]
    print('\n\n>>>TT_A from SMC<<<')
    showTruthTable(TT_A)

    ## 4.1: Random permutation (B)
    TT_B = randomPermutation(TT_A)

    ## 4.2: Inversion of columns
    (b2_B, b3_B, TT_B) = inversionOfColumns(TT_B, 1, 2)
    print('\n\n>>>FINAL TT_B<<<')
    showTruthTable(TT_B)

    print('\n\n>>>SEND TT_B TO SMART CONTRACT<<<')
    nonce = generateNonce(b'nonceB')
    commit = generateCommit(nonce, b2_B, b3_B)
    contract.secondCommit(A.address, commit, TT_B, {'from': B})

def main():
    TruthTable = [  [False,False,False],
                    [False,True,False],
                    [True,False,False],
                    [True,True,False]
    ]

    # Entities involved
    A = accounts[0]
    B = accounts[1]

    # Contract deploy
    contract = deployContract(A)
    
    # Entity A
    generate_TTA(contract, A, TruthTable)
    
    # Entity B
    generate_TTB(contract, A, B)