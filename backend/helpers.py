def to_lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower(): to_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_lowercase(item) for item in obj]
    elif isinstance(obj, str):
        return obj.lower()
    else:
        return obj