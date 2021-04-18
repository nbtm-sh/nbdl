import string, random

def random_string(length):
    return ''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase) for _x in range(length)])

def to_int(input_string):
    combo = string.ascii_lowercase + string.ascii_uppercase
    output = 0
    for l, c in zip(input_string, range(len(input_string))):
        l_val = combo.index(l)
        output += l_val * (pow(len(combo), c))
    
    return output