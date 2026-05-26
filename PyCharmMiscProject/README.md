# SQL Query Executor with Dark Mode

This is a simple web application that provides a user interface for executing SQL queries against a database through a Flask API.

## Features

- Execute SQL queries against a database
- Dark mode toggle with persistent settings
- Responsive design

## Files

- `app.py`: Flask backend API
- `index.html`: Main HTML interface
- `styles.css`: Styling with dark mode support
- `script.js`: Frontend JavaScript functionality

## Dark Mode Implementation

The dark mode feature includes:

1. A toggle button in the top-right corner
2. CSS styles for both light and dark modes
3. LocalStorage persistence for user preferences
4. Smooth transitions between modes

## Setup

1. Install required packages:
   ```
   pip install flask pymysql
   ```

2. Start the Flask server:
   ```
   python app.py
   ```

3. Open `index.html` in a web browser

## API Endpoints

- `POST /execute_sql`: Execute a SQL query
  - Parameters:
    - `sql_query`: The SQL query to execute
    - `connection_info`: Database connection information (host, port, user, password, database)

## License

MIT