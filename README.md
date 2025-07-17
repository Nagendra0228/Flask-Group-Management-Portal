# Flask Group Management Portal

This project is a unique web-based management system built with Flask and Microsoft SQL Server. It empowers organizations to efficiently manage groups, members, savings, loans, and Suraksha records through a secure and user-friendly web interface.

## Features

- User authentication for secure access
- Add/view groups and members
- Manage savings and loans
- Suraksha record management
- SQL Server backend integration

## Technologies Used

- Python 3.x
- Flask
- pyodbc (SQL Server connectivity)
- HTML/CSS (Jinja2 templates)
- Microsoft SQL Server

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Nagendra0228/Flask-Group-Management-Portal.git
   cd dbms
   ```

2. **Install dependencies:**
   ```bash
   pip install flask pyodbc
   ```

3. **Configure database:**
   - Edit `db_config.py` and set your SQL Server connection string.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the app:**
   - Open your browser and go to `http://localhost:5000`

## Project Structure

```
dbms/
│
├── app.py               # Main Flask application
├── db_config.py         # Database connection string
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── README.md            # Project documentation
└── .gitignore           # Git ignore file
```

## Security Notes

- Change `app.secret_key` in `app.py` to a strong, random value before deploying.
- Ensure your database credentials are kept secure.

## License

This project is licensed under the MIT License.
