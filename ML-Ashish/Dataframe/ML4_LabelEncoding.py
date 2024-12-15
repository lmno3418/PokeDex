#import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load datasets
pokemon_df = pd.read_csv("/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/pokemon.csv")
combats_df = pd.read_csv("/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/combats.csv")

# Preview the first few rows of each dataset
print(pokemon_df.head())
print(combats_df.head())

# Replace NaN values in the 'Type 2' column with "Normal"
pokemon_df["Type 2"] = pokemon_df["Type 2"].fillna("Normal")
print(pokemon_df.head())

# Merge Pokemon stats into combats dataframe for the first Pokemon
combats_df = combats_df.merge(
    pokemon_df, left_on="First_pokemon", right_on="#", suffixes=("", "_P1")
)

# Merge Pokemon stats into combats dataframe for the second Pokemon
combats_df = combats_df.merge(
    pokemon_df, left_on="Second_pokemon", right_on="#", suffixes=("", "_P2")
)

print(combats_df.head())

# Drop unnecessary columns from the merged dataframe
combats_df.drop(
    columns=["#", "#_P2", "Generation", "Generation_P2"],
    inplace=True,
)
print(combats_df.head())

# Rename columns for clarity (e.g., adding P1 and P2 prefixes)
combats_df.rename(
    columns={
        "First_pokemon": "P1",
        "Second_pokemon": "P2",
        "Name": "P1_Name",
        "Type 1": "P1_Type1",
        "Type 2": "P1_Type2",
        "HP": "P1_HP",
        "Attack": "P1_Attack",
        "Defense": "P1_Defense",
        "Sp. Atk": "P1_Sp.Atk",
        "Sp. Def": "P1_Sp.Def",
        "Speed": "P1_Speed",
        "Name_P2": "P2_Name",
        "Type 1_P2": "P2_Type1",
        "Type 2_P2": "P2_Type2",
        "HP_P2": "P2_HP",
        "Attack_P2": "P2_Attack",
        "Defense_P2": "P2_Defense",
        "Sp. Atk_P2": "P2_Sp.Atk",
        "Sp. Def_P2": "P2_Sp.Def",
        "Speed_P2": "P2_Speed",
        "Legendary_P2": "P2_Legendary",
        "Legendary": "P1_Legendary",
    },
    inplace=True,
)
print(combats_df.head())

# Convert Legendary columns to integers (1 for True, 0 for False)
combats_df["P1_Legendary"] = combats_df["P1_Legendary"].astype(int)
combats_df["P2_Legendary"] = combats_df["P2_Legendary"].astype(int)

# Create the target column: 1 if P1 is the winner, 0 otherwise
combats_df["Target"] = (combats_df["Winner"] == combats_df["P1"]).astype(int)

print(combats_df.head())

# Drop columns that are not useful for modeling
combats_df.drop(
    columns=[
        "Winner",  # Not needed since we created the Target column
        "P1",  # Redundant after merging stats
        "P2",  # Redundant after merging stats
        "P1_Name",  # Names are not useful for training
        "P2_Name",  # Names are not useful for training
    ],
    inplace=True,
)

print(combats_df.head())
print(combats_df.info())

# Apply Label Encoding to the Type columns
label_encoder = LabelEncoder()

# Encode each type column
for column in ["P1_Type1", "P1_Type2", "P2_Type1", "P2_Type2"]:
    combats_df[column] = label_encoder.fit_transform(combats_df[column])

# Preview the transformed data
print(combats_df.head())
print(combats_df.info())
