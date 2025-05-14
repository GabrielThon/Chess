def is_valid_string_square(string : str):
    if len(string) != 2:
        return False

    columns = ['a','b','c','d','e','f','g','h']
    if string[0] not in columns :
        return False

    if not string[1].isdigit():
        return False
    row = int(string[1])
    rows = range(1,9,1)
    if row not in rows :
        return False

    return True

def is_valid_color(color : str):
    if color.lower() == "white" or color.lower() == "black":
        return True
    return False

if __name__ == "__main__":
    print(is_valid_string_square("a1"))
    print(is_valid_string_square("h8"))
    print(is_valid_string_square("randomstring"))
    print(is_valid_string_square("a0"))
    print(is_valid_string_square("a9"))
    print(is_valid_string_square("i2"))