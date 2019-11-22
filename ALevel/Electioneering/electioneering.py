import random
import random_name
import datetime


class Region:
    def __init__(self, **kwargs):
        self.voters = []

        self.name = kwargs.get('name', random_name.region())


        self.elections = []
        # List of all the the Election objects that have taken place

        self.bias = kwargs.get('bias',  self.gen_bias())

        self.reps = kwargs.get('reps', [])

        self.seat_count = kwargs.get('seat_count', 1)
        # How many representatives this region sends to parliament

        if 'parties' in kwargs:
            self.local_parties = kwargs['parties']
        else:
            self.local_parties = []

        if 'nation' in kwargs:
            self.nation = kwargs['nation']
            if self.nation not in self.nation.regions():
                self.nation.add_region(self)
        else:
            self.nation = None

        if 'population' in kwargs:
            self.add_voters(kwargs['population'])

    def parties(self):
        if self.nation is not None:
            return self.local_parties + self.nation.parties
        else:
            return self.local_parties

    def create_local_parties(self, number):
        self.local_parties += [Party() for i in range(number)]

    def population(self):
        return len(self.voters)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __len__(self):
        return self.population()

    def set_name(self, name):
        self.name = str(name)

    def set_population(self, newpop):
        if newpop < self.population():
            [self.voters.pop(0) for i in range(self.population() - newpop)]
        elif newpop > self.population():
            increase = newpop - self.population()
            self.add_voters(increase)
        elif newpop == self.population():
            pass

    def add_voters(self, number=1):
        for v in range(number):
            self.voters.append(Voter(region=self))

    def set_bias(self, bias):
        if self.bias != bias:
            self.bias = bias
            pop = self.population()
            self.set_population(0)
            # Resets the population but with the new bias
            self.set_population(pop)

    def gen_bias(self):
        self.bias = (0, 0)
        self.set_bias(gen_leaning(0.6))
        return self.bias

    def combine(self, r2):
        # Combines this region with another region
        # Allowing you to combine multiple regions
        r1 = self

        # Sorting out names, if a region has 'and' in its name
        if ' and ' in r1.name:
            r1.name = ', '.join(r1.name.split(' and '))
            if ' and ' in r2.name:
                self.name = r1.name + ', ' + r2.name
            else:
                self.name = r1.name + ' and ' + r2.name
        elif 'and' in r2.name:
            self.name = r1.name + ', ' + r2.name
        else:
            self.name = self.name + ' and ' + r2.name

        r1pop = r1.population()
        r2pop = r2.population()
        totalpop = r1pop + r2pop
        for voter in r2:
            self.voters.append(voter)

        # In case one of the regions has a population of 0
        if r1pop == 0 and r2pop == 0:
            self.bias = (r1.bias[0]*0.5 + r2.bias[0]*0.5, r1.bias[1]*0.5 + r2.bias[1]*0.5)
        elif r1pop == 0:
            self.bias = r2.bias
        elif r2pop == 0:
            self.bias = r1.bias
        else:
            # Generates bias by taking a weighted average of the two regions
            # E.g. if one region has a larger population it also has a larger bias
            self.bias = (r1.bias[0] * (r1pop/totalpop) + r2.bias[0]*(r2pop/totalpop),
                         r1.bias[1] * (r1pop/totalpop) + r2.bias[1]*(r2pop/totalpop))

        self.reps.append(r2.reps)
        self.seat_count += r2.seat_count

    def add_party(self, party=None):
        if party is None:
            party = Party()
        party.region = self
        self.local_parties.append(party)

    def __iter__(self):
        return self.voters.__iter__()


class Voter:
    def __init__(self, region=None):
        self.region = region
        if region is None:
            self.leaning = gen_leaning()
        else:
            self.leaning = gen_leaning()
            self.leaning = self.leaning[0] + region.bias[0], self.leaning[1] + region.bias[1]

    def rank(self, objs):  # objs can be parties or candidates (any object with a .leaning)
        supports = {o: self.support(o) for o in objs}
        return sorted(supports, key=supports.get)

    def distance_from(self, leaning):
        x = (self.leaning[0] - leaning[0]) ** 2
        y = (self.leaning[1] - leaning[1]) ** 2
        return (x + y) ** 0.5

    def support(self, obj):
        # Works out how much you support a particular party or candidate (obj)
        # Accounts form how far away your political views are from them
        # Then uses relevance to work out how much the voter supports the object

        if obj.relevance != 0:
            return self.distance_from(obj.leaning) / obj.relevance
        else:
            return 99999


