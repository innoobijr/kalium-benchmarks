#!/usr/bin/python

import sys
import math

def main():
    f = open(sys.argv[1], "r")
    s1 = 0.0
    n1 = 0.0
    s = f.readlines()
    for line in s:
        l = line.strip("\n")
        p = float(l[:-1])
        if p < 5.00:
            s1 += p
            n1 += 1
    avg = s1 / n1
    stdev = 0
    for line in s:
        l = line.strip("\n")
        p = float(l[:-1])
        if p < 5.00:
            stdev += ((p - avg) ** 2)
    stdev = math.sqrt(stdev / (n1 - 1))
    print ("Avg: %f, Stdev: %f" % (avg, stdev))


if __name__ == "__main__":
    main()
