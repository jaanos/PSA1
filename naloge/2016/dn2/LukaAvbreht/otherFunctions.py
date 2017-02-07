

def primeren_otrok(parent,child):
    """It returns true if the ciycle child can ba a neighbour cycle of parent (input is in string in binary)"""
    k = len(parent)
    assert k != len(child), \
        "Parent and child must be of same size"
    for i in range(k):
        if parent[i] != child[i]:
            return False
    return True

def list_primernih_otrok(pranet):
    """Returns the list of all valid children of a parent as a set of binary numbers"""
