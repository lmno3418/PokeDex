#import numpy as np
import pandas as pd


pokemon_df = pd.read_csv("/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/pokemon.csv")
combats_df = pd.read_csv("/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/combats.csv")

pokemon_df.head()
combats_df.head()

# Replace NaN in column 'Type2' with a Normal
pokemon_df["Type 2"] = pokemon_df["Type 2"].fillna("Normal")

pokemon_df.head()

combats_df = combats_df.merge(
    pokemon_df, left_on="First_pokemon", right_on="#", suffixes=("", "_P1")
)

combats_df = combats_df.merge(
    pokemon_df, left_on="Second_pokemon", right_on="#", suffixes=("", "_P2")
)

combats_df.head()

combats_df.drop(
    columns=["#", "#_P2", "Generation", "Generation_P2"],
    inplace=True,
)

combats_df.head()

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

combats_df.head()

combats_df["P1_Legendary"] = combats_df["P1_Legendary"].astype(int)
combats_df["P2_Legendary"] = combats_df["P2_Legendary"].astype(int)

combats_df["Target"] = (combats_df["Winner"] == combats_df["P1"]).astype(int)

combats_df.head()
combats_df.info()
