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

    /*
    function verify(address owner, bytes memory nonce, bool[2] memory inversionBits, bool[4] memory encryptionBits) public view returns (bool) {
        bytes32 value = commits[owner].commit;
        return CommitHandler.verify(value, nonce, inversionBits, encryptionBits);
    }
    */
    function verify(address owner, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public view returns (bytes32) {
        bytes32 value = commits[owner].commit;
        //return value;
        return CommitHandler.verify(value, nonce, inversion_bits, encryption_bits);
    }
}