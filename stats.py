import matplotlib.pyplot as plt
from database import get_count

# creates a bar chart showing the number of games won and lost
def game_stats():
    all_counts = get_count()
    win_count = all_counts[0][0]
    lose_count = all_counts[1][0]

    categories = ["Games Won", "Games Lost"]
    counts = [win_count, lose_count]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(categories, counts, color=['Cyan', 'Lime'])
    ax.set_title("Games Won vs. Lost")
    ax.set_xlabel("Game Outcome")
    ax.set_ylabel("Number of Games")

    return fig
