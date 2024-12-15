#import numpy as np
import pandas as pd

# Load datasets
pokemon_df = pd.read_csv("DataSets/pokemon.csv")
combats_df = pd.read_csv("DataSets/combats.csv")

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

# Apply One-Hot Encoding to the Type columns
combats_df_OneHot = pd.get_dummies(
    combats_df, columns=["P1_Type1", "P1_Type2", "P2_Type1", "P2_Type2"]
).astype(int)

# Preview the transformed data
print(combats_df.head())
print(combats_df_OneHot.head())
print(combats_df_OneHot.info())

# Define the desired column order
desired_columns = [
    "P1_HP",
    "P1_Attack",
    "P1_Defense",
    "P1_Sp.Atk",
    "P1_Sp.Def",
    "P1_Speed",
    "P1_Legendary",
    "P1_Type1_Bug",
    "P1_Type1_Dark",
    "P1_Type1_Dragon",
    "P1_Type1_Electric",
    "P1_Type1_Fairy",
    "P1_Type1_Fighting",
    "P1_Type1_Fire",
    "P1_Type1_Flying",
    "P1_Type1_Ghost",
    "P1_Type1_Grass",
    "P1_Type1_Ground",
    "P1_Type1_Ice",
    "P1_Type1_Normal",
    "P1_Type1_Poison",
    "P1_Type1_Psychic",
    "P1_Type1_Rock",
    "P1_Type1_Steel",
    "P1_Type1_Water",
    "P1_Type2_Bug",
    "P1_Type2_Dark",
    "P1_Type2_Dragon",
    "P1_Type2_Electric",
    "P1_Type2_Fairy",
    "P1_Type2_Fighting",
    "P1_Type2_Fire",
    "P1_Type2_Flying",
    "P1_Type2_Ghost",
    "P1_Type2_Grass",
    "P1_Type2_Ground",
    "P1_Type2_Ice",
    "P1_Type2_Normal",
    "P1_Type2_Poison",
    "P1_Type2_Psychic",
    "P1_Type2_Rock",
    "P1_Type2_Steel",
    "P1_Type2_Water",
    "P2_HP",
    "P2_Attack",
    "P2_Defense",
    "P2_Sp.Atk",
    "P2_Sp.Def",
    "P2_Speed",
    "P2_Legendary",
    "P2_Type1_Bug",
    "P2_Type1_Dark",
    "P2_Type1_Dragon",
    "P2_Type1_Electric",
    "P2_Type1_Fairy",
    "P2_Type1_Fighting",
    "P2_Type1_Fire",
    "P2_Type1_Flying",
    "P2_Type1_Ghost",
    "P2_Type1_Grass",
    "P2_Type1_Ground",
    "P2_Type1_Ice",
    "P2_Type1_Normal",
    "P2_Type1_Poison",
    "P2_Type1_Psychic",
    "P2_Type1_Rock",
    "P2_Type1_Steel",
    "P2_Type1_Water",
    "P2_Type2_Bug",
    "P2_Type2_Dark",
    "P2_Type2_Dragon",
    "P2_Type2_Electric",
    "P2_Type2_Fairy",
    "P2_Type2_Fighting",
    "P2_Type2_Fire",
    "P2_Type2_Flying",
    "P2_Type2_Ghost",
    "P2_Type2_Grass",
    "P2_Type2_Ground",
    "P2_Type2_Ice",
    "P2_Type2_Normal",
    "P2_Type2_Poison",
    "P2_Type2_Psychic",
    "P2_Type2_Rock",
    "P2_Type2_Steel",
    "P2_Type2_Water",
    "Target",
]

# Reorder the dataframe
combats_df_OneHot = combats_df_OneHot[desired_columns]

# Preview the reordered dataframe
print(combats_df_OneHot.head())
print(combats_df_OneHot.info())

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Step 1: Standardize the data
scaler = StandardScaler()
combats_df_scaled = scaler.fit_transform(combats_df_OneHot)

# Step 2: Apply PCA
# Retain 95% of variance
pca = PCA(n_components=0.95)
combats_df_pca = pca.fit_transform(combats_df_scaled)

# Step 3: Check the shape of the reduced dataset
print("Original shape:", combats_df_OneHot.shape)
print("Reduced shape:", combats_df_pca.shape)

combats_df_OneHot.info()

# Step 4: Optional - Variance explained by each component
explained_variance = pca.explained_variance_ratio_
print("Explained variance ratio by components:", explained_variance)

