# Importing required libraries
import numpy as np
import pandas as pd
import sklearn
import joblib 

print("numpy",np.__version__)
print("pandas",pd.__version__)
print("sklearn",sklearn.__version__)
print("joblib",joblib.__version__)

# Load the datasets
# pokemon_df contains information about each Pokemon
# combats_df contains information about battles between Pokemon
pokemon_df = pd.read_csv(
    "/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/pokemon.csv"
)
combats_df = pd.read_csv(
    "/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/combats.csv"
)

# Preview the first few rows and structure of each dataset
print(pokemon_df.head())  # First few rows of Pokemon dataset
print(pokemon_df.info())  # Information about columns in Pokemon dataset
print(combats_df.head())  # First few rows of Combats dataset
print(combats_df.info())  # Information about columns in Combats dataset

# Fill missing values in the "Type 2" column with "Normal"
# This assumes that Pokemon without a secondary type are treated as having "Normal" as Type 2
pokemon_df["Type 2"] = pokemon_df["Type 2"].fillna("Normal")
print(pokemon_df.head())  # Confirm changes
print(pokemon_df.info())  # Confirm column updates

# Merge Pokemon stats into the Combats dataset for the first Pokemon
combats_df = combats_df.merge(
    pokemon_df, left_on="First_pokemon", right_on="#", suffixes=("", "_P1")
)

# Merge Pokemon stats into the Combats dataset for the second Pokemon
combats_df = combats_df.merge(
    pokemon_df, left_on="Second_pokemon", right_on="#", suffixes=("", "_P2")
)

# Verify the structure and contents of the merged dataframe
print(combats_df.head())
print(combats_df.info())

# Drop unnecessary columns to clean up the data
combats_df.drop(
    columns=["#", "#_P2", "Generation", "Generation_P2"],
    inplace=True,
)
print(combats_df.head())
print(combats_df.info())

# Rename columns for clarity, adding P1 (Player 1) and P2 (Player 2) prefixes
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
print(combats_df.info())

# Convert the Legendary columns to integers: 1 for True, 0 for False
combats_df["P1_Legendary"] = combats_df["P1_Legendary"].astype(int)
combats_df["P2_Legendary"] = combats_df["P2_Legendary"].astype(int)

print(combats_df.head())
print(combats_df.info())

# Create a target column: 1 if P1 wins, 0 otherwise
combats_df["Target"] = (combats_df["Winner"] == combats_df["P1"]).astype(int)

print(combats_df.head())
print(combats_df.info())

# Drop columns that won't be used for training the model
combats_df.drop(
    columns=[
        "Winner",  # Already encoded as "Target"
        "P1",  # IDs are redundant after merging stats
        "P2",  # IDs are redundant after merging stats
        "P1_Name",  # Names are not useful for training
        "P2_Name",  # Names are not useful for training
    ],
    inplace=True,
)

print(combats_df.head())
print(combats_df.info())


# Function to apply target encoding: replace categories with their average target values
def target_encode(df, column, target_column):
    means = df.groupby(column)[
        target_column
    ].mean()  # Calculate mean target for each category
    return df[column].map(means)  # Map category to its mean target value


# Apply target encoding to the Type columns
for column in ["P1_Type1", "P1_Type2", "P2_Type1", "P2_Type2"]:
    combats_df[column] = target_encode(combats_df, column, "Target")

# Verify the transformed data
print(combats_df.head())
print(combats_df.info())

# Separate features (X) and target (y)
X = combats_df.drop(columns=["Target"])  # Input features
y = combats_df["Target"]  # Target variable (whether P1 wins)

