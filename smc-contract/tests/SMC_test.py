import pytest 
import hashlib
from brownie import accounts, SMC, CommitHandler

@pytest.fixture
def truthTable():
    return [ [False,False,False], [False,True,False], [True,False,False], [True,True,False] ]

@pytest.fixture
def A():
    return accounts[0]

@pytest.fixture
def B():
    return accounts[1]

@pytest.fixture
def contract(A):
    """ 
    Return the contracted deployed by A account.
    """
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    return SMC[0]

@pytest.fixture
def nonce():
    nonce = hashlib.sha256()
    nonce.update(b'nonce')
    return nonce.hexdigest()

@pytest.fixture
def inversion_bits():
    return [True, False]

@pytest.fixture
def encryption_bits():
    return [True, True, False, True]

@pytest.fixture
def commit(nonce, inversion_bits, encryption_bits):
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(inversion_bits))
    commit.update(bytes(encryption_bits))
    return "0x" + commit.hexdigest()

def test_first_commit(contract, A, commit, truthTable):
    first_commit = contract.firstCommit.call(commit, truthTable, {'from': A})
    assert first_commit[0] == A.address
    assert first_commit[1] == A.address
    assert first_commit[2] == commit 
    assert first_commit[3] == truthTable

def test_second_commit(contract, A, B, commit, truthTable):
    contract.firstCommit.call(commit, truthTable, {'from': A})
    second_commit = contract.secondCommit.call(A.address, commit, truthTable, {'from': B})
    assert second_commit[0] == B.address
    assert second_commit[1] == A.address
    assert second_commit[2] == commit 
    assert second_commit[3] == truthTable 

def test_valid_verify_commit(A, contract, nonce, commit, truthTable, inversion_bits, encryption_bits):
    contract.firstCommit(commit, truthTable, {'from': A})
    is_valid_commit = contract.verify.call(A.address, nonce.encode(), bytes(inversion_bits), bytes(encryption_bits))
    assert is_valid_commit == True

def test_invalid_verify_commit(A, contract, nonce, commit, truthTable, inversion_bits, encryption_bits):
    contract.firstCommit(commit, truthTable, {'from': A})
    is_valid_commit = contract.verify.call(A.address, nonce.encode(), bytes([False, True]), bytes(encryption_bits))
    assert is_valid_commit == False

def test_get_commit(A, contract, commit, truthTable):
    commit_generated = contract.firstCommit.call(commit, truthTable, {'from': A})
    get_Commit = contract.getCommit.call(A.address)
    assert get_Commit == commit_generated