from flask import Flask, jsonify, render_template, request,session,redirect, url_for, session
import pandas as pd
import numpy as np  # Import numpy to handle NaN values
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = b'\x16T\xbet\x08\xae\x13y\xea\x04\xc8\xbc\xe3\xd4\x81\x0b\x15R\xaeT\xcb\x07\x07\xea'
# Define the file path at the start
load_dotenv()
# Load the JSON from an environment variable
cred = credentials.Certificate({
    "type": os.environ["FIREBASE_TYPE"],
    "project_id": os.environ["FIREBASE_PROJECT_ID"],
    "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace('\\n', '\n'),
    "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
    "client_id": os.environ["FIREBASE_CLIENT_ID"],
    "auth_uri": os.environ["FIREBASE_AUTH_URI"],
    "token_uri": os.environ["FIREBASE_TOKEN_URI"],
    "auth_provider_x509_cert_url": os.environ["FIREBASE_AUTH_PROVIDER_CERT_URL"],
    "client_x509_cert_url": os.environ["FIREBASE_CLIENT_CERT_URL"]
})
firebase_admin.initialize_app(cred)

db = firestore.client()

FIREBASE_CONFIG = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}
file_path = 'PoliticalData.csv'

def load_candidates(file_path):
    """Loads candidates data from an Excel file."""
    try:
        df = pd.read_csv(file_path)
        df["To Democrats"] = pd.to_numeric(df["To Democrats"], errors='coerce').fillna(0)
        df["To Republicans"] = pd.to_numeric(df["To Republicans"], errors='coerce').fillna(0)

        # Replace NaN values with None or another JSON-compatible value
        df = df.replace({np.nan: None})

        return df
    except Exception as e:
        print(f"Error loading candidates: {e}")
        return None
    


@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/get-started')
def get_started():
    return redirect(url_for('index'))

@app.route('/candidates', methods=['GET'])
def match():
    candidates_df = load_candidates(file_path)
    
    if candidates_df is None:
        return jsonify({"error": "Failed to load candidates data"}), 500
    
    donated_democrats = request.args.get('donated_democrats', 0)
    donated_republicans = request.args.get('donated_republicans', 0)
    
    # Store donation information in the session
    session['donated_democrats'] = donated_democrats
    session['donated_republicans'] = donated_republicans

    # Get filter parameters from request
    selected_party = request.args.get('party')
    selected_state = request.args.get('state')
    min_age = request.args.get('min_age')
    max_age = request.args.get('max_age')
    former_position = request.args.get('former_position')
    current_position = request.args.get("current_position")
    selected_college = request.args.get("college")
    donated_democrats = request.args.get('donated_democrats')
    donated_republicans = request.args.get('donated_republicans')
    
    # Filter based on selected criteria
    if selected_party:
        candidates_df = candidates_df[candidates_df['Political Party'] == selected_party]
    if selected_state and selected_state != "Don't Care":
        candidates_df = candidates_df[candidates_df['State'] == selected_state]
    if min_age and max_age:
        candidates_df = candidates_df[(candidates_df['Age'] >= int(min_age)) & (candidates_df['Age'] <= int(max_age))]
    if former_position:
        candidates_df = candidates_df[candidates_df['Former'] == former_position]
    if current_position:
        candidates_df = candidates_df[candidates_df['Current'] == current_position]
    if selected_college:
        candidates_df = candidates_df[candidates_df['College'] == selected_college]
   
    # Convert to dictionary
    available_positions = candidates_df['Current'].dropna().unique().tolist()
    
    candidates = candidates_df.to_dict(orient='records')
    return render_template('match.html', candidates=candidates if candidates else [], available_positions=available_positions)

@app.route('/update_options', methods=['GET'])
def update_options_route():
    candidates_df = load_candidates(file_path)
    
    if candidates_df is None:
        return jsonify({"error": "Failed to load candidates data"}), 500

    # Get the current filter selections from the request
    selected_party = request.args.get('party')
    selected_state = request.args.get('state')
    min_age = request.args.get('min_age')
    max_age = request.args.get('max_age')
    selected_former_position = request.args.get('former_position')
    selected_current_position = request.args.get('current_position')
    selected_college = request.args.get('college')

    donated_democrats = request.args.get('donated_democrats')
    donated_republicans = request.args.get('donated_republicans')

    # Filter candidates based on current selections
    if selected_party:
        candidates_df = candidates_df[candidates_df['Political Party'] == selected_party]
    if selected_state:
        candidates_df = candidates_df[candidates_df['State'] == selected_state]
    if min_age and max_age:
        candidates_df = candidates_df[(candidates_df['Age'] >= int(min_age)) & (candidates_df['Age'] <= int(max_age))]
    if selected_former_position:
        candidates_df = candidates_df[candidates_df['Former'] == selected_former_position]
    if selected_current_position:
        candidates_df = candidates_df[candidates_df['Current'] == selected_current_position]
    if selected_college:
        candidates_df = candidates_df[candidates_df['College'] == selected_college]

    # Get the available options for former_position, current_position, and college
    available_colleges = candidates_df['College'].dropna().unique().tolist()
    available_formers = candidates_df['Former'].dropna().unique().tolist()
    available_positions = candidates_df['Current'].dropna().unique().tolist()

    # Return the filtered options as JSON
    return jsonify({
        "available_colleges": available_colleges,
        "available_formers": available_formers,
        "available_positions": available_positions
    })


