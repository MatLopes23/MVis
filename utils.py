
def get_only_name_method(key):
    start = key.find("::") + 2 if key.find("::") != -1 else 0
    end = key.find("(") if key.find("(") != -1 else len(key)

    return key[start:end] + '()'