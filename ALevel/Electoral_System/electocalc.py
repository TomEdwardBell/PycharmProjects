import random
import random_name
from numpy.random import normal
import matplotlib.pyplot as plt
import house_visualiser as vis
from sys import argv
from PyQt5 import QtWidgets, QtGui, QtCore
import csv2electocalc

class Region(list):
    def __init__(self):
        super(Region, self).__init__()
        self.name = random_name.region()
        self.candidates = []
        self.election_results = []
        self.winner = None

    def population(self):
        return len(self)

    def __str__(self):
        return self.name


class Voter():
    def __init__(self, region = None):
        super(Voter, self).__init__()
        self.candidate_rankings = []
        self.fav_party = []
        self.region = region
        if region is None:
            self.leaning = gen_leanings()
        else:
            self.leaning = gen_leanings()
            self.leaning = self.leaning[0] + region.bias[0], self.leaning[1] + region.bias[1]


    def rank_candidates(self, cands):
        cand_leanings = [cand.leaning for cand in cands]
        cand_distances = [self.distance_from(cl) for cl in cand_leanings]

        cd_to_cands = dict(zip(cand_distances, cands))
        #^^ Generates a list of each candidate and how for away from them they are on each leaning

        sorted_cd = cand_distances.copy()
        sorted_cd.sort()
        rankings = []
        for num in sorted_cd:
            rankings.append(cd_to_cands[num])

        self.candidate_rankings = rankings
        #print([c.name for c in rankings])
        return rankings
        # Returns the candidates :)

    def distance_from(self, leanings):
        x = (self.leaning[0] - leanings[0])**2
        y = (self.leaning[1] - leanings[1])**2
        dist = (x + y)**0.5
        return dist


class Party:
    def __init__(self):
        self.name = random_name.party()
        self.color = gen_random_color()
        self.leaning = gen_leanings()


class Candidate():
    def __init__(self, region, party = None):
        super(Candidate, self).__init__()
        self.name = random_name.full()
        self.party = party
        self.region = region
        if party == None:
            party = Party()
            party.name = "Independent"
            self.party = party
            self.leaning = gen_leanings()
            self.color = gen_random_color()
        else:
            personal_leaning = gen_leanings(0.2)
            party_leanjing = gen_leanings(0.8)
            self.leaning = party.leaning[0] + personal_leaning[0], party.leaning[1]+ personal_leaning[1]
            self.color = party.color

    def show_repview(self):
        vis.view_rep(self)


class House(list):
    def __init__(self, voting_system):
        super(House, self).__init__() # It is a list of the regions it contains
        self.name = ""


        self.voting_system = voting_system  # This is a class-type, not an object
        self.repcount = 0
        self.reps = []

        self.population = 0

    def run(self):
        if self.voting_system is None:
            return None
        else:
            for region in self:
                vot = self.voting_system(region)
                vot.run()
                self.reps.append(region.winner)

    def print_reps(self):
        max_regionname = str(max(len(region.name) for region in self))
        max_winnername = str(max(len(region.winner.name) for region in self))
        max_partyname  = str(max(len(region.winner.party.name) for region in self))
        for region in self:
            preformat = ("{:"+max_regionname+"} - {:"+max_winnername+"} - {:"+max_partyname+"}")
            print(preformat.format(region.name, region.winner.name, region.winner.party.name))


class AV:
    def __init__(self, region): 
        self.rounds = []
        self.rounds_voters = []
        self.region = region

    def display_round(self, round):
        self.sort_round(round)
        dic = self.rounds[round]
        string = ""
        for cand in dic:
            string += ("{}:{}".format(cand,dic[cand])) + "\n"
        return string

    def display(self):
        string = ""
        string += "Election for: " + self.region.name + "\n"
        for round in range(len(self.rounds) - 1):
            string += "-------ROUND {}-------\n".format(round + 1) + self.display_round(round)
        return  string

    def sort_round(self, round):
        dic = self.rounds[round]
        scores = []
        for name in dic:
            scores.append(dic[name])
        scores.sort()
        scores.reverse()
        new_dic = {}
        for score in scores:
            for name in dic:
                if dic[name] == score:
                    new_dic[name] = score
        self.rounds[round] = new_dic

    def run(self):
        self.rounds = []
        prefs = []

        pref_count = [[] for i in range(len(self.region.candidates))]
        # Each candidate starts with 0 votes
        # A vote is represented by the candidate's ranking list

        cands = self.region.candidates
        cand_count = len(cands)
        round = 0

        # Abstracts votes for into a list of numbers
        voter_num = -1
        for voter in self.region:
            voter_num += 1
            prefs.append([])

            # For each candidate that they've ranked

            if type(voter) == Voter:
                for cand in voter.candidate_rankings:
                    # Add the number that represents that candidate to their pref list is prefs
                    prefs[voter_num].append(cands.index(cand))
            elif type(voter) == list: # Accepts voters not being the "voter" object, but instead just being a list of candidates
                for cand in voter:
                    # Add the number that represents that candidate to their pref list is prefs
                    prefs[voter_num].append(cands.index(cand))


        removed = [False for i in range(cand_count)]
        finished_election = [[] for i in range(cand_count)]

        # Round 1 (round 0)
        # Adds that voters ballot to the "pref_count" list of their first choice candidate
        for voter in prefs:
            pref_count[voter[0]].append(voter)

        # Convert info from round into the named vote counts
        self.rounds.append({})
        for cand_num in range(cand_count):
            # For each candidate number
            self.rounds[0][cands[cand_num]] = len(pref_count[cand_num])
            # ^^ The number of votes that the voter has in the current round
            # Is equal to the number of ballots in their part of the pref_count list

        while pref_count != finished_election:
            # Checks if any candidate has a majority (The it's an insta-win)
            # Commented out because I want the user to see each round
            #majority = len(self.region)
            #for cand_num in range(cand_count):
            #    if len(pref_count[cand_num]) >= majority:
            #        self.winner = cands[cand_num]
            #        return self.winner

            # Find the least popular
            for cand_num in range(cand_count):
                if not removed[cand_num]:
                    least_popular = cand_num

            for cand_num in range(cand_count):
                if len(pref_count[cand_num]) < len(pref_count[least_popular]) and not removed[cand_num]:
                    least_popular = cand_num

            # Remove them
            removed[least_popular] = True

            # Goes through each voter and moves their choice to the next candidate that has not been removed
            for voter in pref_count[least_popular]:
                newchoice = -1
                for choice in voter:
                    if not removed[choice]:
                        newchoice = choice
                        break
                if newchoice != -1:
                    pref_count[newchoice].append(voter)
            pref_count[least_popular] = []

            round += 1
            # Convert info from round into the named vote counts
            self.rounds.append({})
            for cand_num in range(cand_count):
                # For each candidate number
                if not removed[cand_num]: # If the candidate isnt removed
                    self.rounds[round][cands[cand_num]] = len(pref_count[cand_num])
                    # ^^ The number of votes that the candidate has in the current round
                    # Is equal to the number of ballots in their part of the pref_count list

        self.region.winner = cands[least_popular]

        round += 1
        # Move onto the next round

        return self.region.winner
        # The winner is the last person who is "least popular"

    def show_results(self):
        prefs = {}
        for cand in self.region.candidates:
            prefs[cand] = []
        for voter in self.region:
            prefs[voter.rank_candidates(self.region.candidates)[0]].append(voter)
        for cand in self.region.candidates:
            cand_color = cand.color
            vlx = [v.leaning[0] for v in prefs[cand]]
            vly = [v.leaning[1] for v in prefs[cand]]
            plt.scatter(vlx, vly, c=cand_color, s=3, alpha=0.4)
            plt.scatter([cand.leaning[0]], [cand.leaning[1]], c=cand_color, edgecolors='black', s=10)
        plt.show()


