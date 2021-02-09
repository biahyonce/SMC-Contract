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
    @param lines represents the lines choosen by the entity
    @return CommitHandler.Commit represents the commit stored using the arguments informed
     */
    function firstCommit(bytes32 commit, bool[3][4] memory truthTable, uint[2] memory lines) public returns (CommitHandler.Commit memory){
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, truthTable, lines);
        commits[owner] = commitGenerated;
        return commitGenerated;
    }

    /**
    @notice Store the next commit of a computation
    @param previousCommitOwner represents the address of the previous commit owner 
    @param commit represents the commit informed by entity
    @param truthTable represents the truth table informed by entity
    @param lines represents the lines choosen by the entity
    @return Commit represents the commit stored using the arguments informed
     */
    function secondCommit(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable, uint[2] memory lines) public returns (CommitHandler.Commit memory) {
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(previousCommitOwner, commit, truthTable, lines);
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

    // test
    /**
    @notice Get value obtained after the computation is done
    @param firstOwner represents the address of the entity that started the computation
    @param secondOwner represents the address of the second entity that joined the computation
    @param b3_first represents the inversion bit of the first entity
    @param b3_second represents the inversion bit of the second entity
    @return bool indicating the value obtained after the computation is done
     */
    function getValue(address firstOwner, address secondOwner, bool b3_first, bool b3_second) public returns (bool) {
        uint[2] memory firstOwnerLines = commits[firstOwner].lines; 
        uint[2] memory secondOwnerLines = commits[secondOwner].lines;
        bool[3][4] memory TT_B = commits[secondOwner].truthTable;
        uint LA1 = firstOwnerLines[0];
        uint LA2 = firstOwnerLines[1];
        uint LB1 = secondOwnerLines[0];
        uint LB2 = secondOwnerLines[1];
        uint line;
        bool result;
        if ((LA1==LB1) || (LA1==LB2)) { line = LA1; }
	    if ((LA2==LB1) || (LA2==LB2)) { line = LA2; }
        result = TT_B[line][2];
        return (result != b3_first) != b3_second;
    }

}