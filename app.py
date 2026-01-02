"""
Airline Recommendation System - Flask Backend API
Provides endpoints for destination listing and airline recommendations
"""

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Configuration
EXCEL_FILE = 'data_set_for_AI.xlsx'
LOGO_FOLDER = 'static/logos'

# Column names from the Excel file (Hebrew)
# Note: We strip column names on load to handle whitespace issues
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


# Load data once at startup
df = load_data()



def get_logo_path(airline_name):
    """Find the logo file for an airline, checking multiple extensions"""
    logo_dir = os.path.join(os.path.dirname(__file__), LOGO_FOLDER)
    # Replace spaces with underscores for filename lookup
    safe_name = airline_name.replace(' ', '_')
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
        filename = f"{safe_name}{ext}"
        if os.path.exists(os.path.join(logo_dir, filename)):
            return f'/static/logos/{filename}'
    # Return default placeholder if no logo found
    return f'/static/logos/{safe_name}.png'


def get_airline_delays():
    """Extract airline delay data as a dictionary"""
    delays = {}
    for _, row in df.iterrows():
        airline = row[COL_AIRLINES]
        delay = row[COL_DELAYS]
        if pd.notna(airline) and pd.notna(delay):
            delays[airline] = float(delay)
    return delays


def get_airlines_for_destination(destination):
    """
    Get airlines that fly to a specific destination,
    sorted by average delay (lowest first)
    """
    # Find the row for this destination
    dest_row = df[df[COL_DESTINATIONS] == destination]
    
    if dest_row.empty:
        return None
    
    # Get all airline columns (excluding the first 3 metadata columns)
    airline_delays = get_airline_delays()
    
    # Find airlines that fly to this destination
    flying_airlines = []
    
    for col in df.columns:
        # Skip non-airline columns
        if col in [COL_AIRLINES, COL_DELAYS, COL_DESTINATIONS]:
            continue
        
        # Check if this airline flies to the destination
        try:
            status = dest_row[col].iloc[0]
            if status == FLIES and col in airline_delays:
                flying_airlines.append({
                    'name': col,
                    'delay': airline_delays[col],
                    'logo': get_logo_path(col)
                })
        except:
            continue
    
    # Sort by delay (ascending)
    flying_airlines.sort(key=lambda x: x['delay'])
    
    return flying_airlines


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/destinations')
def get_destinations():
    """Get list of all available destinations that have airline data"""
    all_destinations = df[COL_DESTINATIONS].dropna().unique().tolist()
    
    # Filter to only include destinations with at least one airline with delay data
    valid_destinations = []
    for dest in all_destinations:
        airlines = get_airlines_for_destination(dest)
        if airlines and len(airlines) > 0:
            valid_destinations.append(dest)
    
    return jsonify({
        'success': True,
        'destinations': valid_destinations
    })


from urllib.parse import unquote

@app.route('/api/recommend/<destination>')
def get_recommendations(destination):
    """Get top 3 airlines with lowest delays for a destination"""
    destination = unquote(destination)
    airlines = get_airlines_for_destination(destination)
    
    if airlines is None:
        return jsonify({
            'success': False,
            'error': f"Destination '{destination}' not found"
        }), 404
    
    if len(airlines) == 0:
        return jsonify({
            'success': False,
            'error': f"No airlines with delay data fly to '{destination}'"
        }), 404
    
    # Get top 3 (or fewer if not enough airlines)
    top_3 = airlines[:3]
    
    return jsonify({
        'success': True,
        'destination': destination,
        'airlines': top_3,
        'total_available': len(airlines),
        'message': generate_message(destination, len(airlines), len(top_3))
    })


def generate_message(destination, total, shown):
    """Generate recommendation message"""
    if shown < 3:
        return (f"עבור היעד '{destination}', נמצאו {total} חברות תעופה עם נתוני עיכובים. "
                "אנו ממליצים לבדוק מידע נוסף לפני קבלת החלטה סופית.")
    else:
        return (f"עבור היעד '{destination}', אלו הן 3 חברות התעופה עם ממוצע העיכובים הנמוך ביותר. "
                "ממוצע עיכובים נמוך יותר מצביע על סבירות גבוהה יותר לטיסה בזמן.")


@app.route('/static/logos/<filename>')
def serve_logo(filename):
    """Serve airline logo files"""
    logo_path = os.path.join(os.path.dirname(__file__), LOGO_FOLDER)
    return send_from_directory(logo_path, filename)


if __name__ == '__main__':
    # Create logos directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), LOGO_FOLDER), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
