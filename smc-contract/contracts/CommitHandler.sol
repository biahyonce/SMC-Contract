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

    /*
    function verify(bytes32 value, bytes memory nonce, bool[2] memory inversionBits, bool[4] memory encryptionBits) public pure returns(bool) {
        // check if abi.encode will make difference
        bytes32 generatedValue = sha256(abi.encode(nonce,inversionBits[0], inversionBits[1], 
                                                         encryptionBits[0], encryptionBits[1], encryptionBits[2], encryptionBits[3]));
        return value == generatedValue;
    }
    */

    function verify(bytes32 value, bytes memory nonce, bytes memory inversion_bits, bytes memory encryption_bits) public pure returns(bytes32) {
        bytes32 generatedValue = sha256(abi.encodePacked(nonce));
        return generatedValue;
    }

    function isFirstCommit(Commit memory commit) public pure returns(bool) {
        return commit.owner == commit.previous;
    }
}