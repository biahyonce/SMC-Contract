from brownie import *
import hashlib

def main():
    TruthTable = [  [False,False,False],
                    [False,True,False],
                    [True,False,False],
                    [True,True,False] ]
    A = accounts[0]
    contract = SMC.deploy({'from': A})

    nonce = hashlib.sha256()
    nonce.update(b'nonce1')
    nonceDigest = nonce.digest()
    returned = contract.testCommitGeneration.call(nonceDigest, True, False, TruthTable, {'from': A})
    print('return value: ')
    print(returned)
    print(returned[1])

    #print('Check: {c}'.format(c=contract.verify.call(nonceDigest, True, False, returned[1], {'from': A})))