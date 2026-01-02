#!/usr/bin/env python3
"""
Script to update Excel data to add flights for UZBEKISTAN, MALTA, and ARMENIA
"""
import pandas as pd

# Load the Excel file
df = pd.read_excel('data_set_for_AI.xlsx')
df.columns = df.columns.str.strip()

# Column definitions
COL_DESTINATIONS = 'רשימות מדינות היעד של לוח הטיסות'

# Find row indices for the target countries
target_countries = ['UZBEKISTAN', 'MALTA', 'ARMENIA']

print("Current status of target countries:")
for country in target_countries:
    dest_row = df[df[COL_DESTINATIONS] == country]
    if not dest_row.empty:
        idx = dest_row.index[0]
        print(f"{country}: row {idx}")
        
        # Show current airline statuses
        for col in df.columns:
            if col not in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', COL_DESTINATIONS]:
                status = dest_row.iloc[0][col]
                if pd.notna(status):
                    print(f"  {col}: {status}")
    else:
        print(f"{country}: not found")

print("\nAvailable airlines:")
for i in range(3, min(10, len(df.columns))):  # Skip first 3 metadata columns
    print(f"  {df.columns[i]}")

# Airlines to assign for each destination (based on realistic routes)
assignments = {
    'UZBEKISTAN': ['EMIRATES', 'LUFTHANSA', 'AIR FRANCE'],  # Airlines that might fly to Central Asia
    'MALTA': ['AIR FRANCE', 'LUFTHANSA', 'IBERIA'],        # European airlines for Malta
    'ARMENIA': ['AEROLINEAS ARGENTINAS S.A.', 'LUFTHANSA', 'AIR FRANCE']  # Airlines for Armenia
}

print("\nUpdating flights for destinations...")

# Update the Excel data
for country, airlines in assignments.items():
    dest_row_idx = df[df[COL_DESTINATIONS] == country].index
    if len(dest_row_idx) > 0:
        row_idx = dest_row_idx[0]
        print(f"\nUpdating {country} (row {row_idx}):")
        
        # First, reset all airlines to "לא טסים"
        for col in df.columns:
            if col not in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', COL_DESTINATIONS]:
                df.at[row_idx, col] = 'לא  טסים'
        
        # Then set the assigned airlines to "טסים"
        for airline in airlines:
            if airline in df.columns:
                df.at[row_idx, airline] = 'טסים'
                print(f"  Set {airline} to טסים")
            else:
                print(f"  Warning: {airline} not found in columns")

# Save the updated Excel file
df.to_excel('data_set_for_AI.xlsx', index=False)
print(f"\nUpdated Excel file saved successfully!")

# Verify the changes
print("\nVerifying changes:")
for country in target_countries:
    dest_row = df[df[COL_DESTINATIONS] == country]
    if not dest_row.empty:
        airlines_flying = []
        for col in df.columns:
            if col not in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', COL_DESTINATIONS]:
                status = dest_row.iloc[0][col]
                if status == 'טסים':
                    airlines_flying.append(col)
        print(f"{country}: {len(airlines_flying)} airlines flying - {', '.join(airlines_flying)}")