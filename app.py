from flask import Flask, jsonify, render_template, request,session,redirect, url_for, session
import pandas as pd
import numpy as np  # Import numpy to handle NaN values
import json
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = b'\x16T\xbet\x08\xae\x13y\xea\x04\xc8\xbc\xe3\xd4\x81\x0b\x15R\xaeT\xcb\x07\x07\xea'
# Define the file path at the start

file_path = 'Political Data.xlsx'

def load_candidates(file_path):
    """Loads candidates data from an Excel file."""
    try:
        df = pd.read_excel(file_path)
        df["To Democrats"] = pd.to_numeric(df["To Democrats"], errors='coerce').fillna(0)
        df["To Republicans"] = pd.to_numeric(df["To Republicans"], errors='coerce').fillna(0)

        # Replace NaN values with None or another JSON-compatible value
        df = df.replace({np.nan: None})

        return df
    except Exception as e:
        print(f"Error loading candidates: {e}")
        return None
    


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/candidates', methods=['GET'])
def match():
    candidates_df = load_candidates(file_path)
    
    if candidates_df is None:
        return jsonify({"error": "Failed to load candidates data"}), 500



    # Get filter parameters from request
    selected_party = request.args.get('party')
    selected_state = request.args.get('state')
    min_age = request.args.get('min_age')
    max_age = request.args.get('max_age')
    former_position = request.args.get('former_position')
    current_position = request.args.get("current_position")
    selected_college = request.args.get("college")
    
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
    
    if liked_candidates_json:
        liked_candidates = json.loads(liked_candidates_json)  # Parse the JSON string to Python list
    else:
        liked_candidates = []

    # Render the final matches page with the liked candidates
    return render_template('final_match.html', liked_candidates=liked_candidates)



if __name__ == "__main__":
    app.run(debug=True)
