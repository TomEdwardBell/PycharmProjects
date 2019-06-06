import random
import random_name
import time, datetime


class Region(list):
    def __init__(self):
        super(Region, self).__init__()
        self.name = random_name.region()
        self.candidates = []
        self.elections = []
        self.bias = (0, 0)
        self.winner = None

    def population(self):
        return len(self)

    def __str__(self):
        return self.name

    def setName(self, name):
        self.name = str(name)

    def setPopulation(self, newpop):
        if newpop < self.population():
            [self.pop(0) for i in range(self.population() - newpop)]
        elif newpop > self.population():
            increase = newpop - self.population()
            self.addVoters(increase)
        elif newpop == self.population():
            pass

    def addVoters(self, number=1):
        voters = [Voter(self) for v in range(number)]
        self += voters

    def addCandidates(self, number = 1):
        self.candidates += [Candidate() for c in range(number)]

    def population(self):
        return len(self)


class Voter():
    def __init__(self, region=None):
        super(Voter, self).__init__()
        self.candidate_rankings = []
        self.fav_party = []
        self.region = region
        if region is None:
            self.leaning = gen_leanings()
        else:
            self.leaning = gen_leanings()
            self.leaning = self.leaning[0] + region.bias[0], self.leaning[1] + region.bias[1]

    def rank(self, objs):  # objs can be parties or candidates
        distances = {o: self.distance_from(o.leaning) for o in objs}
        order = []
        candsleft = list(objs)
        while candsleft != []:
            least = candsleft[0]  # You want to first rank the candidate with the LEAST distance from you
            for cand in candsleft:
                if distances[cand] < distances[least]:
                    least = cand
            candsleft.remove(least)
            order.append(least)
        return order

    def distance_from(self, leanings):
        x = (self.leaning[0] - leanings[0]) ** 2
        y = (self.leaning[1] - leanings[1]) ** 2
        return (x + y) ** 0.5


class Party:
    def __init__(self, name=None):
        if name == None:
            self.name = random_name.party()
        else:
            self.name = name
        self.color = gen_random_color()
        self.check_color()

        self.leaning = gen_leanings()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def gen_list(self, n):
        list = []
        for i in range(n):
            list.append(Candidate(self))
        return list

    def check_color(self):
        party_colors = {"Labour": "#DC241F", "Conservative": "#0087DC", "SNP": "#FEF987",
                        "Liberal Democrats": "#FAA61A",
                        "DUP": "#D46A4C", "Sinn Fein": "#326760", "Green Party": "#6AB023",
                        "Plaid Cymru": "#008142"}

        if self.name in party_colors:
            self.color = party_colors[self.name]


class Candidate():
    def __init__(self, party=None):
        super(Candidate, self).__init__()
        self.name = random_name.full()
        self.party = party
        if party == None:
            party = Party()
            party.name = "Independent"
            self.party = party
            self.leaning = gen_leanings()
            self.color = gen_random_color()
        else:
            personal_leaning = gen_leanings(0.2)
            self.leaning = party.leaning[0] * 0.8 + personal_leaning[0], party.leaning[1] * 0.8 + personal_leaning[1]
            self.color = party.color

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def display_info(self):
        print(self.info())

    def info(self):
        return self.name + ": " + self.party.name


class Nation(list):
    def __init__(self):
        super(Nation, self).__init__()  # It is a list of the regions it contains
        self.name = "Country"
        self.parties = []
        self.elections = []

    def print_reps(self):
        max_regionname = str(max(len(region.name) for region in self))
        max_winnername = str(max(len(region.winner.name) for region in self))
        max_partyname = str(max(len(region.winner.party.name) for region in self))
        for region in self:
            preformat = ("{:" + max_regionname + "} - {:" + max_winnername + "} - {:" + max_partyname + "}")
            print(preformat.format(region.name, region.winner.name, region.winner.party.name))

    def party_count(self):  # Returns a dictionary of each party and how many seats they have
        p = {}
        for region in self:
            if region.winner.party in p:
                p[region.winner.party] += 1
            else:
                p[region.winner.party] = 1
        return p

    def party_reps(self):  # Returns a dictionary of each party and all there MPs
        p = {}
        for region in self:
            if region.winner.party in p:
                p[region.winner.party].append(region.winner)
            else:
                p[region.winner.party] = [region.winner]
        return p

    def add_regions(self, count, mean_population, population_variance=0):
        for a in range(count):
            r = Region()
            r.bias = random.normalvariate(0, 0.2), random.normalvariate(0, 0.2)
            r.addVoters(abs(int(random.normalvariate(mean_population, population_variance))))

    def add_party(self, party):
        self.parties.append(party)

