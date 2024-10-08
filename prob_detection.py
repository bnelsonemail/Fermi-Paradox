# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 01:08:21 2024.

@author: BNELS
"""
# Standard library imports
from random import randint
from collections import Counter

# Third-party imports
import matplotlib
matplotlib.use('TkAgg')  # noqa: E402

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Constants
NUM_EQUIV_VOLUMES = 1000  # number of locations in which to place civilizations
MAX_CIVS = 5000  # maximum number of advanced civilzations
TRIALS = 1000  # number of times to model a given number of civilizations
CIV_STEP_SIZE = 100  # civilizations count step size


# List to store the computed values
x = []  # ratio of civilizations per volume (x values for polynomial fit)
y = []  # corresponding probability of detection (y values for polynomial fit)

# *********************** PART 1**********************************************


# Main simulation
# number of civilizations to model. Need at least 2 civilizations to detect
# each other, and set the max plus 2 to overshoot when calculating the
# polynomial.
for num_civs in range(2, MAX_CIVS + 2, CIV_STEP_SIZE):
    civs_per_vol = num_civs / NUM_EQUIV_VOLUMES
    # variable to keep track of the number of locations containing a single
    # civilization
    num_single_civs = 0
    # For each trial the same number of civilizations are distributed
    for trial in range(TRIALS):
        locations = []  # equivalent volumes containing a civilization.
        while len(locations) < num_civs:
            location = randint(1, NUM_EQUIV_VOLUMES)
            locations.append(location)
        overlap_count = Counter(locations)
        overlap_rollup = Counter(overlap_count.values())
        num_single_civs += overlap_rollup[1]
    prob = 1 - (num_single_civs / (num_civs * TRIALS))

    # Collect Results
    # print ratio of civs-per-volume vs probability of 2+ civs per location
    # print("{:.4f} {:.4f}".format(civs_per_vol, prob))
    x.append(civs_per_vol)
    y.append(prob)

# Create a DataFrame to hold the results
data = pd.DataFrame({
    'Civs Per Volume': x,
    'Probability of Dectection': y
})


# ************************** PART 2 *******************************************


# Polynomial Regression
coefficients = np.polyfit(x, y, 4)  # 4th order polynomial fit
p = np.poly1d(coefficients)
print("\n{}".format(p))
xp = np.linspace(0, 5)
_ = plt.plot(x, y, '.', p(xp), '-')
plt.ylim(-0.5, 1.5)

# Display the DataFrame
print(data)  # This is the table results


# Plot the graph
plt.plot(x, y, marker='o')
plt.title('Probability of Detection vs. Civilizations Per Volume')
plt.xlabel('Civilizations Per Volume')
plt.ylabel('Probability of Detection')
plt.grid(True)
plt.show()
