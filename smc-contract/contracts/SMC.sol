pragma solidity ^0.8.0;

import {CommitHandler} from "./CommitHandler.sol";

/// @title Contract for Secure Multiparty Computation
/// @author BiancaCristina
/// @notice This contract can be use to store truth table commits into Ethereum
contract SMC {
    using CommitHandler for CommitHandler.Commit;

    event StartComputation(address indexed owner, bytes32 commit);
    event FinishComputation(address indexed owner, address previousCommitOwner, bytes32 commit);

    mapping (address => CommitHandler.Commit) public commits;
    constructor() {}

    /// @notice Generate the first commit
    /// @param commit bytes32 from the commit 
    /// @param truthTable indicates the truth table to be commmited
    /// @return the commit generated
    function firstCommit(bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, truthTable);
        commits[msg.sender] = commitGenerated;
        emit StartComputation(msg.sender, commit);
        return commitGenerated;
    }

    /// @notice Generate the second commit
    /// @param previousCommitOwner indicates who owns the first commit
    /// @param commit bytes32 from the commit
    /// @param truthTable indicates the truth table to be commited
    /// @return the commit generated
    function secondCommit(address previousCommitOwner, bytes32 commit, bool[3][4] memory truthTable) public returns (CommitHandler.Commit memory) {
        CommitHandler.Commit memory commitGenerated = CommitHandler.generate(commit, previousCommitOwner, truthTable);
        commits[msg.sender] = commitGenerated;
        emit FinishComputation(msg.sender, previousCommitOwner, commit);
        return commitGenerated;
    }

    /// @notice Get the commit using the owner provided
    /// @param owner the owner's address
    /// @return the commit related
    function getCommit(address owner) public view returns (CommitHandler.Commit memory) {
        return commits[owner];
    }
    
    /// @notice Verify if the information provided matches the commit
    /// @param owner the owner's address
    /// @param nonce the nonce used to generate the commit
    /// @param inversion_bits the inversion bits used to generate the commit
    /// @param encryption_bits the encryption bits used to generate the commit
    /// @return bool indicating if the information matches the commit
    function verify(address owner, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public view returns (bool) {
        bytes32 value = commits[owner].commit;
        return CommitHandler.verify(value, nonce, inversion_bits, encryption_bits);
    }

    /// @notice Computes the final value
    /// @param owner the owner's address
    /// @param row the row choosen
    /// @param first_commit_choices the first commit choices generated during the computation
    /// @param second_commit_choices the second commit choices generated during the computation
    /// @return bool indicating the final value
    function getValue(address owner, uint row, bool[2] memory first_commit_choices, bool[2] memory second_commit_choices) public view returns(bool) {
        bool[3][4] memory truthTable = commits[owner].truthTable;
        bool outputEntry = truthTable[row][2];
        return outputEntry != first_commit_choices[0] != first_commit_choices[1] != second_commit_choices[0] != second_commit_choices[1];
    }
}