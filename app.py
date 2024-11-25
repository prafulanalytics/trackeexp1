from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
import json
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='textures')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024 * 1024 
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file part"}), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return jsonify({"message": "File uploaded successfully", "file_path": file.filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_data', methods=['POST'])
def upload_data():
    try:
        if 'data' not in request.files:
            return jsonify({"error": "No data file part"}), 400

        file = request.files['data']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the data file
            df = pd.read_csv(file_path)
            if 'timestamp' not in df.columns:
                return jsonify({"error": "No timestamp column in data file"}), 400

            # Convert the timestamp to seconds if necessary
            if pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp']).view('int64') // 10**9

            # Convert the DataFrame to a list of dictionaries
            data_points = df.to_dict(orient='records')
            columns = df.columns.tolist()
            return jsonify({"message": "Data uploaded successfully", "data": data_points, "columns": columns}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_data2', methods=['POST'])
def upload_data2():
    try:
        if 'data' not in request.files:
            return jsonify({"error": "No data file part"}), 400

        file = request.files['data']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the data file
            df = pd.read_csv(file_path)
            if 'timestamp' not in df.columns:
                return jsonify({"error": "No timestamp column in data file"}), 400

            # Convert the timestamp to seconds if necessary
            if pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp']).view('int64') // 10**9

            # Convert the DataFrame to a list of dictionaries
            data_points = df.to_dict(orient='records')
            columns = df.columns.tolist()
            return jsonify({"message": "Data uploaded successfully", "data": data_points, "columns": columns}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_home_data', methods=['POST'])
def upload_home_data():
    try:
        if 'homeData' not in request.files:
            return jsonify({"error": "No data file part"}), 400

        file = request.files['homeData']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the data file
            df = pd.read_csv(file_path)
            if 'timestamp' not in df.columns:
                return jsonify({"error": "No timestamp column in data file"}), 400

            # Log the content of the 'data' column before parsing
            for index, row in df.iterrows():
                print(f"Row {index} data: {row['data']}")

            # Parse the JSON string in 'data' column
            try:
                df['data'] = df['data'].apply(lambda x: json.loads(x.replace("'", '"')))
            except json.JSONDecodeError as e:
                return jsonify({"error": f"JSON parsing error: {str(e)}"}), 400

            # Convert the DataFrame to a list of dictionaries
            data_points = df.to_dict(orient='records')
            return jsonify({"message": "Data uploaded successfully", "data": data_points}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_away_data', methods=['POST'])
def upload_away_data():
    try:
        if 'awayData' not in request.files:
            return jsonify({"error": "No data file part"}), 400

        file = request.files['awayData']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process the data file
            df = pd.read_csv(file_path)
            if 'timestamp' not in df.columns:
                return jsonify({"error": "No timestamp column in data file"}), 400

            # Log the content of the 'data' column before parsing
            for index, row in df.iterrows():
                print(f"Row {index} data: {row['data']}")

            # Parse the JSON string in 'data' column
            try:
                df['data'] = df['data'].apply(lambda x: json.loads(x.replace("'", '"')))
            except json.JSONDecodeError as e:
                return jsonify({"error": f"JSON parsing error: {str(e)}"}), 400

            # Convert the DataFrame to a list of dictionaries
            data_points = df.to_dict(orient='records')
            return jsonify({"message": "Data uploaded successfully", "data": data_points}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload_skeleton_data', methods=['POST'])
def upload_skeleton_data():
    try:
        if 'skeletonData' not in request.files:
            return jsonify({"error": "No skeleton data file part"}), 400

        file = request.files['skeletonData']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Read and process the file content
            try:
                with open(file_path, 'r') as f:
                    skeleton_data = json.load(f)
            except json.JSONDecodeError as e:
                return jsonify({"error": f"JSON decoding error: {str(e)}"}), 400

            # Check the structure of the loaded JSON data
            if not isinstance(skeleton_data, dict):
                return jsonify({"error": "Invalid skeleton data format"}), 400

            # Log the first few keys of the skeleton data for debugging
            sample_keys = list(skeleton_data.keys())[:5]
            print(f"Skeleton Data Sample Keys: {sample_keys}")

            return jsonify({"message": "Skeleton data uploaded successfully", "data": skeleton_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/timestamp', methods=['POST'])
def receive_timestamp():
    try:
        data = request.json
        timestamp = data.get('timestamp')
        if timestamp is None:
            return jsonify({'status': 'error', 'message': 'No timestamp provided'}), 400

        return jsonify({'status': 'success', 'timestamp': timestamp}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host ='0.0.0.0',debug=True, port=port)
