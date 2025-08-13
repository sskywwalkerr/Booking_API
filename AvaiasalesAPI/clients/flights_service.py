import hashlib


def generate_signature(params: dict, secret: str) -> str:
    """Генерация подписи для запроса в Aviasales"""
    sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    data_str = f"{sorted_params}&{secret}"
    return hashlib.md5(data_str.encode()).hexdigest()