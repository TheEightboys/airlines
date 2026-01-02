import pandas as pd
import os

# Load the data exactly like in app.py
EXCEL_FILE = 'data_set_for_AI.xlsx'
COL_AIRLINES = 'חברות התעופה הבכירות'
COL_DELAYS = 'הפרש הזמנים (עיכובים)'
COL_DESTINATIONS = 'רשימות מדינות היעד של לוח הטיסות'
FLIES = 'טסים'

def load_data():
    """Load and cache the Excel data"""
    file_path = os.path.join(os.path.dirname(__file__), EXCEL_FILE)
    df = pd.read_excel(file_path)
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    return df

df = load_data()

def get_airline_delays():
    """Extract airline delays from the data"""
    delays = {}
    delay_col = COL_DELAYS
    airline_col = COL_AIRLINES
    
    for _, row in df.iterrows():
        airline = row[airline_col]
        delay = row[delay_col]
        
        if pd.isna(airline) or pd.isna(delay):
            continue
        
        try:
            delays[airline] = float(delay)
        except ValueError:
            continue
    
    return delays

def get_airlines_for_destination(destination):
    """Test function"""
    print(f"\n=== Testing destination: {destination} ===")
    
    # Find the row for this destination
    dest_row = df[df[COL_DESTINATIONS] == destination]
    print(f"Found {len(dest_row)} rows for {destination}")
    
    if dest_row.empty:
        print("No rows found!")
        return None
    
    # Get all airline columns (excluding the first 3 metadata columns)
    airline_delays = get_airline_delays()
    print(f"Airline delays loaded: {len(airline_delays)} airlines")
    
    # Find airlines that fly to this destination
    flying_airlines = []
    
    for col in df.columns:
        # Skip non-airline columns
        if col in [COL_AIRLINES, COL_DELAYS, COL_DESTINATIONS]:
            continue
        
        # Check if this airline flies to the destination
        try:
            status = dest_row[col].iloc[0]
            print(f"  {col}: {status} (in delays: {col in airline_delays})")
            if status == FLIES and col in airline_delays:
                flying_airlines.append({
                    'name': col,
                    'delay': airline_delays[col],
                })
                print(f"    → Added {col} with delay {airline_delays[col]}")
        except Exception as e:
            print(f"    → Error checking {col}: {e}")
            continue
    
    print(f"Total flying airlines found: {len(flying_airlines)}")
    return flying_airlines

# Test the three countries
for country in ['UZBEKISTAN', 'MALTA', 'ARMENIA']:
    result = get_airlines_for_destination(country)
    if result:
        print(f"{country}: {len(result)} airlines")
    else:
        print(f"{country}: No airlines found!")