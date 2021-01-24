pragma solidity ^0.8.0;

/**
@title library responsible for generating the commits
@author BiancaCristina
 */
// add doc
library CommitHandler {
    struct Commit {
        address owner;
        address previous; 
        bytes32 commit; 
        bool[3][4] truthTable; 
    }

    function generate(bytes32 commit, bool[3][4] memory truthTable) public returns(Commit memory) {
        address owner = msg.sender;
        address previousCommitOwner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    function generate(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable) public returns(Commit memory) {
        address owner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    function verify(bytes32 value, bytes32 nonce, bool b1, bool b3, bool[3][4] memory truthTable) public returns(bool) {
        bytes32 generatedValue = sha256(abi.encodePacked(nonce, b1, b3));
        return value == generatedValue;
    }

    function isFirstCommit(Commit memory commit) public returns(bool) {
        return commit.owner == commit.previous;
    }
}
