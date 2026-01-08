class RedisKeys:

    @staticmethod
    def access(jti: str) -> str:
        return f"jwt:access:{jti}"

    @staticmethod
    def refresh(jti: str) -> str:
        return f"jwt:refresh:{jti}"
