import numpy as np
from random import randint
from collections import Counter
import matplotlib.pyplot as plt




pi = np.pi
galactic_disc_height = 1000 # LY
galactic_disc_area = 7.85 * 10**9 # SQ. LY
R_galactic_disc_radius = galactic_disc_area / galactic_disc_height
radio_bubble_volume_est = 4.19 * 10**6 # CU. LY
radio_bubble_radius = 200 / 2 # LY

galactic_disc_volume = pi * R_galactic_disc_radius**2 * galactic_disc_height # CU. LY
radio_bubble_volume_calc = 4/3 * pi * radio_bubble_radius**3 # CU. LY


NUM_EQUIV_VOLUMES = 1000 # number of locations in which to place civilizations
MAX_CIVS = 5000 # maximum number of advanced civilzations 
TRIALS = 1000 # number of times to model a given number of civilizations
CIV_STEP_SIZE = 100 # civilizations count step size


x = [] # ratio of civilizations per volume (x values for polynomial fit)
y = [] # corresponding probability of detection (y values for polynomial fit)

for num_civs in range(2, MAX_CIVS + 2, CIV_STEP_SIZE): # number of civilizations to model. Need at least 2 civilizations to detect each other, and set the max plus 2 to overshoot when calculating the polynomial.
    civs_per_vol = num_civs / NUM_EQUIV_VOLUMES
    num_single_civs = 0 # variable to keep track of the number of locations containing a single civilization
    for trial in range(TRIALS): # For each trial the same number of civilizations are distributed
        locations = [] # equivalent volumes containing a civilization. 
        while len(locations) < num_civs:
            location = randint(1, NUM_EQUIV_VOLUMES)
            locations.append(location)
        overlap_count = Counter(locations)
        overlap_rollup = Counter(overlap_count.values())
        num_single_civs += overlap_rollup[1]
    prob = 1 - (num_single_civs / (num_civs * TRIALS))
    
    # print ratio of civs-per-volume vs probability of 2+ civs per location
    print("{:.4f} {:.4f}".format(civs_per_vol, prob))
    x.append(civs_per_vol)
    y.append(prob)
    



