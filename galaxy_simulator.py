import tkinter as tk
from random import randint, uniform, random
import math
import numpy as np
import prob_detection

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


import math
import random
from math import pi, sqrt, cos, sin
from random import uniform

# Constants that might be used in the class
DISC_RADIUS = 50000  # Example disc radius of the galaxy in light-years
DISC_VOLUME = 1.5e12  # Example volume of the galaxy in cubic light-years
SCALE = 1000  # Scaling factor for radio bubble size
NUM_CIV = 10000  # Hypothetical number of civilizations

class Galaxy:
    """
    Class that defines functions to calculate the probability of communication with other civilizations 
    within the Milky Way Galaxy through the use of the Drake Equation. It also includes methods
    for visualizing galaxy features such as spiral arms and generating random polar coordinates.
    
    Attributes:
    - b: Parameter related to the spiral arm creation (specific meaning can vary).
    - r: Parameter related to the spiral arm creation (specific meaning can vary).
    - rot_fac: Rotation factor for the galaxy's spiral arms.
    - fuz_fac: Fuzziness factor for the spiral arms to simulate realistic variance.
    - arm: Number of spiral arms in the galaxy.
    """

    def __init__(self, b, r, rot_fac, fuz_fac, arm):
        """
        Initialize the Galaxy object with parameters for spiral arm creation and 
        galaxy characteristics.

        Parameters:
        - b (float): Parameter for spiral arm creation (specific usage depends on spiral method).
        - r (float): Parameter for spiral arm creation (specific usage depends on spiral method).
        - rot_fac (float): Rotation factor, affecting the twist of spiral arms.
        - fuz_fac (float): Fuzziness factor, introducing randomness to spiral arm appearance.
        - arm (int): Number of spiral arms in the galaxy.
        """
        self.b = b
        self.r = r
        self.rot_fac = rot_fac
        self.fuz_fac = fuz_fac
        self.arm = arm 
    
    def scale_galaxy(self):
        """
        Scale galaxy dimensions based on radio bubble size (scale).
        
        This method scales the galaxy's disc radius and volume relative to a radio bubble size,
        then calculates the scaled volume for comparison with other objects or regions.
        
        Returns:
        - disc_radius_scaled (int): Scaled radius of the galaxy's disc.
        - disc_volume_scaled (float): Scaled volume of the galaxy.
        """
        # Scale the galaxy's disc radius and calculate the volume
        disc_radius_scaled = round(DISC_RADIUS / SCALE)
        bubble_vol = 4 / 3 * pi * (SCALE / 2)**3  # Calculate the volume of a sphere representing the radio bubble
        disc_volume_scaled = DISC_VOLUME / bubble_vol  # Scale the galaxy's volume by the bubble volume
        return disc_radius_scaled, disc_volume_scaled
    
    def detect_prob(self, disc_volume_scaled):
        """
        Calculate the probability of galactic civilizations detecting each other.
        
        Uses a polynomial equation to estimate the detection probability based on
        the ratio of the number of civilizations to the scaled galaxy volume.
        
        Parameters:
        - disc_volume_scaled (float): Scaled volume of the galaxy.

        Returns:
        - detection_prob (float): Probability (0 to 1) that civilizations can detect each other.
        
        The polynomial equation was generated in a separate script (prob_detection.py) and models
        the probability as a function of the ratio of civilizations to galaxy volume.
        """
        ratio = NUM_CIV / disc_volume_scaled  # Ratio of civilizations to the scaled galaxy volume
        
        # Calculate the probability based on the ratio
        if ratio < 0.002:  # Set very low ratios to a probability of 0
            detection_prob = 0
        elif ratio >= 5:  # Set high ratios to a probability of 1
            detection_prob = 1
        else:
            # Polynomial equation to estimate probability
            detection_prob = -0.004757 * ratio**4 + 0.06681 * ratio**3 - 0.3605 * ratio**2 + 0.9215 * ratio + 0.00826
        
        return round(detection_prob, 3)
    
    def random_polar_coordinates(self, disc_radius_scaled):
        """
        Generate uniform random (x, y) point within a disc for 2D display.
        
        Uses polar coordinates to generate a random point uniformly within a circle
        representing the galaxy's disc.
        
        Parameters:
        - disc_radius_scaled (int): Scaled radius of the galaxy's disc.

        Returns:
        - (int, int): A tuple of x, y coordinates within the galaxy's disc.

        The generated coordinates (x, y) have values between -1 and +1 after scaling, 
        representing a uniform distribution within the disc.
        """
        # Generate random polar coordinates
        r = random.random()  # Generates a float between 0.0 to 1.0. This includes 0.0 but NOT 1.0
        theta = uniform(0, 2 * pi)  # 2*pi is the radian equivalent of 360 degrees
        
        # Convert polar to Cartesian coordinates, scale them by the disc's radius
        x = round(sqrt(r) * cos(theta) * disc_radius_scaled)
        y = round(sqrt(r) * sin(theta) * disc_radius_scaled)
        
        return x, y  # x, y will have values between -1 and +1.  This is due to r
    
    def spirals(self, b, r, rot_fac, fuz_fac, arm):
        """
        Build spiral arms for tkinter display using the logarithmic spiral formula.
        
        This method creates the coordinates for the galaxy's spiral arms based on logarithmic spirals,
        simulating a realistic spiral galaxy appearance.

        Parameters:
        - b (float): Shape parameter for the spiral (affects the tightness of the spiral).
        - r (float): Radius parameter affecting the spread of the spiral arms.
        - rot_fac (float): Rotation factor, affecting the number of twists.
        - fuz_fac (float): Fuzziness factor, adding randomness to the arm's shape.
        - arm (int): Number of spiral arms in the galaxy.

        Returns:
        - None (Typically, this function would generate coordinates or a visual representation).

        The method uses a mathematical model to create the spiral structure, often visualized
        using libraries like tkinter for a 2D representation of the galaxy.
        """
        spiral_stars = []
        fuzz = int(0.030 * abs(r)) # randomly shift star locations
        theta_max_degrees = 520
        for i in range(theta_max_degrees): # range(0, 600, 2) for no black hole
            theta = math.radians(i)
            x = r * math.exp(b * theta) * math.cos(theta + pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            y = r * math.exp(b * theta) * math.sin(theta + pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            spiral_stars.append((x,y))
        for x, y in spiral_stars:
            if arm == 0 and int(x % 2) == 0:
               c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='') 
            elif arm == 0 and int(x % 2) != 0:
                c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
