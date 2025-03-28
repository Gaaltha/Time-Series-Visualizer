import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col=0, parse_dates=True)

# Clean data
df = df.loc[
    (df["value"].quantile(0.025) <= df["value"]) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    df_plot = df.copy()
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))

    x = df_plot.index
    y = df_plot["value"]
    ax.plot(x, y, color="red", lw=0.6)
    
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy() 
    df_bar["year"], df_bar["month"] = df_bar.index.year, df_bar.index.strftime("%B")
    
    df_bar = pd.DataFrame({"mean": df_bar.groupby(["year", "month"])["value"].mean()})
    df_bar = df_bar.unstack()   # unstack "month" from the index ; get a DataFrame with one Series of mean per month (col) per year (rows)

    # Draw bar plot
    fig = df_bar.plot(kind="bar", figsize=(10, 10)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    months =["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    plt.legend(labels=months)


    # # # The Seaborn solution works but does not pass the tests
    # # fig, ax = plt.subplots(figsize=(8,8))
    # # ax = sns.barplot(
    # #     data=df_bar,
    # #     x="year",           # x variable name, the groups
    # #     y="mean",           # y variable name
    # #     hue="month",        # each "month" value in group "year"
    # #     hue_order=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    # #     legend="full"
    # # )

    # # ax.set_xlabel("Years")
    # # ax.set_ylabel("Average Page Views")
    # # ax.legend(title="Months", loc="upper left")
  
  
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(20, 5))
    
    ax1 = sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        hue="year",
        legend=False,
        ax=axs[0]
    )

    ax2 = sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        hue="month",
        order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        legend=False,
        ax=axs[1]
    )

    
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
