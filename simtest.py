from utils import Player, Rolls, Game, roll_dice
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###############################################################
# Let's run a simulation to make sure our statistics are good #
###############################################################

# simulate a bunch of rolls
ngames = 500
nrolls = 60
agg = []
cdf_method = 'pb sss'
for sim in range(ngames):
    simrolls = Rolls()
    gsim = Game({'simp1': Player(simrolls)})
    gsim.players['simp1'].add_settlements([2, 3, 6])
    gsim.players['simp1'].add_settlements([5, 3, 11])
    for roll in roll_dice(nrolls):
        gsim.add_roll(roll)

    resources_count = gsim.players['simp1'].resources_count()
    if cdf_method == 'pb':
        lowerbound = 0 if resources_count == 0 else gsim.players['simp1'].get_percentile_from_resources_poibin(resources_count - 1)
        agg.append(random.uniform(lowerbound, gsim.players['simp1'].get_percentile_from_resources_poibin(resources_count)))
    else:
        try:
            pctile = gsim.players['simp1'].get_percentile_from_resources(resources_count)
            lowerbound = 0 if resources_count == 0 else pctile[0]
            agg.append(random.uniform(lowerbound, pctile[1]))
        except:
            print("game {} failed".format(sim))
            raise

    print('simulated game: {}'.format(sim))

# percentiles should be uniform
plt.hist(agg, bins=15)

# should be 45 degree line
agg.sort()
plt.scatter(range(len(agg)), agg)

# checking a few quantiles
df = pd.DataFrame(agg)
df.quantile(np.arange(0, 1, 0.05))

print(gsim.players['simp1'].resources_count())
print(gsim.players['simp1'].get_performance_summary())


