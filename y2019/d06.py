r"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation
in space often involves transferring between orbits, the orbit maps here are
useful for finding efficient routes between, for example, you and Santa. You
download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit
around exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /

In this diagram, the object BBB is in orbit around AAA. The path that BBB takes
around AAA (drawn with lines) is only partly shown. In the map data, this
orbital relationship is written AAA)BBB, which means "BBB is in orbit around
AAA".

Before you use your map data to plot a course, you need to make sure it wasn't
corrupted during the download. To verify maps, the Universal Orbit Map facility
uses orbit count checksums - the total number of direct orbits (like the one
shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can
be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A
indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L

Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I

In this visual representation, when two objects are connected by a line, the one
on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

    D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.

    L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of
    7 orbits.
    
    COM orbits nothing.

The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU) need to 
take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is 
orbiting. An orbital transfer lets you move from any object to an object 
orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN

Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To 
move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object 
YOU are orbiting to the object SAN is orbiting? (Between the objects they are 
orbiting - not between YOU and SAN.)


"""

import pathlib
import collections
from pprint import pprint

def parse_input(filename):
    input_path = pathlib.Path(__file__).parent / filename
    orbits = {}
    for line in input_path.open('r').readlines():
        a, b = line.strip().split(')')
        orbits[b] = a
    return orbits

def count_orbits(orbits):
    pairs = set()
    for orbiter, orbitee in orbits.items():
        while orbitee:
            pairs.add((orbiter, orbitee))
            orbitee = orbits.get(orbitee, None)
    return len(pairs)

def fewest_transfers(orbits, origin, destination):
    # Build a bidirectional gratph
    neighbors = collections.defaultdict(set)
    for orbiter, orbitee in orbits.items():
        neighbors[orbiter].add(orbitee)
        neighbors[orbitee].add(orbiter)
    
    # Breadth first distance measure from origin to every planet/body
    ingres = { origin: origin}
    frontier = { origin }
    while frontier:
        next_frontier = set()
        # Expand frontier
        for f in frontier:
            for n in neighbors[f]:
                if n in ingres:
                    continue
                ingres[n] = f
                next_frontier.add(n)
        frontier = next_frontier

    # Track back from destination to origin
    current = destination
    path = []
    while current != origin:
        next_step = ingres[current]
        path.append((next_step, current))
        current = next_step
    
    # Reverse path segment list to get the path from origin to destination
    path.reverse()
    return path

def test_count_orbits():
    orbits = parse_input('d06input.test')
    num_orbits = count_orbits(orbits)
    assert num_orbits == 42

def test_part1():
    orbits = parse_input('d06input')
    num_orbits = count_orbits(orbits)
    assert num_orbits == 194721

def test_fewest_transfers():
    orbits = parse_input('d06input.test2')
    origin = orbits['YOU']
    destination = orbits['SAN']
    actual = fewest_transfers(orbits, origin, destination)
    exepected = [
        ('K', 'J'), ('J', 'E'), ('E', 'D'), ('D', 'I')
    ]
    assert actual == exepected

def main():
    orbits = parse_input('d06input')
    num_orbits = count_orbits(orbits)
    print('Number of orbits (Part I):', num_orbits) # 194721

    origin = orbits['YOU']
    destination = orbits['SAN']
    path = fewest_transfers(orbits, origin, destination)
    num_transfers = len(path)
    print('Minimum number of orbital transfers (Part II):', num_transfers)

if __name__ == "__main__":
    main()