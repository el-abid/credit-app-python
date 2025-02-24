from app import db, ClientData, app

# Push the app context to access the database
with app.app_context():
    # Delete all entries from the ClientData table
    db.session.query(ClientData).delete()
    db.session.commit()
    print("All data cleared from the database.")