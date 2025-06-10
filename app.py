from flask import Flask, request, render_template, jsonify, url_for, send_from_directory
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import StandardScaler
from src.components.pipeline.predict_pipeline import PredictPipeline, CustomData
from src.visualization import generate_charts

application = Flask(__name__, static_folder='static')

app = application

# Generate charts when the app starts
charts_info = None

# Initialize charts_info
charts_info = []

# Function to initialize charts
def initialize():
    global charts_info
    charts_info = generate_charts()
    
# Call initialize when the app starts
with app.app_context():
    initialize()

# Route for home page 
@app.route('/')
def index():
    return render_template('index.html', active_page='home')

# Route for prediction page
@app.route('/predict')
def predict():
    return render_template('predict.html', active_page='predict')

# Route for making predictions
@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'GET':
        return render_template('predict.html', active_page='predict')
    else:
        # Get data from form
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            writing_score=int(request.form.get('writing_score')),
            reading_score=int(request.form.get('reading_score'))
         )
        
        # Load model and preprocessor
        pred_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        predicted_score = predict_pipeline.predict(pred_data)
        predicted_score = np.round(predicted_score[0], 2)
        
        return render_template('predict.html', 
                               active_page='predict',
                               prediction=predicted_score,
                               prediction_text=f'Predicted Score: {predicted_score}',
                               gender=data.gender,
                               race_ethnicity=data.race_ethnicity,
                               parental_level_of_education=data.parental_level_of_education,
                               lunch=data.lunch,
                               test_preparation_course=data.test_preparation_course,
                               reading_score=data.reading_score,
                               writing_score=data.writing_score)

# Route for visualization page
@app.route('/visualize')
def visualize():
    global charts_info
    if charts_info is None:
        charts_info = generate_charts()
    return render_template('visualize.html', active_page='visualize', charts=charts_info)

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

# Route to handle the legacy home.html page for backward compatibility
@app.route('/home')
def home():
    return render_template('predict.html', active_page='predict')

# Serve static files explicitly if needed
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)