class FPTP:
    def __init__(self, region):
        self.region = region
        self.winner = None
        self.scores = {}

    def run(self):
        for cand in self.region.candidates:
            self.scores[cand] = 0
        for voter in self.region:
            if type(voter) == Voter:
                self.scores[voter.candidate_rankings[0]] += 1
            elif type(voter) == list:
                self.scores[voter[0]] += 1
        highest = self.region.candidates[0]
        for cand in self.region.candidates:
            if self.scores[cand] > self.scores[highest]:
                highest = cand
        self.region.winner = highest
        return  self.region.winner

    def display(self):
        self.sort()
        string = ""
        string += "Region Of: " + self.region.name +"\n"
        string += '---------FPTP---------\n'
        for cand in self.scores:
            string += cand.name + ": " + str(self.scores[cand]) + '\n'
        string += '----------------------\n'
        string += 'Winner: '+self.winner.name + '\n'
        return  string

    def sort(self):
        dic = self.scores.copy()
        scores = []
        for name in dic:
            scores.append(dic[name])
        scores.sort()
        scores.reverse()
        new_dic = {}
        for score in scores:
            for name in dic:
                if dic[name] == score:
                    new_dic[name] = score
        self.scores = new_dic


def gen_region(population = 10000, candidate_count = 5):
    region = Region()
    for c in range(candidate_count):
        region.candidates.append(Candidate(region))
    region_cands = region.candidates.copy
    for p in range(population):
        v = Voter()
        v.rank_candidates(region_cands())
        region.append(v)

    return region

def gen_house(population = 400000, region_count = 40, party_count = 5):
    house = House(None)
    parties = []
    ppr = population // region_count # ppr = Population Per Region
    party_colors = ["#D10000", "#0000FF", "#FFCF00",  "#00D827",
                    # Red         Blue      Yellow     Green
                    "#FF7D00", "#020049", "#606060", "#00b9f2", "#144C00",
                    # Orange    Navy         Grey     Light Blue   Dark Green
                    "#890034", "#8C5100"
                    #Dark-Rose  Brown
                    ]

    for i in range(party_count):
        parties.append(Party())
        if party_colors is not []:
            parties[i].color = party_colors.pop(0)
    for reg_num in range(region_count):
        r = Region()
        r.bias = gen_leanings(0.3)
        house.append(r)
        house[reg_num].candidates = [Candidate(r, party) for party in parties]
        # Adds a candidate to that region's candidate list
        # This region's party' candidate's leaning is the same as their parties leaning
        # But it does slightly change this as each candidate within a party is different

        for p in range(ppr):
            v = Voter(r)
            v.rank_candidates(house[reg_num].candidates)
            v.leaning = v.leaning[0] + r.bias[0], v.leaning[1] + r.bias[1]
            # ^^ Regional biases

            house[reg_num].append(v)
    return house

def gen_random_color():
    color = "#"
    nums = [random.randint(0, 127), random.randint(128, 255), random.randint(0, 255)]
    random.shuffle(nums)

    color = '#%02x%02x%02x' % (nums[0], nums[1], nums[2])
    return color

def gen_leanings(factor = 1.0):
    x = normal() * factor
    y = normal() * factor
    return x,y

class Test():
    def __init__(self):
        self.h = csv2electocalc.load_election('miniGE.csv')
        self.h.voting_system = FPTP
        self.h.run()
        self.h.print_reps()
        self.v = vis.view_house(self.h)


def main():
    app = QtWidgets.QApplication(argv)
    t = Test()
    app.exec_()


if __name__ == '__main__':
    main()