class Party:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = random_name.party()

        if 'color' in kwargs:
            self.color = kwargs['color']
        else:
            self.color = gen_random_color()

        if 'leaning' in kwargs:
            self.leaning = kwargs['leaning']
        else:
            self.leaning = gen_leaning()

        if 'relevance' in kwargs:
            self.relevance = kwargs['relevance']
        else:
            self.relevance = 1
        # ^ How politically relevant they are
        #   The higher the relevance the more likely people are to vote for your party
        #   Accounts for the fact that some parties have a wider support than others

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def gen_list(self, n, region=None):
        # Generates list of candidates from the party for a dhondt or Webster election
        if region is None:
            return [Candidate(party=self) for c in range(n)]
        else:
            return [Candidate(party=self, region=region) for c in range(n)]


    def check_color(self):
        party_colors = {'Labour': '#DC241F', 'Conservative': '#0087DC', 'SNP': '#FEF987',
                        'Liberal': '#FAA61A', 'Socialist': '#FF0000', 'Communist': '#FF0000',
                        'DUP': '#D46A4C', 'Sinn Fein': '#326760', 'Green': '#6AB023',
                        'Plaid Cymru': '#008142', 'Independent': '#555555'}
        # Some parties already have colours, like these ones

        for color_name in party_colors:
            if color_name in self.name:
                self.color = party_colors[color_name]
                return True
        return False

    def initials(self):
        if self.name == 'Independent':
            return 'IND'
        words = self.name.replace('-',' ')
        words = words.split(' ')
        initials = ''
        for word in words:
            if word.lower() not in ['the', 'for', 'of', 'and']:
                initials += word[0].upper()
            elif word.lower() not in ['the']:
                initials += word[0].lower()
            if word[-1] == '!':
                initials += word[-1]
        return initials


class Candidate:
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
            personal_leaning = gen_leaning(0.2)
            self.leaning = self.party.leaning[0] * 0.8 + personal_leaning[0], self.party.leaning[1] * 0.8 + personal_leaning[1]
            # ^ Their leaning is like their party's leaning with some variation
            self.color = self.party.color
            self.relevance = self.party.relevance
        else:
            self.party = Party()
            self.party.name = 'Independent'
            self.leaning = gen_leaning()
            self.party.leaning = self.leaning
            self.party.color = '#CCCCCC'

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


