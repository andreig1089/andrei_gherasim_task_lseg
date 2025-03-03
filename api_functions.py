from data_processing import *

def read_validate_preprocess(csv_file, consecutive_timestamps=CONSECUTIVE_TIMESTAMPS):
    """
    Reads, validates, and preprocesses data from a CSV file.
    Will select a random set of consecutive timestamps from the data.

    Args:
        csv_file (str): The path to the CSV file.
        consecutive_timestamps (int): The number of consecutive timestamps 
                                      to extract.

    Returns:
        list: The preprocessed data.
    """
    # read data from the csv file
    data = read_csv(csv_file)    
        
    # run validation tests
    validate_data(data, csv_file)
    
    if data:
        # preprocess the data
        data = preprocess_data(data)
        
        if len(data) < consecutive_timestamps:
            logging.warning(f"{csv_file}: Not enough data to process.")
            return data
            
        random_timestamp = random.randint(0, len(data) - consecutive_timestamps)
        
        data = data[random_timestamp : random_timestamp + consecutive_timestamps]
    else:
        return []
    
    return data

def predict(response, save_file=True):
    """
    Predicts the next 3 values based on the given response data.
    Returns the response data with the predicted values.

    Args:
        response (dict): The response data containing the ticker and its 
                         corresponding values.

    Returns:
        dict: The response data with the predicted values.
    """
    pred_response = dict()
    for (k, data) in response.items():
        data = list(map(preprocess_row, data))

        [ticker_str, last_date, _] = data[-1]

        pred_n1 = float(sorted(data, key=lambda v: v[2], reverse=True)[1][2])
        pred_n2 = (float(data[-1][2]) - float(pred_n1)) / 2
        pred_n3 = (pred_n1 - pred_n2) / 2

        data = data + [
            [ticker_str, last_date + timedelta(days=1), round(pred_n1, 2)],
            [ticker_str, last_date + timedelta(days=2), round(pred_n2, 2)],
            [ticker_str, last_date + timedelta(days=3), round(pred_n3, 2)],
        ]
        
        pred_response[k] = list(map(postprocess_row, data))
        
        if save_file:
            with open(f"{OUTPUT_DIR}/{k}.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
    return pred_response

def get_consecutive_data(n_files, n_consecutive):
    """
    Retrieves consecutive data from the specified number of CSV files.
    Uses the csv_files dictionary to select the files, defined in the
    data_processing module.

    Args:
        n_files (int): The number of CSV files to process.
        n_consecutive (int): The number of consecutive timestamps to extract.

    Returns:
        dict: The response data containing the ticker and its corresponding 
              values.
    """
    # first select the no of files
    csv_files_n = [x for v in csv_files.values() for x in v[:n_files]]
        
    response = dict()
    
    for csv_file in csv_files_n:
        data = read_validate_preprocess(csv_file, consecutive_timestamps=n_consecutive)
        
        data = list(map(postprocess_row, data))
        
        response["_".join(os.path.splitext(csv_file)[0].split("/")[-2:])] = data
        
    if not len(response):
        raise Exception('No data found in the csv files.')
    
    return response