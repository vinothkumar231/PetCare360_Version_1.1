import pandas as pd
import os
import subprocess

# New data to add
new_data = [
    {"text": "My dog has been sneezing a lot and has a runny nose.", "condition": "Respiratory Issues", "record_type": "Owner Observation"},
    {"text": "Cat is lethargic and hasn't eaten in 24 hours.", "condition": "General Health", "record_type": "Owner Observation"},
    {"text": "Found a tick on my dog's ear after hiking.", "condition": "Parasites", "record_type": "Owner Observation"},
    {"text": "Dog is shaking head; ear is red and smelly.", "condition": "Ear Infections", "record_type": "Owner Observation"},
    {"text": "Cat has a bald patch on her tail.", "condition": "Skin Irritations", "record_type": "Owner Observation"},
    {"text": "Auscultation reveals lung crackles and increased respiratory effort.", "condition": "Respiratory Issues", "record_type": "Clinical Notes"},
    {"text": "Prescribe amoxicillin/clavulanate for suspected upper respiratory infection.", "condition": "Respiratory Issues", "record_type": "Clinical Notes"},
    {"text": "Slight limp in hind right leg after intense exercise.", "condition": "Mobility Problems", "record_type": "Owner Observation"},
    {"text": "Dog vomited yellow bile this morning.", "condition": "Digestive Issues", "record_type": "Owner Observation"},
    {"text": "Cat is scratching her ears constantly and has black debris.", "condition": "Ear Infections", "record_type": "Owner Observation"},
    {"text": "Puppy has a distended abdomen and seems uncomfortable.", "condition": "Digestive Issues", "record_type": "Owner Observation"},
    {"text": "Blood smear shows evidence of Babesia infection.", "condition": "Parasites", "record_type": "Clinical Notes"},
    {"text": "Heart rate is elevated, pulse is weak.", "condition": "General Health", "record_type": "Clinical Notes"}
]

csv_path = "models/pet-health-symptoms-dataset.csv"

# Load existing data
df = pd.read_csv(csv_path)

# Create DataFrame for new data
new_df = pd.DataFrame(new_data)

# Append and save
df_combined = pd.concat([df, new_df], ignore_index=True)
df_combined.to_csv(csv_path, index=False)

print(f"Added {len(new_data)} new records to {csv_path}")

# Retrain the model
print("Training model...")
subprocess.run(["python", "train_model.py"])
