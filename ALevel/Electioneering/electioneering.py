import random
import random_name
import time, datetime


class Region(list):
    # Region is a list filled with Voter
    def __init__(self):
        super(Region, self).__init__()
        self.name = random_name.region()
        # Region's name

        self.candidates = []
        # List of all of the candidates that will stand at the next election

        self.elections = []
        # List of all the the Election objects that have taken place

        self.bias = (0, 0)
        # Some regions have particular leanings
        # This number here accounts for it
        self.gen_bias()

        self.reps = []

        self.reps_to_send = 1
        # How many representatives this region sends to house

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

    def gen_bias(self):
        self.bias = gen_leanings(0.3)

    def population(self):
        return len(self)

    def combine(self, r2):
        # Combines this region with another region
        # Allowing you to combine multiple regions
        r1 = self

        # Sorting out names, if a region has "and" in its name
        if " and " in r1.name:
            r1.name = ", ".join(r1.name.split(" and "))
            if " and " in r2.name:
                self.name = r1.name + ", " + r2.name
            else:
                self.name = r1.name + " and " + r2.name
        elif "and" in r2.name:
            self.name = r1.name + ", " + r2.name
        else:
            self.name = self.name + ' and ' + r2.name



        r1pop = r1.population()
        r2pop = r2.population()
        totalpop = r1pop + r2pop
        for voter in r2:
            self.append(voter)


        # Incase one of the regions has a population of 0
        if r1pop == 0 and r2pop == 0:
            self.bias = (r1.bias[0]*0.5 + r2.bias[0]*0.5, r1.bias[1]*0.5 + r2.bias[1]*0.5)
        elif r1pop == 0: self.bias = r2.bias
        elif r2pop == 0: self.bias = r1.bias
        else:
            # Generates bias by taking a weighted average of the two regions
            # E.g. if one region has a larger population it also has a larger bias
            self.bias = (r1.bias[0] * (r1pop/totalpop) + r2.bias[0]*(r2pop/totalpop),
                         r1.bias[1] * (r1pop/totalpop) + r2.bias[1]*(r2pop/totalpop))

        self.reps.append(r2.reps)
        self.reps_to_send += r2.reps_to_send


class Voter():
    def __init__(self, region=None):
        self.candidate_rankings = []
        self.fav_party = []
        self.region = region
        if region is None:
            self.leaning = gen_leanings()
        else:
            self.leaning = gen_leanings()
            self.leaning = self.leaning[0] + region.bias[0], self.leaning[1] + region.bias[1]

    def rank(self, objs):  # objs can be parties or candidates (any object with a .leaning)
        supports = {o: self.support(o) for o in objs}
        return sorted(supports, key=supports.get)

    def distance_from(self, leanings):
        x = (self.leaning[0] - leanings[0]) ** 2
        y = (self.leaning[1] - leanings[1]) ** 2
        return (x + y) ** 0.5

    def support(self, obj):
        # Works out how much you support a particular party or candidate (obj)
        # Accounts form how far away your politcal views are from them
        # Then uses relevance to work out how much the voter supports the object

        if obj.relevance != 0:
            return self.distance_from(obj.leaning) / obj.relevance
        else:
            return 99999


class Party:
    def __init__(self, name=None):
        if name is None:
            self.name = random_name.party()
        else:
            self.name = name
        self.color = gen_random_color()
        self.check_color()

        self.leaning = gen_leanings()
        self.relevance = 1
        # ^ How politically relevant they are
        #   The higher the relevance the more likely people are to vote for your party
        #   Accounts for the fact that some parties have a wider support than others

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def gen_list(self, n):
        # Generates list of candidates from the party for a Dhont or Webset election
        return [Candidate(self) for c in range(n)]

    def check_color(self):
        party_colors = {'Labour': '#DC241F', 'Conservative': '#0087DC', 'SNP': '#FEF987',
                        'Liberal Democrats': '#FAA61A',
                        'DUP': '#D46A4C', 'Sinn Fein': '#326760', 'Green Party': '#6AB023',
                        'Plaid Cymru': '#008142', 'Independent': '#555555'}
        # Some parties already have colours, like these ones

        if self.name in party_colors:
            self.color = party_colors[self.name]


