import matplotlib.pyplot as plt

plt.rcdefaults()


def plot_top(tuple_list):
    # Set styling
    plt.style.use("seaborn-darkgrid")
    plt.interactive(False)
    # Custom Font - Download Apple's SF fonts for this to work
    # Otherwise, should default to default font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'SF Pro Display'
    # Set tickers and scores for bar chart
    symbols = [x[0] for x in tuple_list]
    scores = [x[1] for x in tuple_list]
    # Set position for each bar
    y_pos = [i for i in range(len(symbols))]
    # Create bar chart and ticks on x axis
    plt.bar(y_pos, scores, align="center", alpha=0.5)
    plt.xticks(y_pos, symbols)
    # Plot labels
    plt.ylabel("Score")
    plt.xlabel("Tickers")
    plt.title(f"Top {len(scores)} Stock Scores")
    plt.show(block=True)
