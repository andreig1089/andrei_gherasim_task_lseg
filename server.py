from flask import Flask, jsonify, request
from flask import logging as flasklogging
import logging
import api_functions
from datetime import datetime, timedelta

import os

app = Flask(__name__)
ENDPOINT_ROOT = "api"
API_VERSION = "1"
APPLICATION_ROOT = f"/{ENDPOINT_ROOT}/{API_VERSION}"
LOGGING_FORMAT = (
    '%(asctime)s [%(levelname)s | %(filename)s: line %(lineno)s]: %(message)s'
)

flasklogging.default_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

@app.route(f'{APPLICATION_ROOT}/consecutive_points', methods=['GET'])
def consecutive_points():
    """
    Endpoint to get the last n consecutive data points from the given CSV files.

    Params:
        description (str): If "True", returns the description of the endpoint.
        n_files (int): The number of files to process.
        n_consecutive (int): The number of consecutive timestamps to extract.

    Returns:
        JSON: The response data containing the ticker and its corresponding 
              values or an error message.
    """
    arguments = request.args
    
    description = arguments.get('description')
    print(description)
    
    if description == "True":
        return jsonify({
            'description': 'This endpoint returns the last n consecutive data '
                           'points from the given CSV files.'
        }), 200
    
    if not arguments:
        return jsonify({'error': 'Please provide the number of files to process.'}), 400
    
    n_files = arguments.get('n_files')
        
    try:
        n_files = int(n_files)
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': 'The number of files is not a numeric value.'}), 400
    
    if int(n_files) > 2:
        return jsonify({
            'error': 'the max value of n_files is 2'
        }), 400
    
    n_consecutive = arguments.get('n_consecutive', api_functions.CONSECUTIVE_TIMESTAMPS)
    n_consecutive = int(n_consecutive)
   
    try:
        response = api_functions.get_consecutive_data(n_files, n_consecutive)
        
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': e}), 400
    return jsonify(response)


@app.route(f'{APPLICATION_ROOT}/consecutive_points_predict', methods=['GET'])
def predict():
    """
    Endpoint to predict the next 3 values based on the given response data.

    params:
        description (str): If "True", returns the description of the endpoint.
        n_files (int): The number of files to process.

    Returns:
        JSON: The response data with the predicted values or an error message.
    """
    arguments = request.args
    description = arguments.get('description')
    
    if description == "True":
        return jsonify({
            'description': 'This endpoint returns the prediction of 3 values, '
                           'at the end of a random sample of 10 consecutive '
                           'records for the given CSV files.'
        }), 200
    
    n_files = arguments.get('n_files')
                
    with app.test_client() as client:
        # attempt to get the response from the other endpoint
        try:
            response = client.get(
                f"{APPLICATION_ROOT}/consecutive_points", 
                query_string={"n_files": n_files}
            )
            
            if response.status_code != 200:
                return jsonify(response.json), 400
            else:            
                response = response.json
                
            # remove old files from outputs directory
            _ = [os.remove(p.path) 
                for p in os.scandir(api_functions.OUTPUT_DIR) 
                if os.path.splitext(p.name)[1] == '.csv']
        except Exception as e:
            app.logger.error(e)
            return jsonify({'error': e}), 400
        
        try:
            pred_response = api_functions.predict(response)
        except Exception as e:
            app.logger.error(e)
            return jsonify({'error': e}), 400
        
        return jsonify(pred_response)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=5000,
        debug=True
    )
