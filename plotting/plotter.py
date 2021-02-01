from adjustText import adjust_text
import matplotlib.pyplot as plt
import pandas as pd


class Plotter:
    """
    General class for plotting data frames (that have been scraped from pro-football-reference)
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize a plotter
        :param df: The dataframe to plot
        """
        self.df = df

    def plot(self, col1_name: str, col2_name: str, limit: int):
        """
        Plot the data from the two given columns of this plotter's df
        Fails if both columns do not exist
        :param col1_name: str, The name of the first column to plot. Will show up on x-axis of plot
        :param col2_name: str, The name of the second column to plot. Will show up on y-axis of plot
        :param limit: int, The limit of rows to plot (plots the rows up to the limit only)
        """

        # Ensure columns exist in the data frame
        assert col1_name in self.df.columns, f"{col1_name} does not exist in the data frame"
        assert col2_name in self.df.columns, f"{col2_name} does not exist in the data frame"

        # Truncate the df based on limit (without modifying it) and get the data from the appropriate columns
        limited_df = self.df.head(min(len(self.df.index), limit))
        data1 = limited_df[col1_name]
        data2 = limited_df[col2_name]

        # Plot data
        plt.scatter(data1, data2)
        plt.axis([min(0, min(data1)), max(data1), min(0, min(data2)), max(data2)])

        # Annotate points with player names if they exist
        texts = []
        if "Player" in limited_df.columns:
            for index, name in enumerate(limited_df["Player"]):
                texts.append(plt.text(data1[index], data2[index], name))

            # Annotate points in a way that produces minimal overlapping
            adjust_text(texts, force_points=0.2, force_text=0.2,
                        expand_points=(1, 1), expand_text=(1, 1),
                        arrowprops=dict(arrowstyle="-", color='black', lw=0.5))

        # Label axes and show the plot
        plt.xlabel(col1_name)
        plt.ylabel(col2_name)
        plt.show()
