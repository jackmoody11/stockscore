from stockscore.data import Stocks


class Scores(Stocks):
    """Scores for stocks. """

    def __init__(self, stocks=None):
        super().__init__(stocks)
        if self.scores is None:
            self.init_scores()

    def moving_avg_screen(self):
        """Test percent diff in 50 day SMA and 200 day SMA. """
        if self.stats is None:
            self.get_stats()
        self.stats["perDiff"] = (
            (self.stats["day50MovingAvg"] - self.stats["day200MovingAvg"])
            / self.stats["day200MovingAvg"]
        ) * 100
        self.scores.loc[
            self.stats["perDiff"].between(0, 5, inclusive=False), [
                "Momentum Score"]
        ] += 1

    def trading_volume_screen(self):
        """Test volume of stock for liquidity. """
        if self.volume is None:
            self.get_volume()
        self.scores.loc[
            self.volume["latestVolume"] >= 10**5, [
                "Value Score", "Momentum Score"]
        ] += 1
        self.scores.loc[
            self.volume["latestVolume"] <= 50000, [
                "Value Score", "Momentum Score"]
        ] -= 1

    def splits_screen(self, time="1y"):
        """Test for stock splits in the past.

        Args:
          time:  (Default value = "1y")
              Amount of time to test for splits. Choose from
              # finish this...

        Returns:

        """

        if self.splits is None:
            self.get_splits()
        self.splits = self.get_splits(
            time=time) if self.splits is None else self.splits
        for symbol, _ in self.scores.iterrows():
            try:
                symbol_splits = self.splits[symbol]
                num_splits = len(symbol_splits)
                split_ratios = [symbol_splits[i]["ratio"]
                                for i in range(num_splits)]
                if num_splits > 0 and all(
                    split_ratios[i] < 1 for i in range(num_splits)
                ):
                    # Stocks that split so that you get 7 stock for every 1 you
                    # own may indicate good future prospects
                    # They probably feel good about future prospects and want to allow more
                    # investors to invest in them
                    pts = num_splits
                    self.scores.loc[symbol, [
                        "Momentum Score", "Growth Score"]] += pts
                elif num_splits > 0:
                    # Stocks that split so that you get 1 stock for every 7
                    # you own may indicate poor future prospects
                    # They may be worried about staying in the market
                    # and need to maintain some minimum price to keep trading
                    pts = sum(1 for i in range(num_splits)
                              if split_ratios[i] > 1)
                    self.scores.loc[symbol, [
                        "Momentum Score", "Growth Score"]] -= pts
            except (ValueError, KeyError):
                continue

    def net_income_screen(self):
        """Test for net income over the past quarters. """
        # Get data for screen
        if self.financials is None:
            self.get_financials()
        self.financials = (
            self.get_financials() if self.financials is None else self.financials
        )
        # Give score based on net income results from the past year
        for symbol in self.financials:
            try:
                symbol_financials = self.financials[symbol]["financials"]["financials"]
                quarters = len(symbol_financials)
                try:
                    if all(
                        symbol_financials[i]["netIncome"] > 0 for i in range(quarters)
                    ):
                        pts = quarters
                        self.scores.loc[symbol][
                            "Value Score"
                        ] += pts  # positive net income for all quarters reporting
                except (KeyError, TypeError):
                    continue
            except (KeyError, TypeError):
                continue  # Skip to next stock if unable to get data

    def current_ratio_screen(self):
        """Test if current ratio is in some range. """
        # Get data for screen
        if self.financials is None:
            self.get_financials()
        # Give score based on current ratio
        # (measure of ability to cover short term debt obligations)
        for symbol, _ in self.scores.iterrows():
            try:
                fin_base = self.financials[symbol]["financials"]["financials"][0]
                current_assets = fin_base["currentAssets"]
                current_debt = fin_base["currentDebt"]
                try:
                    current_ratio = current_assets / current_debt
                    if current_ratio >= 1.5:
                        self.scores.loc[symbol]["Value Score"] += 2
                    elif current_ratio >= 1:
                        self.scores.loc[symbol]["Value Score"] += 1
                except ZeroDivisionError:
                    if isinstance(current_assets, int or float) and current_assets > 0:
                        self.scores.loc[symbol][
                            "Value Score"
                        ] += 1  # company has no short term obligations to pay
                    continue  # If data is bad, skip to next stock
                except TypeError:
                    if (
                        current_debt is None
                        and current_assets is not None
                        and current_assets > 0
                    ):
                        self.scores.loc[symbol][
                            "Value Score"
                        ] += 1  # company has no short term obligations to pay
                    continue  # If data is bad, skip to next stock
            except (KeyError, TypeError):
                continue  # If current assets and current debt stats
                # are not available, skip to next stock

    def pb_ratio_screen(self):
        """Test if price/book is in range. """
        # Get data for screen
        if self.stats is None:
            self.get_stats()
        # Give score based on price/book ratio - criteria taken
        # from Ben Graham's Intelligent Investor
        self.scores.loc[
            (self.stats["priceToBook"] <= 1.2) & (
                self.stats["priceToBook"] > 0),
            ["Value Score"],
        ] += 1

    def pe_ratio_screen(self):
        """Test if price/earnings is in range. """
        # Get data for screen
        if self.stats is None:
            self.get_stats()
        if self.close is None:
            self.get_close()
        # Give score based on price/earnings ratio
        self.stats.loc[
            (self.stats["ttmEPS"] > 0) & (self.close["close"] > 0), "peRatio"
        ] = (
            self.close[(self.stats["ttmEPS"] > 0) & (
                self.close["close"] > 0)]["close"]
            / self.stats[(self.stats["ttmEPS"] > 0) & (self.close["close"] > 0)][
                "ttmEPS"
            ]
        )
        self.scores.loc[self.stats["peRatio"] <= 30, "Value Score"] += 1
        self.scores.loc[self.stats["peRatio"] <= 15, "Value Score"] += 1

    def profit_margin_screen(self):
        """Check if profit margin is in range. """
        if self.stats is None:
            self.get_stats()
        self.scores.loc[self.stats["profitMargin"] > 10, "Value Score"] += 1
        self.scores.loc[self.stats["profitMargin"] > 20, "Value Score"] += 1

    # Needs updating
    def dividend_screen(self):
        """Check if dividends paid over past quarters """
        if self.dividends is None:
            self.get_dividends()
        # Get data for screen
        self.scores.loc[:, "Value Score"] += self.dividends["count"] // 4
        # Need to account for monthly dividend stocks (add max function to exclude
        # monthly dividend payers from being disproportionately rewarded

    def score(self):
        """Run all screens. """
        self.moving_avg_screen()
        self.trading_volume_screen()
        self.splits_screen()
        self.net_income_screen()
        self.current_ratio_screen()
        self.p_to_b_screen()
        self.pe_ratio_screen()
        self.profit_margin_screen()

        _scores = ["Value Score", "Growth Score", "Momentum Score"]
        self.scores["Score"] = sum([self.scores[_score] for _score in _scores])
