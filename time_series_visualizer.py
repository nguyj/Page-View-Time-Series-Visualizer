import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=["date"])

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) &
        (df["value"] <= df["value"].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    plt.rcParams.update(plt.rcParamsDefault)
    plt.style.use("seaborn-v0_8-paper")

    fig = df.plot(kind="line",
                  title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
                  ylabel="Page Views",
                  xlabel="Date",
                  legend=False,
                  color="red",
                  rot=0,
                  linewidth=1,
                  figsize=(15, 5))
    
    fig = fig.figure

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot(kind="bar",
                      title="Average Daily Page Views per Month",
                      xlabel="Years",
                      ylabel="Average Page Views",
                      rot=0,
                      figsize=(15, 5))

    plt.legend(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
               title="Month")

    fig = fig.figure

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
    month_ordered = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axs = plt.subplots(1, 2, squeeze=False, figsize=(15, 5))
    axs[0, 0] = sns.boxplot(data=df_box, x="year", y="value", hue="year", legend=False, ax=axs[0, 0])
    axs[0, 1] = sns.boxplot(data=df_box, x="month", y="value", hue="month", ax=axs[0, 1], order=month_ordered)

    axs[0, 0].set_title("Year-wise Box Plot (Trend)")
    axs[0, 0].set_ylabel("Page Views")
    axs[0, 0].set_xlabel("Year")

    axs[0, 1].set_title("Month-wise Box Plot (Seasonality)")
    axs[0, 1].set_ylabel("Page Views")
    axs[0, 1].set_xlabel("Month")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
