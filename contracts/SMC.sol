pragma solidity ^0.8.0;

import {CommitHandler} from "./CommitHandler.sol";

// add doc
contract SMC {
    using CommitHandler for CommitHandler.Commit;
    mapping (address => CommitHandler.Commit) public commits;
    constructor() {}

    function firstCommit(bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory){
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(owner, commit, truthTable);
        commits[owner] = commitGenerated;
        return commitGenerated;
    }

    function secondCommit(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        address owner = msg.sender;
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(previousCommitOwner, commit, truthTable);
        return commitGenerated;
    } 

    function checkCommit(address owner, bytes memory nonce, bytes memory b1, bytes memory b3) public returns (bool) {
        bytes32 value = commits[owner].commit;
        return CommitHandler.verify(value, nonce, b1, b3);
    }

    function getCommit(address owner) public returns (CommitHandler.Commit memory){
        return commits[owner];
    }

}