import pytest 
import hashlib

from brownie import accounts, SMC, CommitHandler

@pytest.fixture
def A():
    return accounts[0]

@pytest.fixture
def B():
    return accounts[1]

@pytest.fixture
def contract(A):
    CommitHandler.deploy({'from': A})
    SMC.deploy({'from': A})
    return SMC[0]

@pytest.fixture
def TruthTable():
    return [ [False,False,False], [False,True,False], [True,False,False], [True,True,False] ]

@pytest.fixture
def nonce():
    nonce = hashlib.sha256()
    nonce.update(b'nonce')
    return nonce.hexdigest()

@pytest.fixture
def b1(): return True 

@pytest.fixture
def b3(): return False

@pytest.fixture
def commit(nonce, b1, b3):
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(b1))
    commit.update(bytes(b3))
    return "0x" + commit.hexdigest()

def test_first_commit_generation(A, contract, commit, TruthTable):
    firstCommit = contract.firstCommit.call(commit, TruthTable, {'from': A})
    assert firstCommit[0] == A.address
    assert firstCommit[1] == A.address
    assert firstCommit[2] == commit 
    assert firstCommit[3] == TruthTable

def test_second_commit_generation(A, B, contract, commit, TruthTable):
    firstCommit = contract.firstCommit(commit, TruthTable, {'from': A})
    secondCommit = contract.secondCommit.call(A.address, commit, TruthTable, {'from': B})
    assert secondCommit[0] == B.address
    assert secondCommit[1] == A.address
    assert secondCommit[2] == commit 
    assert secondCommit[3] == TruthTable
    
def test_check_commit(A, contract, nonce, b1, b3, commit, TruthTable):
    commitGenerated = contract.firstCommit(commit, TruthTable, {'from': A})
    checkCommit = contract.checkCommit.call(A.address, nonce.encode(), bytes(b1), bytes(b3))
    assert checkCommit == True

def test_get_commit(A, contract, commit, TruthTable):
    commitGenerated = contract.firstCommit.call(commit, TruthTable, {'from': A})
    getCommit = contract.getCommit.call(A.address)
    assert commitGenerated == getCommit