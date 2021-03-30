#!/usr/bin/python3.6
"""
This shows an execution example of the SMC.

Author: BiancaCristina
"""

from .base_permutation_handler import *

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
    A_choice, b3_A = generate_TTA(contract, A, TruthTable)
    
    # Entity B
    B_choice, b3_B = generate_TTB(contract, A, B)

    # Get value
    result = contract.getValue.call(A.address, B.address, b3_A, b3_B, {'from': A})
    match = result == (A_choice and B_choice)
    print("Match result : {match}".format(match=match))
