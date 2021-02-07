pragma solidity ^0.8.0;

import {CommitHandler} from "./CommitHandler.sol";

/**
@title Contract responsible for store commits related to a truth table permutation
@author BiancaCristina
@notice The current implementation only supports two entity per computation
 */
contract SMC {
    using CommitHandler for CommitHandler.Commit;
    mapping (address => CommitHandler.Commit) public commits;
    constructor() {}

    /**
    @notice Store the first commit of the computation
    @param commit represents the commit informed by entity
    @param truthTable represents the truth table informed by entity
    @return CommitHandler.Commit represents the commit stored using the arguments informed
     */
    function firstCommit(bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory){
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, truthTable);
        commits[owner] = commitGenerated;
        return commitGenerated;
    }

    /**
    @notice Store the next commit of a computation
    @param previousCommitOwner represents the address of the previous commit owner 
    @param commit represents the commit informed by entity
    @param truthTable represents the truth table informed by entity
    @return Commit represents the commit stored using the arguments informed
     */
    function secondCommit(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(previousCommitOwner, commit, truthTable);
        return commitGenerated;
    } 

    /**
    @notice Check wether the nonce an booleans matches the commit value
    @param owner represents the address of the commit owner
    @param nonce represents the nonce used to create the commit value
    @param b1 boolean used during the truth table permutation
    @param b3 boolean used during the truth table permutation
    @return bool indicating if the commit values matches the nonce and booleans informed
     */
    function checkCommit(address owner, bytes memory nonce, bytes memory b1, bytes memory b3) public returns (bool) {
        bytes32 value = commits[owner].commit;
        return CommitHandler.verify(value, nonce, b1, b3);
    }

    /**
    @notice Check wether the commit is the first of the computation
    @param owner represents the address of the commit owner
    @return bool indicating if the commit is the first of hte computation
     */
    function getCommit(address owner) public returns (CommitHandler.Commit memory){
        return commits[owner];
    }

}