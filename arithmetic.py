from math import floor, ceil
from sys import stdout as so
from bisect import bisect


def encode(x, p):

    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter

    p = dict([(a, p[a]) for a in p if p[a] > 0])

    # compute cumulative prob of lower bounds
    f = [0.0]
    for a in p:
        f.append(f[-1]+p[a])
    f.pop()

    f = dict([(a, mf) for a, mf in zip(p, f)])

    y = []  # initialise output list
    lo, hi = 0, one  # initialise lo and hi to be [0,1.0)
    straddle = 0  # initialise the straddle counter to 0

    for k in range(len(x)):  # for every symbol

        # arithmetic coding is slower than vl_encode, so we display a "progress bar"
        # to let the user know that we are processing the file and haven't crashed...
        if k % 100 == 0:
            so.write('Arithmetic encoded %d%%    \r' %
                     int(floor(k/len(x)*100)))
            so.flush()

        lohi_range = hi - lo + 1
        a = x[k]
        lo = lo + int(ceil(f[a]*lohi_range))
        hi = lo + int(floor(p[a]*lohi_range))

        if (lo == hi):
            raise NameError('Zero interval!')

        # re-scale interval if endpoints have bits in common
        while True:
            if hi < half:  # if lo < hi < 1/2
                y.append(0)
                y.extend([1] * straddle)
                straddle = 0

            elif lo >= half:  # if hi > lo >= 1/2
                y.append(1)
                y.extend([0] * straddle)
                straddle = 0
                lo = lo - half
                hi = hi - half

            elif lo >= quarter and hi < threequarters:  # if 1/4 < lo < hi < 3/4
                straddle = straddle + 1
                lo = lo - quarter
                hi = hi - quarter

            else:
                break  # we break the infinite loop if the interval has reached an un-stretchable state

            # stretch interval by 2
            lo = lo * 2
            hi = hi * 2 + 1  # +1 is magical

    # termination bits
    # after processing all input symbols, flush any bits still in the 'straddle' pipeline
    # adding 1 to straddle for "good measure" (ensures prefix-freeness)
    straddle += 1
    if lo < quarter:
        y.append(0)
        y.extend([1] * straddle)
    else:
        y.append(1)
        y.extend([0] * straddle)

    return(y)


def decode(y, p, n):
    precision = 32
    one = int(2**precision - 1)
    quarter = int(ceil(one/4))
    half = 2*quarter
    threequarters = 3*quarter

    p = dict([(a, p[a]) for a in p if p[a] > 0])

    alphabet = list(p)
    f = [0]
    for a in p:
        f.append(f[-1]+p[a])
    f.pop()

    p = list(p.values())

    y.extend(precision*[0])  # dummy zeros to prevent index out of bound errors
    x = n*[0]  # initialise all zeros

    # initialise by taking first 'precision' bits from y and converting to a number
    value = int(''.join(str(a) for a in y[0:precision]), 2)
    y_position = precision  # position where currently reading y
    lo, hi = 0, one

    x_position = 0
    while 1:
        if x_position % 100 == 0:
            so.write('Arithmetic decoded %d%%    \r' %
                     int(floor(x_position/n*100)))
            so.flush()

        lohi_range = hi - lo + 1
        a = bisect(f, (value-lo)/lohi_range) - 1
        x[x_position] = alphabet[a]

        lo = lo + int(ceil(f[a]*lohi_range))
        hi = lo + int(floor(p[a]*lohi_range))
        if (lo == hi):
            raise NameError('Zero interval!')

        while True:
            if hi < half:
                # do nothing
                pass
            elif lo >= half:
                lo = lo - half
                hi = hi - half
                value = value - half
            elif lo >= quarter and hi < threequarters:
                lo = lo - quarter
                hi = hi - quarter
                value = value - quarter
            else:
                break
            lo = 2*lo
            hi = 2*hi + 1
            value = 2*value + y[y_position]
            y_position += 1
            if y_position == len(y):
                break

        x_position += 1
        if x_position == n or y_position == len(y):
            break

    return(x)


if __name__ == "__main__":
    from setup import hamlet, p, Nin
    arith_encoded = encode(hamlet, p)
    arith_decoded = decode(arith_encoded, p, Nin)
    print('\n'+''.join(arith_decoded[:255]))
