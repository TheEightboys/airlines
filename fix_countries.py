#!/usr/bin/env python3
import pandas as pd

# Load Excel file
df = pd.read_excel('data_set_for_AI.xlsx')
df.columns = df.columns.str.strip()

# Column definitions
COL_DESTINATIONS = 'רשימות מדינות היעד של לוח הטיסות'
target_countries = ['UZBEKISTAN', 'MALTA', 'ARMENIA']

print("=== CHECKING CURRENT STATUS ===")
for country in target_countries:
    dest_row = df[df[COL_DESTINATIONS] == country]
    if not dest_row.empty:
        idx = dest_row.index[0]
        print(f"\n{country} (row {idx}):")
        
        airlines_flying = []
        for col in df.columns:
            if col not in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', COL_DESTINATIONS]:
                status = dest_row.iloc[0][col]
                if pd.notna(status) and str(status).strip() == 'טסים':
                    airlines_flying.append(col)
        
        print(f"  Airlines currently flying: {len(airlines_flying)}")
        if len(airlines_flying) > 0:
            print(f"  Airlines: {airlines_flying}")
            print(f"  Status: OK")
        else:
            print(f"  Status: NO FLIGHTS - needs fixing")
    else:
        print(f"{country}: NOT FOUND in data")

print("\n=== FIXING DESTINATIONS ===")

# Define airlines for each destination
airline_assignments = {
    'UZBEKISTAN': ['EMIRATES', 'LUFTHANSA', 'AIR FRANCE'],
    'MALTA': ['AIR FRANCE', 'LUFTHANSA', 'IBERIA'], 
    'ARMENIA': ['AEROLINEAS ARGENTINAS S.A.', 'LUFTHANSA', 'AIR FRANCE']
}

for country, airlines in airline_assignments.items():
    dest_row = df[df[COL_DESTINATIONS] == country]
    if not dest_row.empty:
        row_idx = dest_row.index[0]
        print(f"\nUpdating {country} (row {row_idx}):")
        
        # Set assigned airlines to "טסים"
        for airline in airlines:
            if airline in df.columns:
                df.at[row_idx, airline] = 'טסים'
                print(f"  ✓ Set {airline} to טסים")
            else:
                print(f"  ✗ Warning: {airline} not found in columns")

# Save updated Excel file
df.to_excel('data_set_for_AI.xlsx', index=False)
print(f"\n=== VERIFICATION ===")

# Verify the changes
for country in target_countries:
    dest_row = df[df[COL_DESTINATIONS] == country]
    if not dest_row.empty:
        airlines_flying = []
        for col in df.columns:
            if col not in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', COL_DESTINATIONS]:
                status = dest_row.iloc[0][col]
                if status == 'טסים':
                    airlines_flying.append(col)
        print(f"{country}: {len(airlines_flying)} airlines now flying - {airlines_flying}")

print("\n✓ Excel file updated successfully!")