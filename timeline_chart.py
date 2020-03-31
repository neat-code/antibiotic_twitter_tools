from load_data import DataLoader
import matplotlib.pyplot as plt
import pandas as pd

data_loader = DataLoader()
df = data_loader.format_data()
result = df.plot(x = 'timeStamp', y = 'polarity')
plt.show()
