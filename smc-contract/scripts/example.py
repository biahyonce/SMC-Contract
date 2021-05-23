#!/usr/bin/python3.6

from .base_permutation_handler import *
from brownie import *

A = accounts[0]
B = accounts[1]
CommitHandler.deploy({'from': A})
SMC.deploy({'from': A})
contract = SMC[0]

def main():
    TT = [  [False,False,False],
            [False,True,False],
            [True,False,False],
            [True,True,False] ]

    # Generate TT_A
    TT_A, commit_A, nonce_A, inversion_bits_A, encryption_bits_A = generate_transformed_TT(TT=TT, nonceString = b'nonceA', firstColumn = 0, secondColumn = 2)
    contract.firstCommit(commit_A, TT_A, {'from': A})

    # Generate TT_B
    TT_from_contract = contract.getCommit.call(A.address, {'from': B})[3]
    TT_B, commit_B, nonce_B, inversion_bits_B, encryption_bits_B = generate_transformed_TT(TT=TT_from_contract, nonceString = b'nonceB', firstColumn = 1, secondColumn = 2)
    contract.secondCommit(A.address, commit_B, TT_B, {'from': B})
    
    verifyA = contract.verify.call(A.address, nonce_A.encode(), bytes(inversion_bits_A), bytes(encryption_bits_A))
    verifyB = contract.verify.call(B.address, nonce_B.encode(), bytes(inversion_bits_B), bytes(encryption_bits_B))
    print("Commit from A is valid: {v}".format(v=verifyA))
    print("Commit from B is valid: {v}".format(v=verifyB))

    # Final computation
    row = 1
    result = contract.getValue.call(B.address, row, [inversion_bits_A[1], encryption_bits_A[row]], [inversion_bits_B[1], encryption_bits_B[row]])
    print("Final result: {r}".format(r=result))