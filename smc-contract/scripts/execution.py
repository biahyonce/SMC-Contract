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

def main():
    TruthTable = [  [False,False,False],
                    [False,True,False],
                    [True,False,False],
                    [True,True,False]
    ]

    # Initial truth table
    nonce = generateNonce(b'nonce')
    commit = generateCommit(nonce, True, False)
    print(nonce)
    print()
    print('commit = {c}'.format(c = commit))

    # remove
    A = accounts[0]
    B = accounts[1]
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    contract = SMC[0]
    contract.commit(commit, TruthTable, {'from': A})
    print('get commit = {c}'.format(c=contract.getCommit.call(A.address, {'from': A})[2]))
    print(contract.checkCommit.call(A.address, nonce.encode(), bytes(True), bytes(False)))  