class NationElection():
    def __init__(self, nation):
        self.nation = nation
        self.regionalelections = []
        self.seats = []
        self.voting_system = None

        self.electiondate = datetime.datetime.now().isoformat()

        nation.elections.append(self)

    def av(self, representatives_per_region):
        self.voting_system = "av"
        rpr = representatives_per_region

    def fptp(self):
        self.voting_system = "fptp"
        for region in self.nation:
            re = RegionElection(region)
            re.fptp(region.candidates)
            self.seats += re.seats
            self.regionalelections.append(re)

    def display_info(self):
        print("Election in: "+ self.nation.name +" at "+ self.electiondate)
        for re in self.regionalelections:
            print("  "+re.region.name)
            for winner in re.seats:
                print("   -",winner.info())

class RegionElection():
    def __init__(self, region):
        self.region = region
        self.rounds = []
        self.party_seatcount = {}
        self.seats = []
        self.votingsystem = None

    def divisor(self, partylists, seat_number, divisors):
        self.rounds = []
        self.party_seatcount = {}
        self.seats = []
        seats = []

        # partylists is a dictionary, {party:[list of candidates (in order)]}
        # Seat number is the number of seats that region will send to the parliament

        # Get each voters preferences of the Parties
        parties = partylists.keys()
        ballots = []

        # Make a dict party:[candidate_list]

        partyvotes = self.collect_vote(parties)
        # {party: number of votes}

        # Make a dict, party:seat_number (by default 0)
        party_seatswon = {party: 0 for party in parties}

        # WHILE len(seats) < seat_number

        original_party_votes = partyvotes.copy()
        while len(seats) < seat_number:
            self.rounds.append(partyvotes.copy())
            # Find party with most votes
            most_votes = list(parties)[0]
            for party in partyvotes:
                if partyvotes[party] > partyvotes[most_votes]:
                    most_votes = party

            self.rounds[-1]["_winner"] = most_votes

            # Add the parties next candidate to the seats list
            seats.append(partylists[most_votes][party_seatswon[most_votes]])

            # set that parties votes to (number of original votes for that party)*(divisors[seat_number])
            partyvotes[most_votes] = int(
                round(original_party_votes[most_votes] * divisors[party_seatswon[most_votes]], 0))
            # Increase party:seats dict by 1
            party_seatswon[most_votes] += 1


        # Return the list of candidates
        # Set attributes
        self.region.elections.append((self.votingsystem, self.rounds))
        self.party_seatcount = party_seatswon
        self.seats = seats
        return seats

    def dhont(self, party_lists, seat_count):
        self.votingsystem = "dhont"
        divisors = [1 / (x + 2) for x in range(seat_count)]
        return self.divisor(party_lists, seat_count, divisors)

    def webster(self, party_lists, seat_count):
        self.votingsystem = "webster"
        divisors = [1 / (2 * x + 3) for x in range(seat_count)]
        return self.divisor(party_lists, seat_count, divisors)

    def collect_vote(self, cands):
        # Give a list of candidates / parties
        # returns a dict of {party: number of votes}
        votes = {cand: 0 for cand in cands}
        for voter in self.region:
            votes[voter.rank(cands)[0]] += 1
        return votes

    def av(self, cands, seat_count=1):
        self.votingsystem = "av"
        ballot_count = {}
        # Dictionary
        # {[list of candidates in order of preference] : number of people who voted that way}

        for voter in self.region:
            voter_ranking = tuple(voter.rank(cands))
            if voter_ranking in ballot_count:
                ballot_count[voter_ranking] += 1
            else:
                ballot_count[voter_ranking] = 1

        running = cands.copy()  # Candidates still in the race
        eliminated = []
        votes = {cand: 0 for cand in cands}
        # {candidate: number of people whose highest ranked non-elimineated canidate is that candidate}

        seats = []
        while len(running) > seat_count:
            votes = {cand: 0 for cand in running}  # Resets votes

            # Find top candidate that's running
            for ballot in ballot_count:
                current_pref = ballot[0]
                # The voters current vote is set fot their no.1 choice
                prefnumber = 0
                while current_pref not in running:
                    # Goes through their preferences to find their highest ranked candidate that's still running
                    prefnumber += 1
                    current_pref = ballot[prefnumber]
                votes[current_pref] += ballot_count[ballot]
                # add the number of times that ballot has been used to the votes for that candidate

            # Add results to self.rounds
            self.rounds.append(votes.copy())

            # Find least popular candidate
            least = list(votes.keys())[0]
            for candidate in running:
                if votes[candidate] < votes[least]:
                    least = candidate

            # Remove them
            running.remove(least)
            self.rounds[-1]["_loser"] = least
            seats = running


        self.region.elections.append((self.votingsystem, self.rounds))
        return seats

    def fptp(self, cands):
        self.votingsystem = "fptp"
        votes = {cand: 0 for cand in cands}
        total_votes = 0
        for voter in self.region:
            fav = voter.rank(cands)[0]
            votes[fav] += 1
            total_votes += 1

        self.rounds = [votes.copy()]
        # Adds voter percentages
        self.rounds.append({cand: str(round(votes[cand]*100 / total_votes, 3)) + "%" for cand in votes})
        highest = cands[0]
        for cand in votes:
            if votes[cand] > votes[highest]:
                highest = cand

        self.rounds[0]["_winner"] = highest

        self.region.elections.append((self.votingsystem, self.rounds))
        self.seats = [highest]
        return highest

