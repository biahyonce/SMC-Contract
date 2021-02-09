pragma solidity ^0.8.0;

/**
@title Library responsible for generating the commits
@author BiancaCristina
 */
library CommitHandler {
    struct Commit {
        address owner;
        address previous; 
        bytes32 commit; 
        bool[3][4] truthTable;
        uint[2] lines;
    }

    /** 
    @notice Generate the first commit of a computation
    @param commit represents the commit informed by entity
    @param truthTable represents the truth table informed by entity
    @param lines represents the lines choosen by the entity
    @return Commit represents the commit generated using the arguments informed
     */
    function generate(bytes32 commit, bool[3][4] memory truthTable, uint[2] memory lines) public returns(Commit memory) {
        address owner = msg.sender;
        address previousCommitOwner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable, lines);
    }

    /**
    @notice Generate the next commit of a computation
    @param previousCommitOwner represents the address of the previous commit owner 
    @param commit represents the commit informed by entity
    @param truthTable represents the truth table informed by entity
    @param lines represents the lines choosen by the entity
    @return Commit represents the commit generated using the arguments informed
     */
    function generate(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable, uint[2] memory lines) public returns(Commit memory) {
        address owner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable, lines);
    }

    /**
    @notice Check wether the nonce an booleans matches the commit value
    @param value represents the commit to be checked
    @param nonce represents the nonce used to create the commit value
    @param b1 boolean used during the truth table permutation
    @param b3 boolean used during the truth table permutation
    @return bool indicating if the commit values matches the nonce and booleans informed
     */
    function verify(bytes32 value, bytes memory nonce, bytes memory b1, bytes memory b3) public returns(bool) {
        bytes32 generatedValue = sha256(abi.encodePacked(nonce, b1, b3));
        return value == generatedValue;
    }

    /**
    @notice Check wether the commit is the first of the computation
    @param commit represents the commit to be checked
    @return bool indicating if the commit is the first of hte computation
     */
    function isFirstCommit(Commit memory commit) public returns(bool) {
        return commit.owner == commit.previous;
    }
}
