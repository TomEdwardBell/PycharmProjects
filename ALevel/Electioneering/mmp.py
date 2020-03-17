
# Put into NationElection
def mmp(self, **kwargs):
    # The voting system used by regions to elect members
    self.primary_voting_system = kwargs.get('primary', 'stv')

    # The 'top up' voting system used
    self.additional_voting_system = kwargs.get('secondary', 'dhondt')

    # The number of additional seats
    # By default it is 20% of the number of region_seats
    self.top_up_seats = kwargs.get('top_up', self.nation.total_seat_count() // 5)

    self.party_seats = {}

    # Running the regional elections under the primary voting system
    for region in self.nation.regions():
        re = RegionElection(region=region, voting_system=self.primary_voting_system, parties=self.nation.parties)
        self.region_elections.append(re)
        self.winners += re.winners

    # Create a dictionary of 'party':number of seats they won in the regional elections
    for winner in self.winners:
        if not winner.is_independent:
            if winner.party in self.party_seats:
                self.party_seats[winner.party] += 1
            else:
                self.party_seats[winner.party] = 1

    # Run a divisor based election to see what a fully-proportional parliament would look like
    proportional_seats = {party: 0 for party in self.nation.parties}

    original_party_votes = {party: 0 for party in self.nation.parties}
    for voter in self.nation.voters():
        original_party_votes[voter.rank(self.nation.parties)[0]] += 1
        # Adding each voters favourite party
    current_party_votes = original_party_votes.copy()

    # The divisors used
    divisors = [1 / (x + 2) for x in range(self.top_up_seats + self.nation.total_seat_count())]

    rounds_run = 0
    print('Proportionally distributing: ', self.nation.total_seat_count(), '+', self.top_up_seats)
    while rounds_run < self.nation.total_seat_count() + self.top_up_seats:
        # Find party with most votes
        most_votes = rank_dict(current_party_votes)[0]

        # set that parties votes to (number of original votes for that party)*(divisors[seat_number])
        # As you get more seats the number of votes you have decreases
        new_votes = round(original_party_votes[most_votes] * divisors[proportional_seats[most_votes]], 3)
        current_party_votes[most_votes] = new_votes

        # Add 1 to their party_seats
        rounds_run += 1
        proportional_seats[most_votes] += 1

    partys_seats = {}
    print('Regional Winners: ', self.winners)
    print('Number of Regional Winners: ', len(self.winners))
    # A list of parties and the seats they have already won
    # If they need more seats due to the proportional
    for winner in self.winners:
        if winner.party not in partys_seats:
            partys_seats[winner.party] = [winner]
        else:
            partys_seats[winner.party].append(winner)

    print('Proportional: ', proportional_seats)
    print('Regional: ', partys_seats)

    # Goes through the proportional seats and sees if a party needs more seats to make the parliament look proportional
    for party in proportional_seats:
        if party not in partys_seats:
            print('Adding Candidates from party, ', party)
            new_representatives = party.gen_candidates(proportional_seats[party])
            self.nation.additional_representatives += new_representatives
            partys_seats[party] = new_representatives

        # If the number of seats it should have is more than the number that it does have
        elif proportional_seats[party] > len(partys_seats[party]):
            diff = proportional_seats[party] - len(partys_seats[party])
            print('Adding', diff, 'Candidates from party', party)
            new_representatives = party.gen_candidates(diff)
            partys_seats[party] += new_representatives
            self.nation.additional_representatives += new_representatives

    # Collapse the dictioanry to a list of candidates that includes the additional-proporitonal winners
    # And the regional winners

    total_winners = []
    for party in partys_seats:
        total_winners += partys_seats[party]

    self.winners = total_winners
    return self.winners