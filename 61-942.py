
def perm(s):
    n = len(s)
    list_n = [x for x in range(0, n + 1)]
    perm_list = []
    for i in range(0, n):
        el = None
        if s[i] == "I": 
            el = min(list_n)
            perm_list.append(el)
        else: 
            el = max(list_n)
            perm_list.append(el)
        list_n.remove(el)
        if i == n - 1:  perm_list.append(list_n[-1])
    return perm_list


print(perm("IDID"))