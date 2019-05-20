#!/usr/bin/env python
# -*- coding: utf-8 -*-

import electocalc as e
import openpyxl
import math
import random

def load_election(filename):
    file = open(filename)

    current_region_code = ""
    cand = None
    finished = False
    row_num = 4
    house = e.House(e.FPTP)
    parties = {} # Party name: e.Party() object
    lines = file.readlines()[1:]
    cands = len(lines)

    count = 0
    for row in lines:
        row = row.split(",")
        region_name = row[2]
        cand_name = row[4] + " " + row[3].capitalize()
        party_name = row[6]
        votes = int(row[7])

        if row[0] != current_region_code:
            # If we've moved on to a new region
            current_region_code = row[0]
            region = e.Region()
            region.name = region_name
            house.append(region)


        # Make that candidate
        cand = e.Candidate(region)
        region.candidates.append(cand)
        # Add it to the region

        # Name
        cand.name = cand_name

        # Party Name
        if party_name in parties: # if we've seen the party before
            cand.party = parties[party_name] # Add the to that party
        else:
            new_party = e.Party()  # Creates a new party
            parties[party_name] = new_party
            new_party.name = party_name
            cand.party = new_party
        for v in range(votes// 10): # Gets the number of votes for that candidate
            region.append([cand]) # Add to region
        count += 1
        print(round(count/ cands *100,1),"%", sep="")



    return house

def gen_party_colors(num):
    c = []
    for i in range(num):
        h = i / num
        s = 1
        v = 0.8
        c.append(hsv_to_rgb(h, s, v))
        print(c)
    return c

def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    
    if i == 0: color =  (v, t, p)
    if i == 1: color =  (q, v, p)
    if i == 2: color =  (p, v, t)
    if i == 3: color =  (p, q, v)
    if i == 4: color =  (t, p, v)
    if i == 5: color =  (v, p, q)

    r ,g ,b = color
    r = str(hex(int(r*255)))[2:]
    g = str(hex(int(g*255)))[2:]
    b = str(hex(int(b*255)))[2:]
    if len(r) == 1: r = "0" + r
    if len(g) == 1: g = "0" + g
    if len(b) == 1: b = "0" + b
    color = "#{}{}{}".format(r,g,b)
    return color