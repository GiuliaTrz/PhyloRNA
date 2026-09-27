
def safe_int(value, default=-1):
    if value is None or value == '':
        return default
    try:
        return int(value)
    except:
        return default
