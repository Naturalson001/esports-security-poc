import hashlib


class HashedData:

    @staticmethod
    def generate_hash(data: str) -> str:
        return HashedData._hash(data)

    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def verify_data(input_data: str, stored_hash: str) -> bool:
        return HashedData._hash(input_data) == stored_hash