import numpy as np
import math





# *********** DRAKES EQUATION ****************

# N = R^* f(p) n(e) f(l) f(i) f(c) L

#       N =     The number of civilizations in or galaxy whose electromagnetic emissions are detectable
#       R^* =   The avg rate of star formation in the galaxy (new stars per year)
#       f(p) =  The fraction of stars with planets
#       n(e) =  For stars with planets, the avg number of planets with an enveironment suitable for life
#       f(l) =  The fraction of planets that develop life
#       f(i) =  The fraction of life-bearing planets with intelligent, civilized life
#       f(c) =  The fraction of civilizations that release detectable signs of their existence into space
#       L =     The length of time -- in years -- over which the civilizations release the detectable signals


#       ** Recent studies have indicated that n(e) is in between 10% and 40% of all planets may be suitable for SOME FORM of life. 

#                   DRAKE INPUTS TABLE

#       Parameter       Drake 1961          Drake 2017          Used in Model
#         R^*               1                   3                   2
#       f(p)                0.35                1                   .8
#       n(e)                3                   0.2                 0.2
#       f(l)                1                   0.13                0.5
#       f(i)                1                   1                   1
#       f(c)                0.15                0.2                 0.1
#       L                   50E6                1E9                 1,000
#       N                   7.9E6               15.6E6


# Calculating N

# Estimate each parameter:

# 𝑅* = The rate of star formation in our galaxy. Current estimates suggest that approximately 1–3 new stars form in the Milky Way per year. Let's use 2 stars per year as an example.
# 𝑓(p) = The fraction of stars with planetary systems. Observations from missions like Kepler suggest this is quite high, around 0.7 to 1.0. Let's use 1.0 for simplicity.
# 𝑛(e) = The average number of planets per star that could support life. Recent exoplanet studies suggest there may be 0.1 to 0.2 habitable planets per star. Let's use 0.2.
# 𝑓(l) = The fraction of those planets where life actually appears. This is highly uncertain; some optimistic estimates place this at 1 (life will develop if conditions allow), while others suggest it might be much lower. Let's use 0.5.
# 𝑓(i) = The fraction of planets with life where intelligent life evolves. Again, this is very uncertain. Let's use 0.1.
# 𝑓(c) = The fraction of civilizations that develop detectable technology. This could be quite low, as technological civilizations might not last long or might not use technology that is easily detectable. Let's use 0.1.
# 𝐿 = The length of time civilizations release detectable signals. If we assume civilizations like ours release detectable signals for about 1,000 years on average, we use L = 1,000 years.  For persective, as of 2024, Earth has been releasing detectable signals for 124 years.  The first long range radio transmissions began arouund 1901.


# *************** CONSTANTS *********************

L_1961 = 50E6
L_2017 = 15.6E6
L_weighted_avg = (.2*L_1961 + .8*L_2017) / 2 #weighted average using 80% on recent data


R_ = 2 # R^*
f_p = 0.8
n_e = 0.2
f_l = 0.5
f_i = 1
f_c = 0.1
L = 1000



# CALCULATION OF DRAKE'S NUMBER

DRAKE_NUMBER = R_ * f_p * n_e * f_l * f_i * f_c * L 

print(f"Drake's Number: {DRAKE_NUMBER: ,.0f}")
