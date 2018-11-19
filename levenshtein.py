#! /usr/bin/python3
import argparse

def levenshtein(s, t):
    """
    For all i and j, d[i,j] will contain the Levenshtein
    distance between the first i characters of source string s and the
    first j characters of target string t
    :param s:  source string
    :param t: target string
    :return: Levenshtein matrix needed for backtracing, where cell in last row and last column contains Levenshtein distance
    """
    rows = len(s)+1
    cols = len(t)+1
    d = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(1, rows):
        d[i][0] = i
    for k in range(1, cols):
        d[0][k] = k
    for i in range(1, rows):
        for k in range(1, cols):
            if s[i - 1] == t[k - 1]:
                cost = 0
            else: cost = 1
            d[i][k] = min(d[i - 1][k - 1] + cost,
                        d[i - 1][k] + 1,
                        d[i][k - 1] + 1)
    return d

def trace_operations(s, t, d):
    """
        Reconstructs the path of minimum editing operations
        :param s: source string
        :param t: target string
        :param d: Levenshtein matrix
        :return: list that stores the path
    """
    backtrace = []
    i = len(s)
    k = len(t)
    while not (i<=0 and k<=0):
        values = [d[i-1][k-1], d[i][k-1], d[i-1][k]]
        minimum = values.index(min(values))
        if minimum == 0:
            operation = s[i-1]+":"+t[k-1] #substitution or no edit
            i -= 1
            k -= 1
        elif minimum == 1:
            operation = ":"+t[k-1] #insertion
            k -= 1
        elif minimum == 2:
            operation = s[i-1]+":" #deletion
            i -= 1
        backtrace.insert(0, operation)
    return backtrace


### main processing ###

arg_parser = argparse.ArgumentParser(description='Computes the minimum number of editing operations needed to transform one string into another')
arg_parser.add_argument('wordpairs', type=str, help='a file containing the pairs of source and target strings')
args = arg_parser.parse_args()

with open(args.wordpairs) as wordpairs:
    for pair in wordpairs:
        s, t = pair.strip().split("\t")
        d = levenshtein(s, t)
        backtrace = trace_operations(s, t, d)
        print(s, t, d[-1][-1])
        print(" ".join(backtrace), "\n")
