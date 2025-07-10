from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Custom Login User
USER = {'username': 'hassan', 'password': 'billa'}

# Load the trained model
model = joblib.load('model.pkl')

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER['username'] and password == USER['password']:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        try:
            # Collect 17 features from the form
            features = [float(request.form[f'feature{i}']) for i in range(1, 18)]
            prediction = model.predict([features])[0]
            result = 'Will Purchase' if prediction == 1 else 'Will Not Purchase'
            return render_template('result.html', result=result, features=features, prediction=prediction)
        except Exception as e:
            return f"Error processing input: {e}"
    return redirect(url_for('dashboard'))

@app.route('/visualization')
def visualization():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Example static data for charts (replace with your own stats if you want)
    chart_data = {
        'labels': ['Will Purchase', 'Will Not Purchase'],
        'values': [65, 35]
    }
    return render_template('visualization.html', chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
