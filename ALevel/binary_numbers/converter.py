def denary_to_binary(dec):
    dec = int(dec)
    digits_needed = 0
    digits_found = False
    while not digits_found:
        digits_needed += 1
        if 2**digits_needed > dec:
            digits_found = True

    headers = [2**i for i in range(digits_needed - 1, -1, -1)]

    binstr = ""
    for power in headers:
        if dec >= power:
            dec += - power
            binstr += "1"
        else:
            binstr += "0"

    return binstr


def binary_to_denary(binary):
    binary = binary[::-1]
    h = 0
    denary = 0
    for digit in binary:
        if digit == '1':
            denary += 2**h
        h += 1
    return denary


def binary_to_denarjy(binary):
    max_power = len(str(binary))
    current_heading = 2**max_power
    denary = 0
    for digit in str(binary):
        current_heading = current_heading / 2
        if digit == "1":
            denary += current_heading
        elif digit == "0":
            denary += 0
        else:
            return -1

    return int(denary)


def twoscomplement_to_denary(binary):
    binary = str(binary)
    max_power = len(str(binary))
    current_heading = 2**max_power
    denary = 0

    if str(binary)[0] == "1":
        denary += -1* current_heading
    for digit in binary:
        current_heading = current_heading / 2
        if digit == "1":
            denary += current_heading
        elif digit == "0":
            denary += 0
        else:
            return -1

    return int(denary)


def denary_to_twoscomplement(denary):
    denary = str(denary)
    if denary[0] == "-":
        denary = str(int(denary) + 1)
        denary = denary[1:]
        binary = denary_to_binary(denary)
        reverse = ""
        for digit in binary:
            if digit == "1":
                reverse = reverse + "0"
            elif digit == "0":
                reverse = reverse + "1"

        reverse = "1" + reverse
        return (reverse)
    else:
        return(denary_to_binary(denary))


def binary_to_hex(binary):
    nibble_to_digit = {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3", "0100": "4",
        "0101": "5", "0110": "6", "0111": "7", "1000": "8", "1001": "9",
        "1010": "A", "1011": "B", "1100": "C", "1101": "D", "1110": "E", "1111": "F"
    }
    binary = str(binary)
    zeros_to_add = (4 - (len(binary) % 4)) % 4
    binary = "0"*zeros_to_add + binary

    hexnum = ""
    for n in range(int(len(binary) / 4)):
        nibble = binary[4*n: 4*n+4]
        digit = nibble_to_digit[nibble]
        hexnum = hexnum + digit

    return(hexnum)


def hex_to_binary(hex):
    binary = ""
    for char in str(hex):
        nibble_to_digit = {
            "0":"0000", "1":"0001", "2":"0010", "3":"0011", "4":"0100",
            "5":"0101", "6":"0110", "7":"0111", "8":"1001", "9":"1010",
            "A":"1011", "B":"0111", "C":"1000", "D":"1001", "E":"1011", "F":"1111"
        }
        binary += nibble_to_digit[char]
    return (binary)


def hex_to_denary(hex):
    return binary_to_denary(hex_to_binary(hex))


def denary_to_hex(denary):
    return binary_to_hex(denary_to_binary(denary))


def floating_to_denary(floating, mantissa_length, exponent_length):
    if len(floating) != mantissa_length + exponent_length:
        return False
    current_heading = 1
    man = floating[:mantissa_length]
    exp = floating[mantissa_length:]
    exp = twoscomplement_to_denary(exp)
    if man[0] == "0":
        count = 0
        power = 1
        for digit in man:
            if digit == "1":
                count += 1/power
            power *= 2
        man = count
        return(man*(2**exp))
    elif man[0] =="1":
        count = -1
        power = 1
        for digit in man[1:]:
            power *= 2
            if digit == "1":
                count -= 1/power
        man = count
        return(man*(2**exp))


    else:
        return False