# Split data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Print sizes of training and testing sets
print("Training set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Train a Random Forest model
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # Fit the model to the training data

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model
from sklearn.metrics import accuracy_score, classification_report

# Calculate accuracy: the percentage of correct predictions
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Print a detailed classification report
print("Classification Report:\n", classification_report(y_test, y_pred))

import joblib  # For saving and loading models

# Save the trained model using joblib
joblib.dump(model, "pokemon_battle_1v1_model.joblib")
print("Model saved to 'pokemon_battle_1v1_model.joblib'.")

# Load the model (if needed later)
loaded_model = joblib.load("pokemon_battle_1v1_model.joblib")
print("Loaded model successfully!")

"""
print(combats_df["P1_Type1"].unique())
print(combats_df["P1_Type2"].unique())

print(combats_df["P2_Type1"].unique())
print(combats_df["P2_Type2"].unique())

p1_type1_encoding = combats_df.groupby("P1_Type1")["Target"].mean().to_dict()
p1_type2_encoding = combats_df.groupby("P1_Type2")["Target"].mean().to_dict()

p2_type1_encoding = combats_df.groupby("P2_Type1")["Target"].mean().to_dict()
p2_type2_encoding = combats_df.groupby("P2_Type2")["Target"].mean().to_dict()

print(p1_type1_encoding)
print(p1_type2_encoding)

print(p2_type1_encoding)
print(p2_type2_encoding)
"""

"""
['Rock' 'Grass' 'Fairy' 'Fire' 'Bug' 'Psychic' 'Fighting' 'Water' 'Normal'
 'Ground' 'Electric' 'Dark' 'Ice' 'Dragon' 'Steel' 'Ghost' 'Flying'
 'Poison']
 
['Ground' 'Fighting' 'Flying' 'Normal' 'Water' 'Electric' 'Dark' 'Ice'
 'Steel' 'Ghost' 'Rock' 'Fairy' 'Psychic' 'Poison' 'Dragon' 'Grass' 'Fire'
 'Bug']
 
['Grass' 'Rock' 'Psychic' 'Dragon' 'Bug' 'Steel' 'Ice' 'Ghost' 'Water'
 'Electric' 'Dark' 'Fire' 'Normal' 'Poison' 'Fairy' 'Fighting' 'Ground'
 'Flying']
 
['Dark' 'Fighting' 'Normal' 'Rock' 'Ghost' 'Psychic' 'Dragon' 'Ground'
 'Flying' 'Fairy' 'Steel' 'Fire' 'Electric' 'Bug' 'Water' 'Grass' 'Ice'
 'Poison']

p1_type1_encoding:->
{'Bug': 0.4019607843137255,
 'Dark': 0.6054997355896351,
 'Dragon': 0.6137055837563452,
 'Electric': 0.6126840317100792,
 'Fairy': 0.3062200956937799,
 'Fighting': 0.4370860927152318,
 'Fire': 0.5627679118187385,
 'Flying': 0.743801652892562,
 'Ghost': 0.4151133501259446,
 'Grass': 0.4214235377026075,
 'Ground': 0.5137662337662338,
 'Ice': 0.4082721814543029,
 'Normal': 0.5008280887711163,
 'Poison': 0.40166204986149584,
 'Psychic': 0.528969957081545,
 'Rock': 0.3767813694820994,
 'Steel': 0.3742191936399773,
 'Water': 0.4439059158945118}
 
 p1_type2_encoding:->
 {'Bug': 0.4504950495049505,
 'Dark': 0.5783227848101266,
 'Dragon': 0.5720411663807891,
 'Electric': 0.5142118863049095,
 'Fairy': 0.42644978783592646,
 'Fighting': 0.6700782661047562,
 'Fire': 0.5981554677206851,
 'Flying': 0.6470011439777742,
 'Ghost': 0.19437652811735942,
 'Grass': 0.38664904163912756,
 'Ground': 0.34629133154602326,
 'Ice': 0.5590909090909091,
 'Normal': 0.4395269295751432,
 'Poison': 0.4343675417661098,
 'Psychic': 0.491600790513834,
 'Rock': 0.25792349726775954,
 'Steel': 0.46016381236038717,
 'Water': 0.37219251336898396}
 
 p2_type1_encoding->
 {'Bug': 0.540695016003658,
 'Dark': 0.3336745138178096,
 'Dragon': 0.3470948012232416,
 'Electric': 0.3522432332220986,
 'Fairy': 0.6500904159132007,
 'Fighting': 0.5033434650455927,
 'Fire': 0.4023128423615338,
 'Flying': 0.2288135593220339,
 'Ghost': 0.45241809672386896,
 'Grass': 0.5411369633005517,
 'Ground': 0.4404276985743381,
 'Ice': 0.5284810126582279,
 'Normal': 0.42343234323432344,
 'Poison': 0.5424553812871823,
 'Psychic': 0.43596881959910916,
 'Rock': 0.5648280802292264,
 'Steel': 0.5159663865546219,
 'Water': 0.5082550526615428}
 
 p2_type2_encoding->
 {'Bug': 0.5522388059701493,
 'Dark': 0.38661417322834646,
 'Dragon': 0.36538461538461536,
 'Electric': 0.45093457943925236,
 'Fairy': 0.5678571428571428,
 'Fighting': 0.31522388059701495,
 'Fire': 0.32249674902470743,
 'Flying': 0.3187540348612008,
 'Ghost': 0.3024390243902439,
 'Grass': 0.55794806839772,
 'Ground': 0.5985853227232537,
 'Ice': 0.3995459704880817,
 'Normal': 0.5069759762238917,
 'Poison': 0.531009738595592,
 'Psychic': 0.46465138956606533,
 'Rock': 0.6940382452193475,
 'Steel': 0.460546282245827,
 'Water': 0.5551801801801802}
"""


# Assuming you already have the Pokémon dataset loaded
pokemon_df__ = pd.read_csv(
    "/Users/atharv/Desktop/Ashish GitHub/pokemon/DataSets/pokemon.csv"
)

# Fill NaN values in Type 2
pokemon_df__["Type 2"] = pokemon_df__["Type 2"].fillna("Normal")


# Function to preprocess and encode Pokémon data
def preprocess_pokemon(pokemon_name, pokemon_df__, target_encodings):
    # Fetch Pokémon details
    pokemon = pokemon_df__[pokemon_df__["Name"] == pokemon_name].iloc[0]
    # Prepare the dictionary for features
    features = {
        "Type1": target_encodings["Type1"].get(pokemon["Type 1"], 0),
        "Type2": target_encodings["Type2"].get(pokemon["Type 2"], 0),
        "HP": pokemon["HP"],
        "Attack": pokemon["Attack"],
        "Defense": pokemon["Defense"],
        "Sp.Atk": pokemon["Sp. Atk"],
        "Sp.Def": pokemon["Sp. Def"],
        "Speed": pokemon["Speed"],
        "Legendary": int(pokemon["Legendary"]),
    }
    return features


# Assume we have target encoding mappings from training data
# (Replace this with actual encoding mappings from the training phase)
target_encodings = {
    "Type1": {
        "Bug": 0.4019607843137255,
        "Dark": 0.6054997355896351,
        "Dragon": 0.6137055837563452,
        "Electric": 0.6126840317100792,
        "Fairy": 0.3062200956937799,
        "Fighting": 0.4370860927152318,
        "Fire": 0.5627679118187385,
        "Flying": 0.743801652892562,
        "Ghost": 0.4151133501259446,
        "Grass": 0.4214235377026075,
        "Ground": 0.5137662337662338,
        "Ice": 0.4082721814543029,
        "Normal": 0.5008280887711163,
        "Poison": 0.40166204986149584,
        "Psychic": 0.528969957081545,
        "Rock": 0.3767813694820994,
        "Steel": 0.3742191936399773,
        "Water": 0.4439059158945118,
    },  # Example values
    "Type2": {
        "Bug": 0.4504950495049505,
        "Dark": 0.5783227848101266,
        "Dragon": 0.5720411663807891,
        "Electric": 0.5142118863049095,
        "Fairy": 0.42644978783592646,
        "Fighting": 0.6700782661047562,
        "Fire": 0.5981554677206851,
        "Flying": 0.6470011439777742,
        "Ghost": 0.19437652811735942,
        "Grass": 0.38664904163912756,
        "Ground": 0.34629133154602326,
        "Ice": 0.5590909090909091,
        "Normal": 0.4395269295751432,
        "Poison": 0.4343675417661098,
        "Psychic": 0.491600790513834,
        "Rock": 0.25792349726775954,
        "Steel": 0.46016381236038717,
        "Water": 0.37219251336898396,
    },  # Example values
}

# Take Pokémon names as input
pokemon_1 = input("Enter the name of the first Pokémon: ")
pokemon_2 = input("Enter the name of the second Pokémon: ")

# Preprocess Pokémon data
p1_data = preprocess_pokemon(pokemon_1, pokemon_df__, target_encodings)
p2_data = preprocess_pokemon(pokemon_2, pokemon_df__, target_encodings)

# Combine into a single input row
combined_data = {
    "P1_Type1": p1_data["Type1"],
    "P1_Type2": p1_data["Type2"],
    "P1_HP": p1_data["HP"],
    "P1_Attack": p1_data["Attack"],
    "P1_Defense": p1_data["Defense"],
    "P1_Sp.Atk": p1_data["Sp.Atk"],
    "P1_Sp.Def": p1_data["Sp.Def"],
    "P1_Speed": p1_data["Speed"],
    "P1_Legendary": p1_data["Legendary"],
    "P2_Type1": p2_data["Type1"],
    "P2_Type2": p2_data["Type2"],
    "P2_HP": p2_data["HP"],
    "P2_Attack": p2_data["Attack"],
    "P2_Defense": p2_data["Defense"],
    "P2_Sp.Atk": p2_data["Sp.Atk"],
    "P2_Sp.Def": p2_data["Sp.Def"],
    "P2_Speed": p2_data["Speed"],
    "P2_Legendary": p2_data["Legendary"],
}

# Convert to DataFrame
input_df = pd.DataFrame([combined_data])
print("Prepared Input Data:\n", input_df)

# Make prediction
prediction = model.predict(input_df)
print("Prediction (1 = P1 Wins, 0 = P2 Wins):", prediction)
