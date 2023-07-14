import math
from collections import defaultdict


# Initial rating
base_elo = 1200
ratings = defaultdict(lambda: 1200)


# Function to calculate the Probability
def probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


# Function to calculate Elo rating
def compute_elo_rank(winners, losers, k=30):

    for i in range(len(winners)):
        winner = winners[i]
        loser = losers[i]

        # Expected probability
        Pb = probability(ratings[winner], ratings[loser])
        Pa = probability(ratings[loser], ratings[winner])

        # Elo rating update
        if winner in ratings:
            ratings[winner] = ratings[winner] + k * (1 - Pa)
        if loser in ratings:
            ratings[loser] = ratings[loser] + k * (0 - Pb)
    return ratings


# Players list
players = ["player1", "player2", "player3"]

# Winners and losers list
winners = ["player1", "player3", "player2"]
losers = ["player2", "player1", "player3"]

# Using the function
new_ratings = compute_elo_rank(players, winners, losers)

for player, rating in new_ratings.items():
    print(f'{player} : {rating}')
