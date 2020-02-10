# This script returns a Nation object
# With all of the Region objects being UK constituencies
# In a grid that resembles a map of the UK

import json
import electioneering as e


def uk():
    with open('uk.json', 'r') as file:
        # Open the JSON file
        data = json.load(file)

        # The file I downloaded orignally used hexes
        # Each constituency = one hex
        # We need to convert it into grids, but that's not too hard
        region_info = []

        for info in data['hexes'].values():
            # Converting into a dictionary
            # 'n' from the JSON file becomes 'name'
            # 'p' coord from JSON file becomes 'x'
            # 'r' coord form JSON file becomes 'y'
            # 'e' from JSON becomes population
            # Adding 17 to X coordinates to stop X coordinates from being negative
            # Adding 26 to Y coordinates to stop Y coordinates from being negative
            # Adding 7  to X coordinates to center the map
            region_info.append({'name': info['n'], 'x': info['q'] + 17 + 7, 'y': 26 - info['r'], 'population': info['e']})

        nation = e.Nation(map_width=(26+16+1), map_height=(26+16+1))
        for region in region_info:
            r = e.Region()
            r.set_population(region['population']//100)
            # Dividing each region's population by 100 to help with efficiency
            r.name = region['name']
            nation.add_region(r, region['x'], region['y'])

        return nation
uk()