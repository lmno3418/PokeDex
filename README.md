# Pokedex Application with Authentication and Battle Prediction

A comprehensive Pokedex web application with user authentication and Pokemon battle prediction, built using Flask.

## Features

- User authentication (register, login, logout)
- Protected Pokedex access (only for authenticated users)
- Comprehensive Pokemon database with detailed information
- Advanced filtering and search capabilities
- Pokemon battle prediction using machine learning
- Responsive design for all devices

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables (see `.env-example`):
   ```
   SECRET_KEY=your_secure_secret_key_here
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

### Setting up Supabase

1. Create a Supabase account at [supabase.com](https://supabase.com)
2. Create a new project 
3. Create a table called `users` with the following columns:
   - `id` (uuid, primary key)
   - `username` (text, not null)
   - `email` (text, not null, unique)
   - `password` (text, not null)
4. Copy your Supabase URL and API key to your `.env` file

### Running the Application

Run the application with:
```
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
pokedex2/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                   # Example environment variables
├── static/                # Static assets
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript files
│   └── data/
│       ├── pokemon_RandomForest_model.pkl/           # Random Forest Model
│       └── PokemonData2.json/                        # Pokemon,Img,Animation Data in json
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── home.html          # Home page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── about.html         # About page
    └── pokedex.html       # Pokedex page (protected)
```

## Battle Prediction

The application uses a machine learning model (Random Forest) to predict battle outcomes between two Pokemon. The model takes into account:

- Pokemon types (primary and secondary)
- Stats (HP, Attack, Defense, etc.)
- Height and weight
- Base experience
- Generation
- Legendary status

## Technologies Used

- **Backend**: Python Flask
- **Database**: Supabase
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Styling**: Bootstrap, Custom CSS
- **Machine Learning**: Scikit-learn, NumPy

## License

This project is for educational purposes only. 