class Nation:
    def __init__(self, **kwargs):
        super(Nation, self).__init__()  # It is a list of the regions it contains

        self.map_width = kwargs.get('map_width', 10)
        self.map_height = kwargs.get('map_height', 10)

        self.region_map = [[None for y in range(self.map_height)] for x in range(self.map_width)]

        self.parties = kwargs.get('parties', [])

    def print_reps_by_party(self):
        rbp = self.reps_by_party()
        order = sorted(rbp.keys(), key=rbp.get)[::-1]
        for party in order:
            print(f'{party} ({party.initials()}): {rbp[party]}')

    def mean_population(self):
        if len(self.regions()) != 0:
            return int(self.population() / len(self.regions()))
        else:
            return 1000

    def free_spaces(self):
        frees = []
        for x in range(self.map_width):
                for y in range(self.map_height):
                    if self.region_map[x][y] is None:
                        frees.append((x, y))

        return frees

    def add_party(self, party):
        self.parties.append(party)
        party.nation = self

    def add_regions(self, regions):
        for region in regions:
            self.add_region(region)

    def add_region(self, region=None, x=None, y=None):
        if region is None:
            region = Region(population=self.mean_population())
        region.nation = self

        if self.is_full() and x is None and y is None:
            self.resize_map(self.map_width + 1, self.map_height + 1)

        if x is None or y is None:
            x, y = self.random_free_coords()

        if x > self.map_width + 1:
            self.resize_map(x, self.map_height)
        if y > self.map_height + 1:
            self.resize_map(self.map_width, y)

        if (x, y) in self.free_spaces():
            self.region_map[x][y] = region
        if x >= self.map_width:
            self.map_width = x + 1
        if y >= self.map_height:
            self.map_height = y + 1

    def resize_map(self, width, height):
        if width > self.map_width:
            for x in range(self.map_width, width):
                self.region_map.append([None for y in range(0, self.map_height)])

        elif width < self.map_width:
            for x in range(width, self.map_width):
                self.region_map.pop(-1)

        self.map_width = width

        if height > self.map_height:
            for x in range(self.map_width):
                self.region_map[x] += [None for y in range(self.map_height, height)]

        elif height < self.map_height:
            for x in range(self.map_width):
                for y in range(height, self.map_height):
                    self.region_map[x].pop(-1)

        self.map_height = height
        
    def random_free_coords(self):
        if self.is_full():
            return False
        else:
            x, y = random.choice(self.free_spaces())
            return x, y

    def set_seat_count(self, total):
        if len(self.regions()) == 0:
            return False
        if len(self.regions()) == 1:
            self.regions()[0].seat_count = total
            return

        def total_designations(designations):
            return sum(designations.values())

        def find_highest(populations):
            highest = list(populations.keys())[0]
            for region in populations:
                if populations[region] > populations[highest]:
                    highest = region
            return highest

        # Proportionally distributes seats
        # Guarentees at least each region gets one seat
        # Uses a similar method to D'Hont to distribute the seats
        designations = {region: 1 for region in self.regions()}
        populations = {region: region.population() for region in self.regions()}
        original_populations = populations.copy()
        divisors = [1/(n+2) for n in range(total - total_designations(designations))]
        while total_designations(designations) < total:
            highest = find_highest(populations)
            divisor = divisors[designations[highest]]
            populations[highest] = original_populations[highest] * divisor
            designations[highest] += 1
        for region in designations:
            region.seat_count = designations[region]
        return designations

    def create_regions(self, number, population=1000):
        for i in range(number):
            self.add_region(Region(population=population))

    def create_parties(self, number):
        for i in range(number):
            self.parties.append(Party())

    def is_empty(self):
        return len(self.regions()) == 0

    def is_full(self):
        return self.free_spaces() == []

    def regions(self):
        r = []
        for sub in self.region_map:
            for region in sub:
                if region is not None:
                    r.append(region)
        return r

    def __repr__(self):
        return self.regions()

    def reps(self):
        reps = []
        # Returns a list of all of the representatives
        for region in self.regions():
            reps += region.reps
        return reps

    def print_reps(self):
        reps = self.reps()

        max_repname = str(max(len(rep.name) for rep in reps))
        max_partyname = str(max(len(rep.party.name) for rep in reps))
        max_regionname = str(max(len(region.name) for region in self.regions()))

        for rep in reps:
            # {:10} means the .format() has to be 10 charachters long
            preformat = ('{:' + max_repname + '} - {:' + max_partyname + '} - {:' + max_regionname + '}')
            # preformat looks like '{:10} - {:10} - {:10}

            print(preformat.format(rep.name, rep.party.name, rep.region.name))
            # Looks like Rep Name - Party - Region

    def reps_by_party(self):
        # Returns a dictionary of each party and how many representatives they have
        # In size order
        p = {}
        for rep in self.reps():
            if rep.party in p:
                p[rep.party] += 1
            else:
                p[rep.party] = 1
        ordered = {}
        for party in rank_dict(p):
            ordered[party] = p[party]
        return ordered

    def percentages_by_party(self):
        p = self.reps_by_party()
        total = len(self.reps())
        for party in p:
            p[party] = round(100 * p[party] / total, 3)

        return p

    def party_reps(self):  # Returns a dictionary of each party and all their Reps
        p = {}
        for rep in self.reps():
            if rep.party in p:
                p[rep.party].append(rep)
            else:
                p[rep.party] = [rep]

        return p

    def population(self):
        return sum(region.population() for region in self.regions())


