from burnsidelib import *

A.<t> = BurnsideRing(gap("CyclicGroup(2)"))
print((3*t-4).marks()) # (2,-4)