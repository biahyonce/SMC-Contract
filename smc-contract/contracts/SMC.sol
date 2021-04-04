pragma solidity ^0.8.0;

import {CommitHandler} from "./CommitHandler.sol";

contract SMC {
    using CommitHandler for CommitHandler.Commit;
    mapping (address => CommitHandler.Commit) public commits;
    constructor() {}

    function firstCommit(bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, truthTable);
        commits[msg.sender] = commitGenerated;
        return commitGenerated;
    }

    function secondCommit(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, previousCommitOwner, truthTable);
        commits[msg.sender] = commitGenerated;
        return commitGenerated;
    }

    function getCommit(address owner) public view returns (CommitHandler.Commit memory) {
        return commits[owner];
    }
    
    function verify(address owner, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public view returns (bool) {
        bytes32 value = commits[owner].commit;
        return CommitHandler.verify(value, nonce, inversion_bits, encryption_bits);
    }

    function getValue(address owner, uint row, bool[2] memory first_commit_choices, bool[2] memory second_commit_choices) public view returns(bool) {
        bool[3][4] memory truthTable = commits[owner].truthTable;
        bool outputEntry = truthTable[row][2];
        return outputEntry != first_commit_choices[0] != first_commit_choices[1] != second_commit_choices[0] != second_commit_choices[1];
    }
}