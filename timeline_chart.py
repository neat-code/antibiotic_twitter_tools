from load_data import DataLoader
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def update_timechart(dataframe, figure_number, title):
    plt.plot(dataframe.groupby([dataframe['timeStamp'].dt.date])['polarity'].mean(), color="r", label="Polarity", markevery=5)
    plt.plot(dataframe.groupby([dataframe['timeStamp'].dt.date])['subjectivity'].mean(), color="b", label="Subjectivity", markevery=5)
    plt.title(title)
    plt.legend()
    plt.show()

data_loader = DataLoader()
df = data_loader.format_data()

# Total Rows
update_timechart(df, 1, "Total")
# Corona Rows
update_timechart(df.loc[df["aboutCorona"]], 2, "Corona")
# Resistance Rows
update_timechart(df.loc[df["aboutResistance"]], 3, "Resistance")
# Virus Rows
update_timechart(df.loc[df["aboutVirus"]], 4, "Virus")

plt.show()