class Candidate():
    def __init__(self,  **kwargs):
        super(Candidate, self).__init__()
        self.name = random_name.full()

        self.relevance = 1
        # ^ How politically relevant they are
        #   The higher the relevance the morel likely people are to vote for you

        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'party' in kwargs:
            self.party = kwargs['party']
            personal_leaning = gen_leanings(0.2)
            self.leaning = self.party.leaning[0] * 0.8 + personal_leaning[0], self.party.leaning[1] * 0.8 + personal_leaning[1]
            # ^ Their leaning is like their party's leaning with some variation
            self.color = self.party.color
            self.relevance = self.party.relevance
        else:
            self.party = Party()
            self.party.name = 'Independent'
            self.leaning = gen_leanings()
            self.party.leaning = self.leaning
            self.party.color = "#CCCCCC"

        if 'region' in kwargs:
            self. region = kwargs['region']
        else:
            self.region = Region()
        if 'relevance' in kwargs:
            self.relevance = kwargs['relevance']


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def display_info(self):
        print(self.info())

    def info(self):
        return self.name + ': ' + self.party.name


class Nation(list):
    def __init__(self):
        super(Nation, self).__init__()  # It is a list of the regions it contains
        self.name = 'Country'
        self.parties = []
        self.elections = []

    def reps(self):
        reps = []
        # Returns a list of all of the representatives
        for region in self:
            for rep in region.reps:
                reps.append(rep)
        return reps

    def print_reps(self):
        reps = self.reps()

        max_repname = str(max(len(rep.name) for rep in reps))
        max_partyname = str(max(len(rep.party.name) for rep in reps))
        max_regionname = str(max(len(region.name) for region in self))

        for rep in reps:
            # {:10} means the .format() has to be 10 charachters long
            preformat = ('{:' + max_repname + '} - {:' + max_partyname + '} - {:' + max_regionname + '}')
            # preformat looks like '{:10} - {:10} - {:10}

            print(preformat.format(rep.name, rep.party, rep.region))
            # Looks like Rep Name - Party - Region

    def party_count(self):  # Returns a dictionary of each party and how many seats they have
        p = {}
        for rep in self.reps():
            if rep.party in p:
                p[rep.party] += 1
            else:
                p[rep.party] = 1
        return p

    def party_reps(self):  # Returns a dictionary of each party and all their Reps
        p = {}
        for rep in self.reps():
            if rep.party in p:
                p[rep.party].append(rep)
            else:
                p[rep.party] = [rep]

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
        self.voting_system = 'av'
        rpr = representatives_per_region


    def fptp(self):
        self.voting_system = 'fptp'
        for region in self.nation:
            re = RegionElection(region)
            re.fptp(region.candidates)
            self.seats += re.seats
            self.regionalelections.append(re)

    def display_info(self):
        print('Election in: '+ self.nation.name +' at '+ self.electiondate)
        for re in self.regionalelections:
            print('  '+re.region.name)
            for reps in re.seats:
                for rep in reps:
                    print('   -',rep.info())


