"""
This file test the behavior of SMC contract acting as a unit test.     
"""

import pytest 
import hashlib

from brownie import accounts, SMC, CommitHandler

@pytest.fixture
def A():
    """
    Return a mocked A account from brownie.
    """
    return accounts[0]

@pytest.fixture
def B():
    """
    Return a mocked B account from brownie.
    """
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
def TruthTable():
    """
    Return a mocked truth table. 
    """
    return [ [False,False,False], [False,True,False], [True,False,False], [True,True,False] ]

@pytest.fixture
def nonce():
    """
    Return the hexdigest of a nonce. 
    """
    nonce = hashlib.sha256()
    nonce.update(b'nonce')
    return nonce.hexdigest()

@pytest.fixture
def b1(): 
    """
    Return a boolean True that mocked the boolean used during the table permutation.
    """
    return True 

@pytest.fixture
def b3(): 
    """
    Return a boolean False that mocked the boolean used during the table permutation.
    """
    return False

@pytest.fixture
def commit(nonce, b1, b3):
    """
    Return a mocked commit.
    """
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(b1))
    commit.update(bytes(b3))
    return "0x" + commit.hexdigest()

def test_first_commit_generation(A, contract, commit, TruthTable):
    """
    Test if the first commit is generated correctly.
    """
    firstCommit = contract.firstCommit.call(commit, TruthTable, {'from': A})
    assert firstCommit[0] == A.address
    assert firstCommit[1] == A.address
    assert firstCommit[2] == commit 
    assert firstCommit[3] == TruthTable

def test_second_commit_generation(A, B, contract, commit, TruthTable):
    """
    Test if the second commit is generated correctly.
    """
    firstCommit = contract.firstCommit(commit, TruthTable, {'from': A})
    secondCommit = contract.secondCommit.call(A.address, commit, TruthTable, {'from': B})
    assert secondCommit[0] == B.address
    assert secondCommit[1] == A.address
    assert secondCommit[2] == commit 
    assert secondCommit[3] == TruthTable
    
def test_check_commit(A, contract, nonce, b1, b3, commit, TruthTable):
    """
    Test if a commit matches the nonce and boolean permutation.
    """
    commitGenerated = contract.firstCommit(commit, TruthTable, {'from': A})
    checkCommit = contract.checkCommit.call(A.address, nonce.encode(), bytes(b1), bytes(b3))
    assert checkCommit == True

def test_get_commit(A, contract, commit, TruthTable):
    """
    Test if the commit matches the owner address.
    """
    commitGenerated = contract.firstCommit.call(commit, TruthTable, {'from': A})
    getCommit = contract.getCommit.call(A.address)
    assert commitGenerated == getCommit