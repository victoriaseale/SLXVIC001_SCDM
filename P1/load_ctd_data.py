import pandas as pd

# Load the CTD data file
ctd = pd.read_csv("CTD_data.md", sep="\s+")

# Print the dataframe
print(ctd)
