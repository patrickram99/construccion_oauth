from app import create_app
from db.schema import create_tables

if __name__ == "__main__":
    # Create database tables if they don't exist
    create_tables()
    
    # Create and run the Flask app
    app = create_app()
    app.run(debug=True)