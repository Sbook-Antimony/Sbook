
def parse(obj, data):
    i = 0
    while i < len(data):
        c = data[i]
        if c.isspace():
            i += 1
            continue
        if c == '<'