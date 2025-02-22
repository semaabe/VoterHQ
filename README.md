# SmartVote: Political Candidate Matchmaker

SmartVote is a web application designed to help users find political candidates who align with their preferences.  Users can filter candidates based on various criteria, such as political party, state, age, previous and current positions, college attended, and donation history to both Democrats and Republicans. The application utilizes a Tinder-style interface for candidate selection and integrates with Firebase for user data storage and authentication.  Similar user matching functionality is also included.


## Features

*   **Candidate Filtering:** Filter candidates based on party affiliation, state, age range, previous positions, current positions, college attended, and donation amounts to Democrats and Republicans.
*   **Tinder-Style Interface:** Browse candidates using a swipe-based interface, indicating "like" or "dislike" for each candidate.
*   **Final Match Display:** View a summary of liked candidates after completing the swiping process.
*   **Firebase Integration:** User data (preferences and matches) is securely stored and managed using Firebase Firestore.  Firebase Authentication is used for anonymous login, allowing the saving of user selections without requiring a user account.
*   **Similar User Matching:** After providing basic demographic information (age, gender, race, and state), the system finds users with similar profiles and displays their candidate matches.
*   **Dynamic Filtering:** Filter options update dynamically based on the user's current selections, ensuring relevant options are always available.

## Usage

1.  **Access the Application:** Visit [smartvote.com](smartvote.com).
2.  **Filter Candidates:** Use the provided filters on the index page to narrow down the candidate pool.
3.  **Swipe Through Matches:** On the match page, swipe left to dislike or right to like candidates.
4.  **View Final Matches:** After swiping, you'll see a list of your liked candidates.
5.  **Sign In (Optional):** Sign in anonymously to save your profile and view matches from users with similar demographics.

## Installation

This application is deployed on Vercel and does not require local installation.  To run locally, you will need:

*   Python 3.7+
*   `pip install -r requirements.txt` (you'll need to create a `requirements.txt` file listing the dependencies)
*   A Firebase project with Firestore enabled, and environment variables configured accordingly (see Configuration).
*   A `PoliticalData.csv` file in the same directory as `app.py` containing candidate data.

## Technologies Used

*   **Python:**  The backend is implemented using Python, leveraging Flask for the web framework.
*   **Flask:** A lightweight and flexible micro web framework for Python.  Handles routing, template rendering, and request processing.
*   **Pandas:** Used for data manipulation and analysis of the `PoliticalData.csv` file.
*   **NumPy:** Used for numerical operations, particularly handling NaN values in the candidate data.
*   **Firebase:**  Provides both authentication and database services (Firestore) for user data storage and management.
*   **HTML, CSS, JavaScript:** Used for frontend development.  Includes use of Swiper for the card swiping interface.
*   **Google Analytics:** Implemented via gtag.js for tracking user engagement.

## Statistical Analysis

The application performs basic data filtering based on user-specified criteria. No complex statistical analysis is currently implemented.  Data is loaded from a CSV file (`PoliticalData.csv`), cleaned to handle missing values (NaN replaced with None), and then filtered.

## Configuration

The application relies on environment variables for Firebase configuration.  These should be set using a `.env` file or your hosting provider's environment variable settings:

```
FIREBASE_TYPE=...
FIREBASE_PROJECT_ID=...
FIREBASE_PRIVATE_KEY_ID=...
FIREBASE_PRIVATE_KEY=...
FIREBASE_CLIENT_EMAIL=...
FIREBASE_CLIENT_ID=...
FIREBASE_AUTH_URI=...
FIREBASE_TOKEN_URI=...
FIREBASE_AUTH_PROVIDER_CERT_URL=...
FIREBASE_CLIENT_CERT_URL=...
FIREBASE_API_KEY=...
FIREBASE_AUTH_DOMAIN=...
FIREBASE_STORAGE_BUCKET=...
FIREBASE_MESSAGING_SENDER_ID=...
FIREBASE_APP_ID=...
FIREBASE_MEASUREMENT_ID=...
```

## API Documentation

The application primarily uses internal API calls between the frontend and backend.  The `/candidates`, `/update_options`, `/final_match`, `/store_user_data`, and `/similar_matches` routes handle requests from the frontend.  `/set_session_uid` handles the setting of a user ID in the session for anonymous users. Refer to the code for details of each route's functionality.  JSON is used for data exchange.

## Dependencies

*   Flask
*   pandas
*   numpy
*   firebase-admin
*   python-dotenv

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Testing

No dedicated testing framework is currently implemented.  Testing should be added to improve the robustness of the application.


*README.md was made with [Etchr](https://etchr.dev)*