import math

import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import pandas as pd
import re

from data import alias, CIV_COLORS

# https://docs.google.com/spreadsheets/d/1M-PMRjR0yQp3y8HOZnvByBMiYOfVAcDcgtAegZ6Qs4Q/edit#gid=0
df = pd.read_csv('wars.tsv', delimiter='\t')

# df['Rank'] = df['End'].rank(ascending=True)
# df.set_index('Rank', inplace=True)


def process_name(name: str):
    name = name.strip()
    name = name.replace(" Empire", "")
    name = name.replace("Republic of ", "")
    name = name.replace("Kingdom of ", "")
    name = name.replace("The ", "")

    if name in alias:
        name = alias[name]

    counter[name] += 1
    return name


counter = Counter()


def parse_player(player):
    print(player)
    result = re.split(r'[,()\-]', player)
    result = [process_name(r) for r in result]
    return result


civ_colors = defaultdict(lambda: 'k')
for civ in CIV_COLORS:
    civ_colors[civ] = [x / 255 for x in CIV_COLORS[civ]["territory"]]


# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


# Function to calculate Elo rating
def compute_elo_rank(winner_rating, loser_rating, k=30):
    # Expected probability
    Pb = probability(winner_rating, loser_rating)
    Pa = probability(loser_rating, winner_rating)

    winner_diff = k * (1 - Pa)
    loser_diff = k * (0 - Pb)
    return winner_diff, loser_diff


ratings = defaultdict(lambda: 1200)
# ratings['Byzantine'] = 1500
# ratings['Papal States'] = 1500
# ratings['Austria'] = 1200
play_time_rating = defaultdict(defaultdict)

for index, row in df.iterrows():
    # Access the values in each column
    war = row['War']
    end = row['End']
    #     print(row['Winner'])
    winners = parse_player(row['Winner'])
    losers = parse_player(row['Loser'])

    winner_rating = sum(ratings[w] for w in winners) / len(winners)
    loser_rating = sum(ratings[l] for l in losers) / len(losers)
    # ...
    # Call the compute_elo_rank function with the values from the row
    winner_diff, loser_diff = compute_elo_rank(winner_rating, loser_rating)

    for w in winners:
        ratings[w] += winner_diff
        play_time_rating[w][end] = ratings[w]
    for l in losers:
        ratings[l] += loser_diff
        play_time_rating[l][end] = ratings[l]

# Create a plot with a specific size
plt.figure(figsize=(8, 6))

for p in ['England', 'France', 'Portugal', 'Spain', 'Austria', 'Russia', \
          'Prussia', 'Denmark', 'Sweden', 'Ottomans', 'Netherlands', 'Poland', \
          'Venice', 'Sardinia', 'Papal States', 'United States']:
    # Plotting Player 1

    sorted_dict = {k: play_time_rating[p][k] for k in sorted(play_time_rating[p])}
    #     print(p, sorted_dict)
    plt.plot(sorted_dict.keys(), sorted_dict.values(), label=p, color=civ_colors[p])

plt.xlabel('Time')
plt.ylabel('Scores')
plt.title('Players\' Scores over Time')

# Add a legend
plt.legend()

# Show the plot
plt.savefig('score.png')

print(counter)
