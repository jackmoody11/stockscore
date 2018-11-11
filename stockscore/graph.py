import matplotlib.pyplot as plt

plt.rcdefaults()


def plot_top(df):
    """
    :param df: Stock score Pandas DataFrame
    :type df: Pandas DataFrame
    :return: Matplotlib plot with stocks and scores (broken down by score id)
    """
    # Set styling
    plt.style.use("seaborn-darkgrid")
    plt.interactive(False)
    # Custom Font - Download Apple's SF fonts for this to work
    # Otherwise, should default to default font
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "SF Pro Display"
    # Plot DataFrame as bar chart
    df.plot.bar()
    # Plot labels
    plt.ylabel("Score")
    plt.xlabel("Tickers")
    plt.title(f"Top {len(df)} Stock Scores")
    plt.show(block=True)
