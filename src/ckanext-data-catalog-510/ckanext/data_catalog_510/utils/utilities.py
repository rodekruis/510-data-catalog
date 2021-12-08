def endsWith(string: str, suffix_list: list):
    for suffix in suffix_list:
        if string.endswith(suffix):
            return True
    return False