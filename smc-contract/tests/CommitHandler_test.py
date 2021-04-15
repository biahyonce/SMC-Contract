import pytest 
import hashlib
from brownie import *

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
def commit_handler(A):
    CommitHandler.deploy({'from': A})
    return CommitHandler[0]

@pytest.fixture
def nonce():
    nonce = hashlib.sha256()
    nonce.update(b'nonce')
    return nonce.hexdigest()

@pytest.fixture
def invalid_nonce():
    nonce = hashlib.sha256()
    nonce.update(b'nonceInvalid')
    return nonce.hexdigest()

@pytest.fixture
def inversion_bits():
    return [True, False]

@pytest.fixture
def invalid_inversion_bits():
    return [False, True]

@pytest.fixture
def encryption_bits():
    return [True, True, False, True]

@pytest.fixture
def invalid_encryption_bits():
    return [False, True, False, True]

@pytest.fixture
def commit(nonce, inversion_bits, encryption_bits):
    commit = hashlib.new('sha256', nonce.encode())
    commit.update(bytes(inversion_bits))
    commit.update(bytes(encryption_bits))
    return "0x" + commit.hexdigest()

@pytest.fixture
def invalid_commit(invalid_nonce, inversion_bits, encryption_bits):
    commit = hashlib.new('sha256', invalid_nonce.encode())
    commit.update(bytes(inversion_bits))
    commit.update(bytes(encryption_bits))
    return "0x" + commit.hexdigest()

def test_verify(commit_handler, commit, nonce, inversion_bits, encryption_bits):
    verify = commit_handler.verify(commit, nonce.encode(), bytes(inversion_bits), bytes(encryption_bits))
    assert verify == True

def test_verify_invalid_commit(commit_handler, invalid_commit, nonce, inversion_bits, encryption_bits):
    verify = commit_handler.verify(invalid_commit, nonce.encode(), bytes(inversion_bits), bytes(encryption_bits))
    assert verify == False

def test_verify_invalid_inversion_bits(commit_handler, commit, nonce, invalid_inversion_bits, encryption_bits):
    verify = commit_handler.verify(commit, nonce.encode(), bytes(invalid_inversion_bits), bytes(encryption_bits))
    assert verify == False

def test_verify_invalid_encryption_bits(commit_handler, commit, nonce, inversion_bits, invalid_encryption_bits):
    verify = commit_handler.verify(commit, nonce.encode(), bytes(inversion_bits), bytes(invalid_encryption_bits))
    assert verify == False

def test_generate(commit_handler, A, commit, truthTable):
    commit_generated = commit_handler.generate.call(commit, truthTable, {'from': A})
    assert commit_generated[0] == A.address
    assert commit_generated[1] == A.address 
    assert commit_generated[2] == commit 
    assert commit_generated[3] == truthTable

def test_generate_with_previous_owner(commit_handler, A, B, commit, truthTable):
    commit_handler.generate(commit, truthTable, {'from': A})
    commit_generated = commit_handler.generate.call(commit, A.address, truthTable, {'from': B})
    assert commit_generated[0] == B.address
    assert commit_generated[1] == A.address 
    assert commit_generated[2] == commit 
    assert commit_generated[3] == truthTable
