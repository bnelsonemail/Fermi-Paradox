import tkinter as tk
from random import randint, uniform, random
import math
import numpy as np

# *************** MAIN INPUT ***************************

# SCALED_DISC_RADIUS = disc_radius / bubble diameter

# scale radio bubble diameter in light-years
SCALE = 225 # enter 225 to see Earth's radio bubble

# number of advanced civilizations from Drake equation:
NUM_CIV = 15_600_000

# Establish the constant pi
pi = np.pi 


# actual Milky Way dimensions in light-years
DISC_RADIUS = 50_000
DISC_HEIGHT = 1_000
DISC_VOLUME = pi * DISC_RADIUS**2 * DISC_HEIGHT




# set up display canvas
root = tk.Tk()
root.title("Milky Way Galaxy")
c = tk.Canvas(root, width=1000, height=800, bg='black') # Sets the dimensions of the Canvas window.  w=1000 and h=800 works well on a laptop.
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400)) # configures how the widget is shown in the canvas window.  To center the widget, these numbers need to be half of the screen size


class Galaxy:
    """
    Class that defines functions to calculate the probability of communication with other civilizations within the Milky Way Galaxy through use of the Drake Equation
    """

    def __init__(self) -> None:
        pass
    
    def scale_galaxy(self):
        """Scale galaxy dimensions based on radio bubble size (scale)."""
        disc_radius_scaled = round(DISC_RADIUS / SCALE)
        bubble_vol = 4/3 * pi * (SCALE / 2)**3
        disc_volume_scaled = DISC_VOLUME / bubble_vol
        return disc_radius_scaled, disc_volume_scaled
    
    def detect_prob(disc_volume_scaled):
        """Calculate probability of galactic civilizations detecting each other."""
        ratio = NUM_CIV / disc_volume_scaled # ratio of civs to scaled galaxy volume
        if ratio < 0.002: # set very low ratios to probability of 0
            detection_prob = 0
        elif ratio >= 5: # set high ratios to probabity of 1
            detection_prob = 1
        else:
            detection_prob = -0.004757 * ratio**4 + 0.06681 * ratio**3 - 0.3605 * ratio**2 + 0.9215 * ratio + 0.00826 # this equation was generated in the prob_detection.py
        return round(detection_prob, 3)
    
    