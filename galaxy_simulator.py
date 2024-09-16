import tkinter as tk
from random import randint, uniform, random
import math
import numpy as np
import prob_detection


# *************** MAIN INPUT ***************************

# SCALED_DISC_RADIUS = disc_radius / bubble diameter


SCALE = 225 # scaling factor for radio bubble diameter in light-years.  Enter 225 to see Earth's radio bubble

NUM_CIV = 15_600_000 # number of advanced civilizations from Drake equation
pi = np.pi # Establish the constant pi

DISC_RADIUS = 50_000 # Milky Way dimensions in light-years
DISC_HEIGHT = 1_000 # Milky Way dimensions in light-years
DISC_VOLUME = pi * DISC_RADIUS**2 * DISC_HEIGHT # Milky Way volume in cubic light-years


# set up display canvas
root = tk.Tk()
root.title("Milky Way Galaxy")
c = tk.Canvas(root, width=1000, height=800, bg='black') # Sets the dimensions of the Canvas window.  w=1000 and h=800 works well on a laptop.
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400)) # configures how the widget is shown in the canvas window.  To center the widget, these numbers need to be half of the screen size


class Galaxy:
    """
    Class that defines functions to calculate the probability of communication with other civilizations 
    within the Milky Way Galaxy through the use of the Drake Equation. It also includes methods
    for visualizing galaxy features such as spiral arms and generating random polar coordinates.
    
    Attributes:
    - b: Parameter related to the logrithmic spiral equation (constant).
    - r: scaled galactic disc radius.
    - rot_fac: Rotation factor for the galaxy's spiral arms.
    - fuz_fac: Fuzziness factor for the spiral arms to simulate realistic variance. This is a random shift in star position in arm, appied to 'fuzz' variable
    - arm: Number of spiral arms in the galaxy (0 = main arm, 1 = trailing stars).
    """

    def __init__(self, b, r, rot_fac, fuz_fac, arm, density):
        """
        Initialize the Galaxy object with parameters for spiral arm creation and 
        galaxy characteristics.

        Parameters:
        - b: Parameter related to the logrithmic spiral equation (constant).
        - r: scaled galactic disc radius.
        - rot_fac: Rotation factor for the galaxy's spiral arms.
        - fuz_fac: Fuzziness factor for the spiral arms to simulate realistic variance. This is a random shift in star position in arm, appied to 'fuzz' variable
        - arm: Number of spiral arms in the galaxy (0 = main arm, 1 = trailing stars).
        """
        self.b = b
        self.r = r
        self.rot_fac = rot_fac
        self.fuz_fac = fuz_fac
        self.arm = arm 
        self.density = density
    
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
        x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
        y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
        
        return x, y  # x, y will have values between -1 and +1.  This is due to r
    
    def spirals(self, b, r, rot_fac, fuz_fac, arm):
        """
        Build spiral arms for tkinter display using the logarithmic spiral formula.
        
        This method creates the coordinates for the galaxy's spiral arms based on logarithmic spirals,
        simulating a realistic spiral galaxy appearance.

        Parameters:
        - b: Parameter related to the logrithmic spiral equation (constant).
        - r: scaled galactic disc radius.
        - rot_fac: Rotation factor for the galaxy's spiral arms.
        - fuz_fac: Fuzziness factor for the spiral arms to simulate realistic variance. This is a random shift in star position in arm, appied to 'fuzz' variable
        - arm: Number of spiral arms in the galaxy (0 = main arm, 1 = trailing stars).

        Returns:
        - None (Typically, this function would generate coordinates or a visual representation).

        The method uses a mathematical model to create the spiral structure, often visualized
        using libraries like tkinter for a 2D representation of the galaxy.
        """
        spiral_stars = []
        fuzz = int(0.030 * abs(r)) # randomly shift star locations
        theta_max_degrees = 520
        
        for i in range(theta_max_degrees): # range(0, 600, 2) for no black hole, Loop through angle steps to create the spiral
            theta = math.radians(i)
            # Calculate star positions using logarithmic spiral formula and add randomness
            x = r * math.exp(b * theta) * math.cos(theta + pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            y = r * math.exp(b * theta) * math.sin(theta + pi * rot_fac) + randint(-fuzz, fuzz) * fuz_fac
            spiral_stars.append((x,y)) # Store the star coordinates
            
        # Draw stars on the canvas based on the calculated positions
        for x, y in spiral_stars:
            if arm == 0 and int(x % 2) == 0:
               c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='') 
            elif arm == 0 and int(x % 2) != 0:
                c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
            elif arm == 1:
                c.create_oval(x, y, x, y, fill='white', outline='')
    
    def star_haze(disc_radius_scaled, random_polar_coordinates, density):
        """
        Create a diffuse haze of faint stars randomly distributed within the galactic disc.
        
        This function generates a number of small, faint stars and places them at random
        positions within the scaled galactic disc to simulate a star haze or background starfield.
        The number of stars is determined by the scaled radius of the disc and the specified density.

        Args:
            disc_radius_scaled (int): The radius of the galactic disc, scaled to the size of the radio bubble.
                                    This determines the area within which stars will be randomly placed.
            density (int): A multiplier that controls the number of stars generated. A higher density
                        value results in more stars, creating a denser haze.
                        
        Returns:
            None: The function draws stars directly on the tkinter canvas.
        """
        for i in range(0, disc_radius_scaled * density):
            x, y = random_polar_coordinates(disc_radius_scaled)
            c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')

            
    
    
# if __name__ == '__main__':
#     main()
