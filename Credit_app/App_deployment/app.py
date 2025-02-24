import numpy as np
from flask import Flask, request, render_template
import pickle
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load the model
model = pickle.load(open('model.pkl', 'rb'))

# Define the ClientData model
class ClientData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_history = db.Column(db.Integer)
    married = db.Column(db.Integer)
    coapplicant_income = db.Column(db.Float)
    prediction = db.Column(db.String(10))

# Run this once to create the database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) if x.isdigit() else x for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = "Accepted" if prediction[0] == 1 else "Declined"

    # Save to database
    new_entry = ClientData(
        credit_history=int_features[0],
        married=int_features[1],
        coapplicant_income=int_features[2],
        prediction=output
    )
    db.session.add(new_entry)
    db.session.commit()

    return render_template('index.html', prediction_text=f'The response to your request is: {output}')

@app.route('/view_data')
def view_data():
    clients = ClientData.query.all()  # Retrieve all entries from ClientData table
    return render_template('view_data.html', clients=clients)

if __name__ == "__main__":
    app.run(debug=True)