class NationElection:
    def __init__(self, **kwargs):
        if 'nation' in kwargs:
            self.nation = kwargs['nation']
        else:
            self.nation = Nation()
        self.region_elections = []
        self.type = ''
        self.reps = []

    def run(self, vs):
        # Will run a general election with each region holding a RegionElection under a selected voting system
        for region in self.nation.regions():
            re = RegionElection(region=region, voting_system=vs)
            self.region_elections.append(re)
            self.reps += re.reps

    def popular_vote(self):
        votes = {}
        total_votes = 0
        ind = Party(name='Independents')
        for re in self.region_elections:
            re_votes = re.rounds[0].votes
            for candidate in rank_dict(re_votes):
                total_votes += re_votes[candidate]
                if candidate.party in votes:
                    votes[candidate.party] += re_votes[candidate]
                elif candidate.party.name == 'Independent':
                    if ind in votes:
                        votes[ind] += re_votes[candidate]
                    else:
                        votes[ind] = re_votes[candidate]
                else:
                    votes[candidate.party] = re_votes[candidate]
        for party in votes:
            votes[party] = round(100*votes[party] / total_votes, 2)
            
        return votes


class RegionElection:
    systems = ['runoff', 'fptp', 'stv', 'borda', 'dowdall', 'dhondt', 'webster']

    class Round:
        def __init__(self):
            self.roundnum = 0
            self.winners = []
            self.losers = []
            self.voting_system = None
            self.votes = {}
            self.percentages = {}

        def candidates(self):
            return list(self.votes.keys())
        
        def parties(self):
            return list(self.votes.keys())

    class Votes(dict):
        def __init__(self):
            super(RegionElection.Votes, self).__init__()
            # {order(tuple): votes(float)}

        def rank(self):
            # Returns a list of candidates in order of how well they did
            pref_votes = self.pref_votes()
            return sorted(self.pref_votes(), key=pref_votes.get())[::-1]

        def remove_cand(self, candidate):
            # Remove a candidate from race
            # Involves taking all ballots with that candidate on and removing them
            old_votes = self.copy()
            orders_to_pop = []

            for order in old_votes:
                if candidate in order:
                    new_order = list(order).copy()
                    new_order.remove(candidate)
                    new_order = tuple(new_order)

                    orders_to_pop.append(order)
                    votes = self[order]

                    if new_order in self:
                        self[new_order] += votes
                    else:
                        self[new_order] = votes

            for order in orders_to_pop:
                self.pop(order)

        def distribute_cand_proportion(self, candidate, proportion):
            # Distributes a proportion of all votes for a candidate to each ballot's second favourite candidate
            if proportion == 1:
                self.remove_cand(candidate)
                return None

            old_votes = self.copy()
            orders_to_pop = []

            for order in old_votes:
                if candidate in order:
                    new_order = list(order).copy()
                    new_order.remove(candidate)
                    new_order = tuple(new_order)

                    if order[0] == candidate:
                        # If the order's #1 is that candidate
                        # Their votes must be redistributed
                        original_votes = self[order]
                        votes_to_keep = (1 - proportion)*original_votes
                        votes_to_move = proportion*original_votes
                        self[order] = votes_to_keep
                        if new_order in self:
                            self[new_order] += votes_to_move
                        else:
                            self[new_order] = votes_to_move

                    else:
                        # If the candidate appears somewhere else in the order
                        # Just remove that candidate from the order
                        orders_to_pop.append(order)
                        new_order = list(order).copy()
                        new_order.remove(candidate)
                        new_order = tuple(new_order)
                        votes = self[order]

                        if new_order in self:
                            self[new_order] += votes
                        else:
                            self[new_order] = votes

            for order in orders_to_pop:
                self.pop(order)

        def add_vote(self, order, num=1, eliminated=None):
            if eliminated is None:
                eliminated = []
            filtered_order = tuple(filter(lambda x: x not in eliminated, order))
            if filtered_order in self:
                self[filtered_order] += num
            else:
                self[filtered_order] = num

        def total_votes(self):
            v = 0
            for order in self:
                v += self[order]
            return v

        def pref_votes(self):
            pref_count = {}
            for order in self:
                if order != ():
                    if order[0] in pref_count:
                        pref_count[order[0]] += self[order]
                    else:
                        pref_count[order[0]] = self[order]
            return pref_count

        def ballots_by_first_pref(self):
            # Returns a dictionary of ballots
            # {candidate: {order (who's #1 is that candidate): votes for with that order}
            v = {}
            for order in self:
                if order is not ():
                    if order[0] in v:
                        v[order[0]][order] += self[order]
                    else:
                        v[order[0]][order] = self[order]
            return v

    def __init__(self, **kwargs):
        self.region = kwargs.get('region', Region(population=1000))
        self.voting_system = kwargs.get('voting_system', '')
        self.parties = kwargs.get('parties', self.region.parties())
        self.candidates = kwargs.get('candidates', [])
        self.region.seat_count = kwargs.get('seat_count', self.region.seat_count)
        self.min_candidates = kwargs.get('min_candidates', self.region.seat_count + 2)
        self.min_parties = kwargs.get('min_parties', 2)
        self.party_lists = kwargs.get('party_lists', {})

        self.rounds = []
        self.party_seatcount = {}
        self.reps = []
        self.order = []

        self.candidatesystems = {
            'runoff': self.runoff,
            'fptp': self.fptp,
            'stv': self.stv,
            'borda': self.borda,
            'dowdall': self.dowdall

        }
        self.partylistsystems = {
            'dhondt': self.dhondt,
            'webster': self.webster,
        }


        self.run()

    def run(self):
        if self.voting_system in self.candidatesystems:
            if len(self.candidates) < self.min_candidates:
                # If there are not enough candidates
                # Add candidates from each party
                for party in self.region.parties():
                    self.candidates += [Candidate(region=self.region, party=party) for c in range(self.region.seat_count)]

            # If there are still not enough candidates, add some independents
            if len(self.candidates) < self.min_candidates:
                diff = self.min_candidates - len(self.candidates)
                self.candidates += [Candidate(region=self.region) for c in range(diff)]

            self.candidatesystems[self.voting_system]()

        elif self.voting_system in self.partylistsystems:
            if len(self.parties) < self.min_parties:
                diff = self.min_parties - self.min_parties
                self.parties += [Party() for i in range(diff)]

            self.party_lists = {party: party.gen_list(self.region.seat_count, self.region) for party in self.region.parties()}

            self.partylistsystems[self.voting_system]()

    def runoff(self):
        # Like STV, however the quota is removed
        # Lowest ranked candidates get removed until the number of candidates left is equal to the seat_count
        self.voting_system = 'runoff'
        self.rounds = []

        votes = RegionElection.Votes()

        for voter in self.region:
            order = voter.rank(self.candidates)
            votes.add_vote(order, 1)

        seat_num = self.region.seat_count
        if len(self.candidates) < seat_num:
            seat_num = len(self.candidates)
        if len(self.candidates) == 0:
            return False

        won = []
        eliminated = []
        running = self.candidates.copy()

        # While the number of winners < the number of people we want to elect
        while len(won) < seat_num:
            finish_round = False
            # Count votes
            prefs = votes.pref_votes()

            # Save round
            self.rounds.append(RegionElection.Round())
            self.rounds[-1].votes = votes.pref_votes()

            # See if the number of remaining candidates = the number of seats left to fill
            if len(running) == seat_num - len(won):
                # Set all of these candidates as winners
                winners = running.copy()
                for candidate in winners:
                    self.rounds[-1].winners.append(candidate)
                    won.append(candidate)
                    running.remove(candidate)
                # Skip the rest of the while loop
                finish_round = True
            if finish_round:
                continue

            if running == []:
                continue
            # Find lowest ranked candidate thats still running
            loser = running[0]
            for candidate in prefs:
                if candidate in running and prefs[candidate] < prefs[loser]:
                    loser = candidate

            # If there are any candidates with 0 votes that haven't been eliminated, they become the round loser
            for candidate in running:
                if candidate not in prefs:
                    loser = candidate

            # Set them as round loser
            self.rounds[-1].losers = [loser]
            eliminated.append(loser)
            running.remove(loser)
            votes.remove_cand(loser)

        self.region.reps = won
        self.region.elections.append(self)
        self.order = won + running + eliminated[::-1]
        return won

    def fptp(self):
        self.voting_system = 'fptp'
        candidates = self.candidates

        seat_count = self.region.seat_count
        if len(self.candidates) < seat_count:
            seat_count = len(self.candidates)
        if len(self.candidates) == 0:
            return False

        votes = {candidate: 0 for candidate in candidates}
        # Each candidate starts with 0 votes
        total_votes = 0
        for voter in self.region:
            favs = voter.rank(candidates)[0:seat_count]
            # Every voter votes for their favourite candidate
            # If multiple candidates are to be elected, you put as many X's as there are candidates
            for fav in favs:
                votes[fav] += 1
            total_votes += len(favs)

        self.rounds = [self.Round()]
        # Adds votes
        self.rounds[0].votes = {candidate: round(votes[candidate]) for candidate in votes}
        self.rounds[0].percentages = {candidate: round(votes[candidate]*100 / total_votes, 4) for candidate in votes}

        # Find highest ranked candidate
        winners = rank_dict(votes)[0: self.region.seat_count]
        self.rounds[0].winners = winners

        self.region.elections.append(self)
        self.reps = winners
        self.order = rank_dict(votes)
        self.region.reps = winners
        return winners

    def stv(self):
        candidates = self.candidates
        self.voting_system = 'stv'
        self.rounds = []

        votes = RegionElection.Votes()
        total_votes = len(self.region)

        for voter in self.region:
            order = tuple(voter.rank(candidates))
            if len(order) > 7:
                order = order[0::7]
            votes.add_vote(order, 1)

        seat_num = self.region.seat_count
        if len(self.candidates) < seat_num:
            seat_num = len(self.candidates)
        if len(self.candidates) == 0:
            return False
        won = []
        eliminated = []
        running = candidates.copy()

        # Quota
        quota = total_votes / (seat_num + 1)

        # While the number of winners < the number of people we want to elect
        while len(won) < seat_num:
            finish_round = False
            # Count votes
            prefs = votes.pref_votes()

            # Save round
            self.rounds.append(RegionElection.Round())
            self.rounds[-1].votes = votes.pref_votes()

            # See if the number of remaining candidates = the number of seats left to fill
            if len(running) == seat_num - len(won):
                # Set all of these candidates as winners
                winners = running.copy()
                for candidate in winners:
                    self.rounds[-1].winners.append(candidate)
                    won.append(candidate)
                    running.remove(candidate)
                # Skip the rest of the while loop
                finish_round = True
            if finish_round:
                continue

            # Go through each candidate
            for candidate in running:
                # If they're over the quota
                if candidate in prefs:
                    if prefs[candidate] >= quota:
                        # Add them as winners
                        won.append(candidate)
                        self.rounds[-1].winners = [candidate]
                        running.remove(candidate)
                        # Find out number of excess votes
                        surplus = prefs[candidate] - quota
                        # Find out proportion of votes that are over that quota
                        surplus_proportion = surplus / prefs[candidate]
                        # Distribute the votes
                        votes.distribute_cand_proportion(candidate, surplus_proportion)
                        finish_round = True
                        break

            if finish_round: continue

            if running == []:
                continue

            # Find lowest ranked candidate thats still running
            loser = list(prefs.keys())[0]
            for candidate in prefs:
                if candidate in running and prefs[candidate] < prefs[loser]:
                    loser = candidate

            # If there are any candidates with 0 votes that haven't been eliminated, they become the round loser
            for candidate in running:
                if candidate not in prefs:
                    loser = candidate

            # Set them as round loser
            self.rounds[-1].losers = [loser]
            eliminated.append(loser)
            running.remove(loser)
            votes.remove_cand(loser)

        self.region.reps = won
        self.region.elections.append(self)
        self.order = won + running + eliminated[::-1]
        return won

    def borda(self):
        self.voting_system = 'borda'
        # Uses a points based system
        # Your least fav candidate gets one point
        # Your second least fav gets two, etc
        # Total points added, top candidate selected
        # Only works to elect one candidate
        cand_points = {candidate: 0 for candidate in self.candidates}
        for voter in self.region:
            rank = voter.rank(self.candidates)
            point = 1
            for candidate in rank[::-1]:
                cand_points[candidate] += point
                point += 1

        # Finding winner
        winners = rank_dict(cand_points)[0:self.region.seat_count]

        # Add the round to self.rounds
        self.rounds = [RegionElection.Round()]
        self.rounds[0].votes = cand_points.copy()
        self.rounds[0].voting_system = self.voting_system
        self.rounds[0].winners = winners

        self.region.reps = winners
        self.region.elections.append(self)
        self.order = rank_dict(cand_points)
        return winners

    def dowdall(self):
        self.voting_system = 'dowdall'
        # Also a points based system
        # Fav candidate gets 1 point
        # Second fav gets 1/2 a point, etc
        # Can elect more than one candidate
        cand_points = {candidate: 0 for candidate in self.candidates}
        for voter in self.region:
            rank = voter.rank(self.candidates)
            point = 1
            for candidate in rank:
                cand_points[candidate] += 1/point
                point += 1

        # Finding winner
        winners = rank_dict(cand_points)[0:self.region.seat_count]
        # Rounds system
        self.rounds = [RegionElection.Round()]
        self.rounds[0].votes = cand_points.copy()
        self.rounds[0].voting_system = self.voting_system
        self.rounds[0].winners = winners

        self.region.reps = winners
        self.region.elections.append(self)
        self.order = rank_dict(cand_points)
        return winners

    def dhondt(self):
        # A divisor based voting system
        # Party with the most votes earns a seat
        # The number of votes they now have is equal to:
        #     number of votes they had originally) / (number of seats they now have +1)
        self.voting_system = 'dhondt'
        divisors = [1 / (x + 2) for x in range(self.region.seat_count)]
        return self.divisor(divisors)

    def webster(self):
        # A divisor based voting system
        # But with a slightly different set of divisors
        self.voting_system = 'webster'
        divisors = [1 / (2 * x + 3) for x in range(self.region.seat_count)]
        return self.divisor(divisors)

    def divisor(self, divisors):
        # Divisor based elections like dhondt or Webster
        party_lists = self.party_lists
        self.rounds = []
        self.party_seatcount = {}
        reps = []
        self.parties = list(party_lists.keys())

        # party_lists is a dictionary, {party:[list of candidates (in order)]}
        # Seat number is the number of seats that region will send to the parliament

        # Get each voters preferences of the Parties
        parties = party_lists.keys()

        # Make a dict party:[candidate_list]

        partyvotes = self.collect_vote(parties)
        # {party: number of votes}

        # Make a dict, party:seat_number (by default 0)
        party_seatswon = {party: 0 for party in parties}

        # WHILE len(reps) < seat_number
        original_party_votes = partyvotes.copy()
        while len(reps) < self.region.seat_count:
            self.rounds.append(RegionElection.Round())
            r = self.rounds[-1]
            r.voting_system = self.voting_system
            r.votes = partyvotes.copy()

            # Find party with most votes
            most_votes = rank_dict(partyvotes)[0]

            # Add the parties next candidate to the seats list
            reps.append(party_lists[most_votes][party_seatswon[most_votes]])
            r.winners = [party_lists[most_votes][party_seatswon[most_votes]], most_votes]

            # set that parties votes to (number of original votes for that party)*(divisors[seat_number])
            # As you get more seats the number of votes you have decreases
            partyvotes[most_votes] = round(original_party_votes[most_votes] * divisors[party_seatswon[most_votes]], 0)

            # Increase party:seats dict by 1
            party_seatswon[most_votes] += 1

        # Return the list of candidates
        # Set attributes
        self.region.elections.append(self)
        self.party_seatcount = party_seatswon
        self.order = rank_dict(self.rounds[0].votes)
        self.reps = reps
        self.region.reps = reps
        return reps

    def collect_vote(self, candidates):
        # Give a list of candidates / parties
        # returns a dict of {party: number of votes}
        # Only one vote of that person's favourite candidate
        votes = {candidate: 0 for candidate in candidates}
        for voter in self.region:
            votes[voter.rank(candidates)[0]] += 1
        return votes

    def print_rounds(self):
        for r in range(len(self.rounds)):
            print(f'Round {r + 1}:')
            if self.voting_system in self.candidatesystems:
                cands = self.candidates
            elif self.voting_system in self.partylistsystems:
                cands = self.parties
            else:
                return None
            for cand in cands:
                if cand in self.rounds[r].votes:
                    print(f'    {cand.name}: {self.rounds[r].votes[cand]}')


def gen_random_color():
    color = '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])

    return color


def gen_leaning(factor=1.0):
    x = random.normalvariate(0, factor)
    y = random.normalvariate(0, factor)
    return x, y


def rank_dict(dictionary):
    # Returns a sorted list of all of the keys in the dictionary
    # Sorted by the values in the dictionary
    return sorted(dictionary, key=dictionary.get)[::-1]

