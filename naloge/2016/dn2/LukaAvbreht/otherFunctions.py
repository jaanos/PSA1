

def primeren_otrok(parent,child):
    """It returns true if the ciycle child can ba a neighbour cycle of parent (input is in string in binary)"""
    k = len(parent)
    assert k == len(child), \
        "Parent and child must be of same size"
    for i in range(k):
        if parent[i] == child[i] == 1:
            return False
    return True

def list_primernih_otrok(parent):
    """Returns the list of all valid children of a parent as a list of binary numbers(strings)"""
    assert valid_cycle(parent) == True, "Parent is not the valid cycle"
    if parent[0] == '1':
        res = ['0']
        k = 1
    else:
        res = ['1','0']
        k = 2
    for i in parent[1:]:
        tren = list()
        if i =='1':
            for j in range(k):
                tren.append(res[j]+'0')
        else:
            dif = 0
            for j in range(k):
                if res[j][-1]=='1':
                    tren.append(res[j]+'0')
                    dif += 1
                else:
                    tren.append(res[j]+'1')
                    tren.append(res[j]+'0')
            k = k*2-dif
        res = tren
    tren = list()
    for i in res:
        if valid_cycle(i):
            tren.append(i)
    return tren

def valid_cycle(cycle):
    """Returns True if a cycle is valid and False othervise (Cycle is valid ifi it has an independent subgroup of ones)"""
    for i in range(len(cycle)-1):
        if cycle[i] == '1':
            if cycle[i-1] != '0' or cycle[i+1] != '0':
                return False
    return True

def are_neighbours(a,b,T):  # aLso returns false if you compere by
    """Returns True if two nodes are neighbours, otherwise returns False"""
    x,u = a[0],a[1]
    y,v = b[0],b[1]
    Cikelsos = abs((x-y)%k)
    if u == v and Cikelsos <= 1:
        return True
    Drevosos = u in T[v]
    if Cikelsos == 0 and Drevosos:
        return True
    return False

def all_valid_cycles(n):
    """Returns the list of all valid cycles of length n"""
    return list_primernih_otrok('0'*n)