class RegionElection():
    class Round():
        def __init__(self):
            self.roundnum = 0
            self.winners = []
            self.losers = []
            self.votingsystem = None
            self.votes = {}
            self.percentage  = {}

        def candidates(self):
            return list(self.votes.keys())
        
        def parties(self):
            return list(self.votes.keys())

    class Votes(list):
        def __init__(self):
            super(RegionElection.Votes, self).__init__()

        def rank(self):
            # Returns a list of canidadates in order of how well they did
            return sorted(self.pref_votes(), key=self.pref_votes().get)[::-1]


        def find_order(self, order):
            for ballot in self:
                if ballot.order == order:
                    return(ballot)
            return False


        def check_dupes_for(self, check_ballot):
            old = self.total_votes()

            # Checks if any duplicate ballots exist for a particular order of candidates
            order = check_ballot.order
            ballots_to_delete = []
            for ballot in self:
                if ballot.order == order:
                    ballots_to_delete.append(ballot)

            for ballot in ballots_to_delete:
                check_ballot.votes += ballot.votes
                ballot.votes = 0
                self.remove(ballot)
                del(ballot)


        def add_vote(self, order, num, eliminated=[]):
            for ballot in self:
                filtered_order = list(filter(lambda x: x not in eliminated, ballot.order))
                if filtered_order == order:
                    ballot.order = filtered_order
                    ballot.votes += num
                    return None
            self.append(RegionElection.Ballot(order, num))

        def total_votes(self):
            v = 0
            for ballot in self:
                v += ballot.votes
            return v

        def pref_votes(self, cands):
            pref_count = {cand: 0 for cand in cands}
            for ballot in self:
                if not ballot.empty():
                    pref_count[ballot.pref()] += ballot.votes
            return pref_count

        def filter(self, removed):
            orders = {}
            ballots = self.copy()
            for ballot in ballots:
                print(random.randint(0, 10))
                ballot.order = tuple(filter(lambda x: x not in removed, ballot.order))
                if tuple(ballot.order) in orders:
                    joint_ballot = orders[ballot.order]
                    joint_ballot.votes += ballot.votes
                    ballot.votes = 0
                    self.remove(ballot)
                    del(ballot)
                else:
                    orders[ballot.order] = ballot

        def ballots_by_first_pref(self):
            # Returns a dictionary of ballots
            # {candidate: [every ballot with that prefered candidate on it]
            v = {}
            for ballot in self:
                if ballot.pref() in v:
                    v[ballot.pref()].append(ballot)
                else:
                    v[ballot.pref()] = [ballot]
            return v

    class Ballot():
        def __init__(self, order = [], votes = 0):
            self.order = order
            self.votes = votes

        def pref(self):
            if not self.empty():
                return self.order[0]
            else: return None

        def setVotes(self, v):
            self.votes = v

        def addVotes(self, v):
            self.votes += v

        def removeVotes(self, v):
            self.votes -= v
            if self.votes < 0:
                self.votes = 0

        def filter(self, removed):
            self.order = list(filter(lambda x: x not in removed, self.order))

        def empty(self):
            return len(self.order) == 0


    def __init__(self, region):
        self.region = region
        self.rounds = []
        self.party_seatcount = {}
        self.seats = []
        self.votingsystem = None
        self.order = []

    def av(self, cands):
        # Alternative vote
        self.votingsystem = 'av'
        ballot_count = {}
        # Dictionary
        # {[list of candidates in order of preference] : number of people who voted that way}
        # ^ Not list of candidates, but list of a specific order of candidates

        self.order = []
        # ^^ Order the candidates came in (from best to worst)

        for voter in self.region:
            voter_ranking = tuple(voter.rank(cands))
            if voter_ranking in ballot_count:
                ballot_count[voter_ranking] += 1
            else:
                ballot_count[voter_ranking] = 1

        running = cands.copy()  # Candidates still in the race
        # {candidate: number of people whose highest ranked non-elimineated canidate is that candidate}

        seats = []
        while len(running) > self.region.reps_to_send:

            # Create a new Round object for this round
            self.rounds.append(RegionElection.Round())
            r = self.rounds[-1]
            # Set voting system
            r.votingsystem = self.votingsystem

            votes = {cand: 0 for cand in running}  # Number of votes reset each round

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
            r.votes = votes.copy()
            # Find least popular candidate
            least = list(votes.keys())[0]
            for candidate in running:
                if votes[candidate] < votes[least]:
                    least = candidate
            # Remove them
            r.losers = [least]
            self.order.insert(0, least)
            running.remove(least)
            seats = running


        self.order = seats + self.order
        self.region.elections.append(self)
        self.region.reps = seats
        return seats

    def stv(self, cands):
        def save_round(**kwargs):
            r = self.Round()
            r.votingsystem = "stv"
            self.rounds.append(r)
            r.roundnum = len(self.rounds)
            if "winner" in kwargs: r.winner = kwargs['winner']
            if "loser" in kwargs: r.loser = kwargs['loser']
            if "votes" in kwargs: r.votes = kwargs['votes']

        self.votingsystem = "stv"
        self.rounds = []

        votes = RegionElection.Votes()
        total_votes = len(self.region)

        for voter in self.region:
            order = voter.rank(cands)
            votes.add_vote(order, 1)

        seat_num = self.region.reps_to_send
        won = []
        eliminated = []
        running = cands.copy()

        # Quota
        quota = total_votes / (seat_num + 1)

        # While the number of winners < the number of people we want to elect
        while len(won) < seat_num:
            finish_round = False
            # Count votes
            prefs = votes.pref_votes(cands)

            # Save round
            self.rounds.append(RegionElection.Round())
            self.rounds[-1].votes = votes.pref_votes(cands)

            # See if the number of remaining candidates = the number of seats left to fill
            if len(running) == seat_num - len(won):
                # Set all of these cands as winners
                for cand in running:
                    self.rounds[-1].winners.append(cand)
                    won.append(cand)
                    running.remove(cand)
                # Skip the rest of the while loop
                finish_round = True
            if finish_round:
                continue



            # Go through each candidate
            for cand in running:
                # If they're over the quota
                if prefs[cand] >= quota:
                    # Add them as winners
                    won.append(cand)
                    self.rounds[-1].winners = [cand]
                    running.remove(cand)
                    # Find out number of excess votes
                    surplus = prefs[cand] - quota
                    # Find out proportion of votes that are over that quota
                    surplus_proportion = surplus / prefs[cand]
                    # Get every ballot with that cand as option one
                    cand_ballots = votes.ballots_by_first_pref()[cand]
                    for ballot in cand_ballots:
                        # Find the number of votes that need to be moved
                        votes_to_move = ballot.votes * surplus_proportion
                        # Remove the excess votes from the ballot
                        ballot.removeVotes(votes_to_move)
                        # Create a new order with eliminated candidates removed
                        new_order = list(filter(lambda x: x in running, ballot.order))
                        # Add those votes
                        votes.add_vote(new_order, votes_to_move, eliminated + won)
                    # Skip the rest of the while loop's iteration
                    finish_round = True
                    continue
            if finish_round: continue


            if running == []:
                print("here")
                continue
            # Find lowest ranked candidate thats still running
            loser = running[0]
            for cand in prefs:
                if cand in running and prefs[cand] < prefs[loser]:
                    loser = cand

            # Set them as round loser
            self.rounds[-1].losers = [loser]
            eliminated.append(loser)
            running.remove(loser)
            # Get every ballot with that cand as option one
            cand_ballots = votes.ballots_by_first_pref()[loser]
            # Filter the votes to get rid of removed candidates
            for ballot in cand_ballots:
                # Find the number of votes that need to be moved
                votes_to_move = ballot.votes
                # Set number of votes for that ballot to 0
                ballot.removeVotes(votes_to_move)
                # Create a new order with that candidate removed
                new_order = list(filter(lambda x: x in running, ballot.order))
                # Add the redristributed votes to the Votes object
                votes.add_vote(new_order, votes_to_move, eliminated + won)

        self.region.reps = won
        self.region.elections.append(self)
        self.order = won + running + eliminated
        return won

    def fptp(self, cands):
        self.votingsystem = 'fptp'
        votes = {cand: 0 for cand in cands}
        # Each candidate starts with 0 votes
        total_votes = 0
        for voter in self.region:
            fav = voter.rank(cands)[0]
            # Every voter votes for their favourite candidate
            votes[fav] += 1
            total_votes += 1

        self.rounds = [self.Round()]
        # Adds votes
        self.rounds[0].votes = {cand: round(votes[cand]) for cand in votes}
        self.rounds[0].percentages = {cand: round(votes[cand]*100 / total_votes, 4) for cand in votes}

        # Find highest ranked cand
        highest = self.rank_dict(votes)[0]
        self.rounds[0].winners = [highest]


        self.region.elections.append(self)
        self.seats = [highest]
        self.region.reps = [highest]
        return [highest]

    def borda(self, cands):
        self.votingsystem = "borda"
        # Uses a points based system
        # Your least fav candidate gets one point
        # Your second least fav gets two, etc
        # Total points added, top candidate selected
        # Only works to elect one candidate
        cand_points = {cand: 0 for cand in cands}
        for voter in self.region:
            rank = voter.rank(cands)
            point = 1
            for cand in rank[::-1]:
                cand_points[cand] += point
                point += 1

        # Finding winner
        highest = self.rank_dict(cand_points)[0]

        # Add the round to self.rounds
        self.rounds = [RegionElection.Round()]
        self.rounds[0].votes = cand_points.copy()
        self.rounds[0].votingsystem = self.votingsystem
        self.rounds[0].winners = [highest]

        self.region.reps = [highest]
        self.region.elections.append(self)
        return [highest]

    def dhont(self, party_lists):
        # A divisor based voting system
        # Party with the most votes earns a seat
        # The number of votes they now have is equal to:
        #     number of votes they had originally) / (number of seats they now have +1)
        self.votingsystem = 'dhont'
        divisors = [1 / (x + 2) for x in range(self.region.reps_to_send)]
        return self.divisor(party_lists, self.region.reps_to_send, divisors)

    def dowdall(self, cands):
        self.votingsystem = "dowdall"
        # Also a points based system
        # Fav candidate gets 1 point
        # Second fav gets 1/2 a point, etc
        # Can elect more than one candidate
        cand_points = {cand: 0 for cand in cands}
        for voter in self.region:
            rank = voter.rank(cands)
            point = 1
            for cand in rank:
                cand_points[cand] += 1/point
                point += 1

        # Finding winner
        winners = self.rank_dict(cand_points)[0:self.region.reps_to_send]
        # Rounds system
        self.rounds = [RegionElection.Round()]
        self.rounds[0].votes = cand_points.copy()
        self.rounds[0].votingsystem = self.votingsystem
        self.rounds[0].winners = winners

        self.region.reps = winners
        self.region.elections.append(self)
        return winners

    def webster(self, party_lists):
        # A divisor based voting system
        # But with a slightly different set of divisors
        self.votingsystem = 'webster'
        divisors = [1 / (2 * x + 3) for x in range(self.region.reps_to_send)]
        return self.divisor(party_lists, self.region.reps_to_send, divisors)

    def divisor(self, partylists, seat_number, divisors):
        # Divisor based elections like Dhont or Webster

        self.rounds = []
        self.party_seatcount = {}
        self.seats = []
        seats = []

        # partylists is a dictionary, {party:[list of candidates (in order)]}
        # Seat number is the number of seats that region will send to the parliament

        # Get each voters preferences of the Parties
        parties = partylists.keys()

        # Make a dict party:[candidate_list]

        partyvotes = self.collect_vote(parties)
        # {party: number of votes}

        # Make a dict, party:seat_number (by default 0)
        party_seatswon = {party: 0 for party in parties}

        # WHILE len(seats) < seat_number
        original_party_votes = partyvotes.copy()
        while len(seats) < seat_number:
            self.rounds.append(RegionElection.Round())
            r = self.rounds[-1]
            r.votingsystem = self.votingsystem
            r.votes = partyvotes.copy()

            # Find party with most votes
            most_votes = self.rank_dict(partyvotes)[0]

            # Add the parties next candidate to the seats list
            seats.append(partylists[most_votes][party_seatswon[most_votes]])
            r.winners = [partylists[most_votes][party_seatswon[most_votes]]]

            # set that parties votes to (number of original votes for that party)*(divisors[seat_number])
            # As you get more seats the number of votes you have decreases
            partyvotes[most_votes] = int(
                round(original_party_votes[most_votes] * divisors[party_seatswon[most_votes]], 0))

            # Increase party:seats dict by 1
            party_seatswon[most_votes] += 1


        # Return the list of candidates
        # Set attributes
        self.region.elections.append(self)
        self.party_seatcount = party_seatswon
        self.seats = seats
        return seats

    def rank_dict(self, dict):
        # Returns a sorted list of all of the keys in the dictionry
        # Sorted by the values in the dictionary
        return sorted(dict, key=dict.get)[::-1]

    def collect_vote(self, cands):
        # Give a list of candidates / parties
        # returns a dict of {party: number of votes}
        # Only one vote of that person's favourite candidate
        votes = {cand: 0 for cand in cands}
        for voter in self.region:
            votes[voter.rank(cands)[0]] += 1
        return votes


