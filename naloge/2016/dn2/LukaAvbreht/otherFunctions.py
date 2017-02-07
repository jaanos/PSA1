

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
            res = tren
        else:
            for j in range(k):
                tren.append(res[j]+'1')
                tren.append(res[j]+'0')
            k = k*2
            res = tren
    return res


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
