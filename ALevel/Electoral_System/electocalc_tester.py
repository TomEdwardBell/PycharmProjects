import electocalc as e
import electocalc_widgets as ew



nat = e.gen_nation(4000, 20, 7)
ne = e.NationElection(nat)
ne.fptp()
ne.display_info()
