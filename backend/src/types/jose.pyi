from typing import Any, Dict, List

class jwt:
    @staticmethod
    def encode(to_encode: Dict[str, Any], secret_key: str, algorithm: str) -> str: ...
    @staticmethod
    def decode(
        token: str, secret_key: str, algorithms: List[str]
    ) -> Dict[str, Any]: ...

JWTError = Exception
