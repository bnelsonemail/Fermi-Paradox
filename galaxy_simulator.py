# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 20:33:02 2024.

@author: BNELS
"""
import tkinter as tk
from drake_equation import DRAKE_NUMBER
from random import randint, uniform, random
import math
import numpy as np

# *************** MAIN INPUT ***************************

SCALE = 225  # scaling factor for radio bubble diameter in light-years.
NUM_CIV = DRAKE_NUMBER  # number of advanced civilizations from Drake equation
pi = np.pi  # Establish the constant pi

DISC_RADIUS = 50_000  # Milky Way dimensions in light-years
DISC_HEIGHT = 1_000  # Milky Way dimensions in light-years
# Milky Way volume in cubic light-years
DISC_VOLUME = pi * DISC_RADIUS**2 * DISC_HEIGHT

# set up display canvas
root = tk.Tk()
root.title("Milky Way Galaxy")
# Sets the dimensions of the Canvas window.
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))


class Galaxy:
    """
    A class to simulate and visualize the structure of the Milky Way galaxy.

    The Galaxy class provides tools to simulate the Milky Way galaxy's spiral
    arms and diffuse star haze using a logarithmic spiral model. It also
    calculates the probability of detection of advanced civilizations based
    on the scaled galactic volume and the number of civilizations.

    The class uses tkinter for graphical visualization, presenting the
    galaxy's structure on a 2D canvas and including key attributes like the
    scale of the galaxy, the number of spiral arms, and the density of stars.

    Attributes
    ----------
    b : float
        Parameter for the logarithmic spiral equation, controlling the
        curvature of the spiral arms.
    r : float
        The scaled radius of the galactic disc in light-years.
    rot_fac : float
        Rotation factor for positioning spiral arms within the galaxy.
    fuz_fac : float
        Fuzziness factor to introduce variability in the position of stars in
        the spiral arms.
    arm : int
        Indicates whether stars belong to the main arm (0) or trailing arm (1).
    density : int
        Density factor controlling the number of randomly distributed stars
        in the diffuse star haze.

    Methods
    -------
    __init__(self, b, r, rot_fac, fuz_fac, arm, density)
        Initializes the Galaxy object with parameters to define spiral arms
        and overall structure.
    scale_galaxy(self)
        Scales the galaxy's dimensions and volume based on the size of a radio
        bubble.
    detect_prob(self, disc_volume_scaled)
        Calculates the probability that civilizations can detect each other
        based on the scaled galactic volume and the number of civilizations.
    random_polar_coordinates(self, disc_radius_scaled)
        Generates random (x, y) coordinates within the galactic disc using
        polar coordinates for uniform distribution in a 2D space.
    spirals(self, b, r, rot_fac, fuz_fac, arm)
        Creates the spiral arms of the galaxy on the tkinter canvas using a
        logarithmic spiral model and plots stars accordingly.
    star_haze(self, disc_radius_scaled, density)
        Creates a diffuse star haze across the galactic disc by randomly
        distributing small, faint stars.
    main(self)
        Orchestrates the scaling of the galaxy, calculates civilization
        detection probability, and displays the galaxy with spiral arms,
        star haze, and statistics on a tkinter canvas.
    """

    def __init__(self, b, r, rot_fac, fuz_fac, arm, density):
        """Initialize the Galaxy object with parameters for spiral arm.

        creation.
        """
        self.b = b
        self.r = r
        self.rot_fac = rot_fac
        self.fuz_fac = fuz_fac
        self.arm = arm
        self.density = density

    def scale_galaxy(self):
        """Scale galaxy dimensions based on radio bubble size (scale)."""
        disc_radius_scaled = round(DISC_RADIUS / SCALE)
        bubble_vol = 4 / 3 * pi * (SCALE / 2) ** 3
        disc_volume_scaled = DISC_VOLUME / bubble_vol
        return disc_radius_scaled, disc_volume_scaled

    def detect_prob(self, disc_volume_scaled):
        """Calculate the probability of galactic civilizations detecting.

        each other.
        """
        ratio = NUM_CIV / disc_volume_scaled
        if ratio < 0.002:
            detection_prob = 0
        elif ratio >= 5:
            detection_prob = 1
        else:
            detection_prob = (-0.004757 * ratio ** 4 + 0.06681 * ratio ** 3 -
                              0.3605 * ratio ** 2 + 0.9215 * ratio + 0.00826)
        return round(detection_prob, 3)

    def random_polar_coordinates(self, disc_radius_scaled):
        """Generate uniform random (x, y) point within a disc.

        for 2D display.
        """
        r = random()
        theta = uniform(0, 2 * pi)
        x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
        y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
        return x, y

    def spirals(self, b, r, rot_fac, fuz_fac, arm):
        """Build spiral arms for tkinter display using log spiral form."""
        spiral_stars = []
        fuzz = int(0.030 * abs(r))
        theta_max_degrees = 520

        for i in range(theta_max_degrees):
            theta = math.radians(i)
            x = (r * math.exp(b * theta) * math.cos(theta + pi * rot_fac) +
                 randint(-fuzz, fuzz) * fuz_fac)
            y = (r * math.exp(b * theta) * math.sin(theta + pi * rot_fac) +
                 randint(-fuzz, fuzz) * fuz_fac)
            spiral_stars.append((x, y))

        for x, y in spiral_stars:
            if arm == 0 and int(x % 2) == 0:
                c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='')
            elif arm == 0 and int(x % 2) != 0:
                c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
            elif arm == 1:
                c.create_oval(x, y, x, y, fill='white', outline='')

    def star_haze(self, disc_radius_scaled, density):
        """Create a diffuse haze of faint stars randomly distributed."""
        for i in range(0, disc_radius_scaled * density):
            x, y = self.random_polar_coordinates(disc_radius_scaled)
            c.create_text(x, y, fill='white', font=('Helvetica', '7'),
                          text='.')

    def main(self):
        """Calculate detection prob. & post galaxy display & statistics."""
        disc_radius_scaled, disc_volume_scaled = self.scale_galaxy()
        detection_prob = self.detect_prob(disc_volume_scaled)

        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=2, fuz_fac=1.5, arm=0)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=1.91, fuz_fac=1.5, arm=1)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=2, fuz_fac=1.5, arm=0)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=2.09, fuz_fac=1.5, arm=1)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=0.5, fuz_fac=1.5, arm=0)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=0.4, fuz_fac=1.5, arm=1)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=0.5, fuz_fac=1.5, arm=0)
        self.spirals(b=-0.3, r=disc_radius_scaled,
                     rot_fac=0.6, fuz_fac=1.5, arm=1)

        self.star_haze(disc_radius_scaled, density=8)

        c.create_text(-455, -360, fill='white', anchor='w',
                      text='One Pixel = {} LY'.format(SCALE))
        c.create_text(-455, -330, fill='white', anchor='w',
                      text='Radio Bubble Diameter = {} LY'.format(SCALE))
        c.create_text(-455, -300, fill='white', anchor='w',
                      text='Prob. of detection for {:,} civilizations = {}'.format(NUM_CIV, detection_prob))

        if SCALE == 225:
            c.create_rectangle(115, 75, 116, 76, fill='red', outline='')
            c.create_text(118, 72, fill='red', anchor='w',
                          text="<---------- Earth's Radio Bubble")

        root.mainloop()


if __name__ == "__main__":
    galaxy = Galaxy(b=-0.3, r=50_000, rot_fac=2, fuz_fac=1.5, arm=0, density=8)
    galaxy.main()