# Ensure the existing update_options function is defined
def filter_candidates(candidates, selected_party=None, selected_state=None, selected_college=None, selected_former=None, selected_position=None):
    """Filters the candidates based on the provided criteria."""
    if selected_party:
        candidates = candidates[candidates['Political Party'] == selected_party]
    if selected_state:
        candidates = candidates[candidates['State'] == selected_state]
    if selected_college:
        candidates = candidates[candidates['College'] == selected_college]
    if selected_former:
        candidates = candidates[candidates['Former'] == selected_former]
    if selected_position:
        candidates = candidates[candidates['Position'] == selected_position]
    
    return candidates

def get_unique_values(candidates, column_name):
    """Returns the unique values for a given column."""
    return candidates[column_name].dropna().unique().tolist()



@app.route('/final_match', methods=['GET'])
def final_match():
    # Retrieve liked candidates from the query parameters
    liked_candidates_json = request.args.get('liked_candidates')
    donated_democrats = request.args.get('donated_democrats', 0)
    donated_republicans = request.args.get('donated_republicans', 0)

    if liked_candidates_json:
        liked_candidates = json.loads(liked_candidates_json)  # Parse the JSON string to Python list
    else:
        liked_candidates = []

    # Firebase configuration (assuming you've loaded it via dotenv)
    FIREBASE_CONFIG = {
        'apiKey': os.getenv('FIREBASE_API_KEY'),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.getenv('FIREBASE_PROJECT_ID'),
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.getenv('FIREBASE_APP_ID'),
        'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
    }

    # Render the final matches page with the liked candidates and firebase config
    return render_template(
        'final_match.html',
        liked_candidates=json.loads(liked_candidates_json) if liked_candidates_json else [],
        donated_democrats=donated_democrats,
        donated_republicans=donated_republicans,
        firebase_config=FIREBASE_CONFIG
    )


# firebase_admin.initialize_app(cred)



@app.route('/store_user_data', methods=['POST'])
def store_user_data():
    user_data = request.get_json()
    uid = user_data['uid']  # UID from Firebase Auth
    age = user_data['age']
    gender = user_data['gender']
    race = user_data['race']
    state = user_data['state']
    final_match = user_data['final_match']

    # Retrieve donation information from session (from filter page)
    donated_democrats = session.get('donated_democrats', 0)
    donated_republicans = session.get('donated_republicans', 0)

    doc_ref = db.collection('users').document(uid)
    doc_ref.set({
        'age': age,
        'gender': gender,
        'race': race,
        'state': state,
        'final_match': final_match,
        'donated_democrats': donated_democrats,  # Store donation information
        'donated_republicans': donated_republicans  # Store donation information
    })
    
    return jsonify({"status": "success"})


@app.route('/similar_matches')
def similar_matches():
    uid = session.get('uid')

    if not uid:
        return redirect(url_for('index'))

    try:
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        # Check if user_doc exists
        if not user_doc.exists:
            print(f"User document not found for UID: {uid}")
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()
    except Exception as e:
        print("Error fetching user data:", e)
        return jsonify({"error": "Failed to retrieve user data"}), 500

    # Debug user_data
    print(f"User data retrieved: {user_data}")

    # Query for similar users using keyword arguments
    query_ref = db.collection('users') \
        .where(field_path='race', op_string='==',value=user_data.get('race')) \
        .where(field_path='state', op_string='==', value=user_data.get('state')) \
        .where(field_path='college', op_string='==', value=user_data.get('college'))

    similar_users = query_ref.stream()

    similar_matches = []
    for user in similar_users:
        similar_data = user.to_dict()
        matches = similar_data.get('final_match', [])  # Ensure this is a list
        similar_matches.append({
            'age': similar_data['age'],
            'gender': similar_data['gender'],
            'race': similar_data['race'],
            'state': similar_data['state'],
            'matches': matches  # Store matches here
        })

    # Firebase configuration (assuming you've loaded it via dotenv)
    FIREBASE_CONFIG = {
        'apiKey': os.getenv('FIREBASE_API_KEY'),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.getenv('FIREBASE_PROJECT_ID'),
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.getenv('FIREBASE_APP_ID'),
        'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
    }

    print(f"Similar matches found: {similar_matches}")
    return render_template(
        'similar_matches.html',
        matches=similar_matches,
        firebase_config=FIREBASE_CONFIG
    )

@app.route('/set_session_uid', methods=['POST'])
def set_session_uid():
    data = request.get_json()
    uid = data.get('uid')

    if uid:
        session['uid'] = uid
        return jsonify({"status": "UID stored in session"}), 200
    else:
        return jsonify({"error": "UID not provided"}), 400


if __name__ == "__main__":
    app.run(debug=True)
