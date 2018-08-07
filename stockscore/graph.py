import matplotlib.pyplot as plt
plt.rcdefaults()


def plot_top(tuple_list):
    symbols = [x[0] for x in tuple_list]
    scores = [x[1] for x in tuple_list]
    y_pos = [i for i in range(len(symbols))]

    plt.bar(y_pos, scores, align='center', alpha=0.5)
    plt.xticks(y_pos, symbols)
    plt.ylabel('Score')
    plt.xlabel('Tickers')
    plt.title('Stock Scores by Ticker')

    plt.show()
