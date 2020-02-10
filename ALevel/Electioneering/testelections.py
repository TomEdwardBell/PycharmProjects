# Testing Scenario
import electioneering as e

def fptp():
    region = e.Region()
    candidates = [e.Candidate(name="A"), e.Candidate(name="B"), e.Candidate(name="C"), e.Candidate(name="D")]

    # Voters for candidate A
    region.voters += [e.Voter(leaning=candidates[0]) for v in range(100)]
    region.voters += [e.Voter(leaning=candidates[1]) for v in range(80)]
    region.voters += [e.Voter(leaning=candidates[2]) for v in range(70)]
    region.voters += [e.Voter(leaning=candidates[3]) for v in range(50)]

    election = e.RegionElection(voting_system='fptp', candidates=candidates)
    election.print_rounds()
    print(election.winners)

fptp()