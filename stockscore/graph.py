import matplotlib.pyplot as plt

plt.rcdefaults()


def plot_top(df):
    """Plot stocks based on total score.

    Args:
      df(pandas.DataFrame): Stock score pandas.DataFrame

    Returns:
      Matplotlib plot with stocks and scores (broken down by score id)

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
    plt.title("Top {num} Stock Scores".format(num=len(df)))
    plt.show(block=True)