def gen_region(population=10000, candidate_count=5):
    region = Region()
    region.candidates = [Candidate() for c in candidate_count]
    for p in range(population):
        v = Voter()
        region.append(v)

    return region

def gen_nation(population=400000, region_count=40, party_count=5):
    nation = Nation()
    parties = []
    ppr = population // region_count  # ppr = Population Per Region
    party_colors = ['#D10000', '#0000FF', '#FFCF00', '#00D827',
                    # Red         Blue      Yellow     Green
                    '#FF7D00', '#020049', '#606060', '#00b9f2', '#144C00',
                    # Orange    Navy         Grey     Light Blue   Dark Green
                    '#890034', '#8C5100'
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
    color = '#'
    nums = [random.randint(0, 127), random.randint(128, 255), random.randint(0, 255)]
    random.shuffle(nums)

    color = '#%02x%02x%02x' % (nums[0], nums[1], nums[2])
    return color

def gen_leanings(factor=1.0):
    x = random.normalvariate(0, factor)
    y = random.normalvariate(0, factor)
    return x, y

if __name__ == '__main__':
    r = Region()
    r.addVoters(100000)
    r.reps_to_send = 5
    e = RegionElection(r)
    print(e.stv([Candidate(relevance=random.randint(1,3)) for i in range(99)]))



