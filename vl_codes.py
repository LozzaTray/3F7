from math import log2, ceil

def shannon_fano(p):

    # Sort probs in decreasing order and remove zeroes
    p = dict(sorted([(a,p[a]) for a in p if p[a]>0.0], key = lambda el: el[1], reverse = True))
    f = [0] # cumulative prob

    for a in p:
        f.append(f[-1] + p[a])

    f.pop() # remove final entry =1
    f = dict([(a,mf) for a,mf in zip(p,f)]) # convert to dictionary f : a -> lower bound

    # assign the codewords
    code = {} # initialise as an empty dictionary
    for a in p: # for each probability
        length = ceil(log2(1/p[a]))

        codeword = [] # initialise current codeword
        myf = f[a]

        for pos in range(length):
            # multiply myf by 2 (shifting it "left" in binary)
            myf = myf * 2

            if(myf > 1): # implies > 0.5 => 1 in MSB
                codeword.append(1)
                myf = myf - 1
            else:
                codeword.append(0)

        code[a] = codeword # assign the codeword
        
    return code # return the code table


def huffman(p):
    """
    Returns huffman code from probability dictionary
    p = {'symbol': Pr(symbol)}
    """
    # xt = [[parent_index, [children_indices_array], node_label]
    xt = [[-1,[], a] for a in p]
    # p = [(xt_index, prob)]
    p = [(k,p[a]) for k,a in zip(range(len(p)),p)] 

    # arbitrary intermediate node label
    nodelabel = len(p)

    # run until p array is of length one
    # each pass merges two least probable nodes
    while len(p) > 1:
        # sort probabilities in ascending order >> p[0] & p[1] are least probablr
        p = sorted(p, key = lambda el: el[1])

        # append new node labelled nodeLabel with no parent or children
        xt.append([-1, [], str(nodelabel)])
        nodelabel += 1

        # get indices
        parent_index = len(xt) - 1
        left_child_index = p[0][0]
        right_child_index = p[1][0]

        # link children to parent
        xt[left_child_index][0] = parent_index
        xt[right_child_index][0] = parent_index
        
        # link parent to children
        xt[parent_index][1] = [left_child_index, right_child_index]

        # add new node to p with summed prob and remove 2 children
        p.append((parent_index, p[0][1] + p[1][1]))
        p.pop(0)
        p.pop(0)
        
    return(xt)



def bits2bytes(x):
    n = len(x)+3
    r = (8 - n % 8) % 8
    prefix = format(r, '03b')
    x = ''.join(str(a) for a in x)
    suffix = '0'*r
    x = prefix + x + suffix
    x = [x[k:k+8] for k in range(0,len(x),8)]
    y = []
    for a in x:
        y.append(int(a,2))

    return y

def bytes2bits(y):
    x = [format(a, '08b') for a in y]
    r = int(x[0][0:3],2)
    x = ''.join(x)
    x = [int(a) for a in x]
    for k in range(3):
        x.pop(0)
    for k in range(r):
        x.pop()
    return x


def vl_encode(x, c):
    y = []
    for a in x:
        y.extend(c[a])
    return y


def vl_decode(y, xt):
    x = []
    root = [k for k in range(len(xt)) if xt[k][0]==-1]
    if len(root) != 1:
        raise NameError('Tree with no or multiple roots!')
    root = root[0]
    leaves = [k for k in range(len(xt)) if len(xt[k][1]) == 0]

    n = root
    for k in y:
        if len(xt[n][1]) < k:
            raise NameError('Symbol exceeds alphabet size in tree node')
        if xt[n][1][k] == -1:
            raise NameError('Symbol not assigned in tree node')
        n = xt[n][1][k]
        if len(xt[n][1]) == 0: # it's a leaf!
            x.append(xt[n][2])
            n = root
    return x

