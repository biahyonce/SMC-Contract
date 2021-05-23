pragma solidity ^0.8.0;

/// @title Helper librafy for the SMC contract
/// @author BiancaCristina
/// @notice This library can be used to simplify the SMC contract
library CommitHandler {
    struct Commit {
        address owner;
        address previous;
        bytes32 commit;
        bool[3][4] truthTable;
    }

    /// @notice Generate the first commit structure
    /// @param commit bytes32 from the commit
    /// @param truthTable the truth table to be commited
    /// @return the commit structure generated
    function generate(bytes32 commit, bool[3][4] memory truthTable) public view returns(Commit memory) {
        address owner = msg.sender;
        address previousCommitOwner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    /// @notice Generate the first commit structure
    /// @param commit bytes32 from the commit
    /// @param previousCommitOwner indicates who owns the first commit
    /// @param truthTable the truth table to be commited
    /// @return the commit structure generated
    function generate(bytes32 commit, address previousCommitOwner, bool[3][4] memory truthTable) public view returns(Commit memory) {
        address owner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    /// @notice Verify if the information provided matches the commit
    /// @param value bytes32 from the commit to be verified
    /// @param nonce the nonce used to generate the commit
    /// @param inversion_bits the inversion bits used to generate the commit
    /// @param encryption_bits the encryption bits used to generate the commit
    /// @return bool indicating if the information matches the commit
    function verify(bytes32 value, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public pure returns(bool) {
        bytes32 generatedValue = sha256(abi.encodePacked(nonce, inversion_bits, encryption_bits));
        return value == generatedValue;
    }

    /// @notice Verify if the commit is the first one
    /// @param commit the commit to be verified
    /// @return bool indicating if the commit provided is the first
    function isFirstCommit(Commit memory commit) public pure returns(bool) {
        return commit.owner == commit.previous;
    }
}