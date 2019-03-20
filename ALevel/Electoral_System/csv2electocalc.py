#!/usr/bin/env python
# -*- coding: utf-8 -*-

import electocalc as e
import openpyxl
import math

def load_election(filename):
    file = open(filename)

    region_code = ""
    cand = None
    finished = False
    row_num = 4
    house = e.House(e.FPTP)
    parties = {} # Party name: e.Party() object

    count = 0
    for raw_row in file:
        row = raw_row.split(",")
        region_name = row[2]
        cand_name = row[4] + " " + row[3].capitalize()
        party_name = row[6]
        votes = int(row[7])

        if row[0] != region_code:
            # If we've moved on to a new region
            region_code = row[0]
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

        for v in range(votes): # Gets the number of votes for that candidate
            region.append([cand]) # Add to region
        count += 1
        print(count/ 3300)

    return house

