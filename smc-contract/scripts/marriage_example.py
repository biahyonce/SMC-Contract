from .base_permutation_handler import *
from brownie import *

ALICE = accounts[0]
BOB = accounts[1]
CommitHandler.deploy({'from': ALICE})
SMC.deploy({'from': ALICE})
contract = SMC[0]

def main():
    T = [  [False,False,False],
           [False,True,False],
           [True,False,False],
           [True,True,False] ]
    
    # Etapa de Ofuscamento T -> T' (Alice)
    T_ALICE, commit_ALICE, nonce_ALICE, inversion_bits_ALICE, encryption_bits_ALICE = generate_transformed_TT(TT=T, nonceString = b'nonceALICE', firstColumn = 0, secondColumn = 2)
    contract.firstCommit(commit_ALICE, T_ALICE, {'from': ALICE})

    # Etapa de Ofuscamento T' -> T'' (Bob)
    T_from_contract = contract.getCommit.call(ALICE.address, {'from': BOB})[3]
    T_BOB, commit_BOB, nonce_BOB, inversion_bits_BOB, encryption_bits_BOB = generate_transformed_TT(TT=T_from_contract, nonceString = b'nonceBOB', firstColumn = 1, secondColumn = 2)
    contract.secondCommit(ALICE.address, commit_BOB, T_BOB, {'from': BOB})

    # Final computation
    row = 1
    result = contract.getValue.call(BOB.address, row, [inversion_bits_ALICE[1], encryption_bits_ALICE[row]], [inversion_bits_BOB[1], encryption_bits_BOB[row]])
    print("Final result: {r}".format(r=result))