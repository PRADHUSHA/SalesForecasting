from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
import os
from werkzeug.utils import secure_filename
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

app = Flask(__name__)
cors = CORS(app)
# Load data
data = pd.read_csv('data_sales.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

#First five rows
data.head()

#Last five rows
data.tail()

#Shape
data.shape

#Description
data.describe()

#Preprocessing step
data.isnull().sum()

#Declaring X and Y

X = data[['Y', 'M','pid']]
y = data['Sales']

# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the random forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model on the training data
model.fit(X_train, y_train)

# Predict the sales for the testing data
y_pred = model.predict(X_test)

# Evaluate the model performance
mse = mean_absolute_error(y_test, y_pred)
print("Mean Absolute Error:", mse)


# FORM DATA
@app.route('/form', methods=['POST'])
def hforms():
    year = request.json['year']
    month = request.json['month']
    pid = request.json['pid']
    data = [int(pid),int(year),int(month)]
    int_f = [np.array(data)]
    pred = model.predict(int_f)
    return jsonify(pred.tolist())

# CONNECTIVITY CODE

app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENTIONS = {'txt','xls','csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS 

@app.route('/upload', methods=['POST'])
def file_upload():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file included in request.'}),400

    file = request.files['file']

    if file.filename =='':
        return jsonify({'error': 'no file is selected.'}),400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message ': 'File uploaded successfully'}),200

    else:
        return jsonify({'error':'Invalid file format'}),400

if __name__ == '__main__':
    app.run(debug=True)