def gen_region(population=10000, candidate_count=5):
    region = Region()
    for c in range(candidate_count):
        region.candidates.append(Candidate())
    region_cands = region.candidates.copy
    for p in range(population):
        v = Voter()
        v.rank(region_cands())
        region.append(v)

    return region


def gen_nation(population=400000, region_count=40, party_count=5):
    nation = Nation()
    parties = []
    ppr = population // region_count  # ppr = Population Per Region
    party_colors = ["#D10000", "#0000FF", "#FFCF00", "#00D827",
                    # Red         Blue      Yellow     Green
                    "#FF7D00", "#020049", "#606060", "#00b9f2", "#144C00",
                    # Orange    Navy         Grey     Light Blue   Dark Green
                    "#890034", "#8C5100"
                    # Dark-Rose  Brown
                    ]

    for i in range(party_count):
        parties.append(Party())
        if len(party_colors) == 0:
            parties[i].color = party_colors.pop(0)
    for reg_num in range(region_count):
        r = Region()
        r.bias = gen_leanings(0.3)
        nation.append(r)
        nation[reg_num].candidates = [Candidate(party) for party in parties]
        # Adds a candidate to that region's candidate list
        # This region's party' candidate's leaning is the same as their parties leaning
        # But it does slightly change this as each candidate within a party is different

        for p in range(ppr):
            v = Voter(r)
            v.rank(nation[reg_num].candidates)
            v.leaning = v.leaning[0] + r.bias[0], v.leaning[1] + r.bias[1]
            # ^^ Regional biases

            nation[reg_num].append(v)
    return nation


def gen_random_color():
    color = "#"
    nums = [random.randint(0, 127), random.randint(128, 255), random.randint(0, 255)]
    random.shuffle(nums)

    color = '#%02x%02x%02x' % (nums[0], nums[1], nums[2])
    return color


def gen_leanings(factor=1.0):
    x = random.normalvariate(0, factor)
    y = random.normalvariate(0, factor)
    return x, y
