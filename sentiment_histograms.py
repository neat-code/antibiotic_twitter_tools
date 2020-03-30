import matplotlib.pyplot as plt
from matplotlib.pyplot import subplot, figure
from load_data import DataLoader

def update_histogram(dataframe, metric_column, figure_number, title):
    chart = plt.subplot(2, 4, figure_number)
    chart.hist(dataframe[metric_column])
    chart.set_title(title)

data_loader = DataLoader()
df = data_loader.format_data()

# Total Rows
update_histogram(df, "polarity", 1, "Total Polarity")
update_histogram(df, "subjectivity", 2, "Total Subjectivity")

# Corona Rows
update_histogram(df.loc[df["aboutCorona"]], "polarity", 3, "Corona Polarity")
update_histogram(df.loc[df["aboutCorona"]], "subjectivity", 4, "Corona Subjectivity")

# Resistance Rows
update_histogram(df.loc[df["aboutResistance"]], "polarity", 5, "Resistance Polarity")
update_histogram(df.loc[df["aboutResistance"]], "subjectivity", 6, "Resistance Subjectivity")

# Virus Rows
update_histogram(df.loc[df["aboutVirus"]], "polarity", 7, "Virus Polarity")
update_histogram(df.loc[df["aboutVirus"]], "subjectivity", 8, "Virus Subjectivity")

plt.show()
