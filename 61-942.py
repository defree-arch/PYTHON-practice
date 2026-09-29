
def perm(s):
    n = len(s)
    low, high = 0, n
    perm_list = []
    
    for i in s:
        el = None
        if i == "I": 
            el = low
            low += 1
        else: 
            el = high
            high -= 1
        perm_list.append(el)
    perm_list.append(low)
    return perm_list


print(perm("IDID"))