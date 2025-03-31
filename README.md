# MADI-cs2003

This project was made as part of the **Diploma in Programming** course at **IIT Madras**.

## Project Overview
The **MADI-cs2003** project aims to provide a solution for household service management using a web application. This application is built using **Python** and **Flask**, designed to provide easy access to household service requests and management.

## Features
- **Service Request**: Users can request various household services.
- **Admin Panel**: Admins can manage the service requests.
- **Database Integration**: The app uses a database for storing service requests and user information.

## Technologies Used
- **Python**: Programming language used for backend development.
- **Flask**: Web framework for building the web application.
- **HTML/CSS**: Used for designing the frontend of the application.
- **JavaScript**: For client-side functionality.

## Installation

### Prerequisites
Before running the application, ensure that you have the following installed:
- **Python 3.x**: Install Python from [python.org](https://www.python.org/downloads/)
- **pip**: Python package installer. It comes with Python by default.

### Steps to Run the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/21f1000601/MADI-cs2003.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd MADI-cs2003
   ```

3. **Install required dependencies**:
   Use the `requirements.txt` file to install necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   Run the following command to set up the database:
   ```bash
   python create_db.py
   ```

5. **Run the application**:
   Start the Flask application by running:
   ```bash
   python app.py
   ```

6. **Open the app in your browser**:
   Once the app is running, open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Directory Structure
- `static/`: Contains the static files (CSS, images, etc.).
- `templates/`: Contains HTML files for rendering the web pages.
- `app.py`: Main Python file where the Flask application runs.
- `create_db.py`: Script to create the required database.
- `check_db.py`: Script to check the database connection.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
