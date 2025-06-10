from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.preprocessing import StandardScaler
from src.components.pipeline.predict_pipeline import PredictPipeline, CustomData

# Import the prediction pipeline (if needed)
# from src.components.pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)

app = application


## Route for home page 
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'GET':
        return render_template('home.html')
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
        
        return render_template('home.html', 
                               prediction=predicted_score,
                               prediction_text=f'Predicted Score: {predicted_score}',
                               gender=data.gender,
                               race_ethnicity=data.race_ethnicity,
                               parental_level_of_education=data.parental_level_of_education,
                               lunch=data.lunch,
                               test_preparation_course=data.test_preparation_course,
                               reading_score=data.reading_score,
                               writing_score=data.writing_score)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)