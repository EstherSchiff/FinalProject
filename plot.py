import matplotlib.pyplot as plt

# formats the pie chart label to show fractions instead of percentages
def autopct_format(pct):
    numerator = int(round(pct * 5 / 100))
    return f"{numerator}/5"

# displays a pie chart showing using and remaining guesses
def draw_pie_chart(remaining_guesses):
    # Data for the pie chart
    total_guesses = 5
    used = total_guesses - remaining_guesses
    labels = ['Used', 'Remaining']
    sizes = [used, remaining_guesses]
    colors = ['pink', 'cyan']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct=autopct_format, pctdistance=1.25, labeldistance=1.4,
           startangle=90, wedgeprops={'edgecolor': 'black'}, radius=0.5, textprops={"size": "7"})
    return fig
