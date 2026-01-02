import pandas as pd

# Load the data
df = pd.read_excel('data_set_for_AI.xlsx')
df.columns = df.columns.str.strip()

COL_DESTINATIONS = 'רשימות מדינות היעד של לוח הטיסות'
FLIES = 'טסים'

# Check UZBEKISTAN row
uzbek_rows = df[df[COL_DESTINATIONS].str.contains('UZBEKISTAN', na=False)]
print("UZBEKISTAN rows found:", len(uzbek_rows))
print("\nUZBEKISTAN data:")
for idx, row in uzbek_rows.iterrows():
    print(f"Row {idx}: {row[COL_DESTINATIONS]}")
    
    # Check which airlines fly there
    flying_airlines = []
    for col in df.columns:
        if col in ['חברות התעופה הבכירות', 'הפרש הזמנים (עיכובים)', 'רשימות מדינות היעד של לוח הטיסות']:
            continue
        if pd.notna(row[col]) and str(row[col]).strip() == FLIES:
            flying_airlines.append(col)
    
    print(f"Airlines flying to UZBEKISTAN: {flying_airlines}")

# Check all destinations
all_destinations = df[COL_DESTINATIONS].dropna().unique().tolist()
uzbek_in_list = [d for d in all_destinations if 'UZBEKISTAN' in str(d).upper()]
print(f"\nUZBEKISTAN in destinations list: {uzbek_in_list}")