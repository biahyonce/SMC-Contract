#!/usr/bin/python3.6

from .base_permutation_handler import *
from brownie import *

def make_commit(nonce: str, inversion_bits: list, encryption_bits: list):
    commit = hashlib.new('sha256', nonce.encode())
    #commit.update(bytes(inversion_bits))
    #commit.update(bytes(encryption_bits))
    return "0x" + commit.hexdigest()

def main():
    TT = [  [False,False,False],
            [False,True,False],
            [True,False,False],
            [True,True,False] ]

    # 1.1: Permutar TT
    TT_shuffled = shuffle(TT)[0]

    # 1.2: Inversão de colunas
    TT_inverted, inversion_bits = inversion_of_columns(TT_shuffled, 0, 2)

    # 1.3: Encrypt output column
    TT_encrypted, encryption_bits = encryption_of_output_column(TT_inverted)

    # 1.4.Commit
    nonce = generate_nonce(b'nonce')
    commit = make_commit(nonce, inversion_bits, encryption_bits)
    nonceSent = "0x" + nonce
    print("nonce encoded: {ne}".format(ne=nonce.encode()))
    print("nonce: {n}".format(n=nonceSent))
    # Deploy
    A = accounts[0]
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    contract = SMC[0]
    print(commit)
    
    contract.firstCommit(commit, TT_encrypted, {'from': A})
    verify = contract.verify.call(A.address, nonce, bytes(inversion_bits), bytes(encryption_bits))
    print(verify)