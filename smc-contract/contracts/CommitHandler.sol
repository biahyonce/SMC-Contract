pragma solidity ^0.8.0;

library CommitHandler {
    struct Commit {
        address owner;
        address previous;
        bytes32 commit;
        bool[3][4] truthTable;
    }

    function generate(bytes32 commit, bool[3][4] memory truthTable) public view returns(Commit memory) {
        address owner = msg.sender;
        address previousCommitOwner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    function generate(bytes32 commit, address previousCommitOwner, bool[3][4] memory truthTable) public view returns(Commit memory) {
        address owner = msg.sender;
        return Commit(owner, previousCommitOwner, commit, truthTable);
    }

    function verify(bytes32 value, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public pure returns(bool) {
        bytes32 generatedValue = sha256(abi.encodePacked(nonce, inversion_bits, encryption_bits));
        return value == generatedValue;
    }

    function isFirstCommit(Commit memory commit) public pure returns(bool) {
        return commit.owner == commit.previous;
    }
}