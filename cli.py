import argparse
import os
import requests

STOCK_PRICE_DATA_FILES = 'stock_price_data_files'
DEFAULT_SERVER_ADDRESS = 'http://127.0.0.1:5000'

available_choices = {i.name: i.path for i in os.scandir(STOCK_PRICE_DATA_FILES) 
                     if os.path.isdir(i.path)}

def get_subchoices(ticker):
    """
    Retrieves the subchoices for a given ticker.

    Args:
        ticker (str): The ticker to get subchoices for.

    Returns:
        dict: A dictionary of subchoices with their names and paths.
    """
    if ticker in available_choices:
        return {str(_idx): (i.name, i.path) for (_idx, i) in enumerate(
            os.scandir(os.path.join(STOCK_PRICE_DATA_FILES, ticker))) 
                if os.path.isfile(i.path)}
    else:
        return None

def get_api_response(endpoint_address):
    """
    Retrieves the API response from the server.
    """
    response = requests.get(endpoint_address).text
        
    print(response)
    
    save_file = input(
        "Save json result to file? (enter path, default: no): "
    ).strip()
    
    return response, save_file

def menu():
    """
    Displays the menu and handles user input.
    """
    choices = {
        '1': ('Get the 10 consecutive values.', None),
        '2': ('Predict the next 3 values.', None),        
    }
    choices['d'] = ('describe', lambda: print("Description:"))
    choices['q'] = ('quit', lambda: print("You'll now quit, so long!"))
    
    server_address = input(
        f"Enter server:port address (by default {DEFAULT_SERVER_ADDRESS}): "
    ).strip()
    if not server_address:
        server_address = f'{DEFAULT_SERVER_ADDRESS}'   
         
    while True:
        print("\nSelect an option:")
        for key, (desc, _) in choices.items():
            print(f"{key}. {desc}")

        choice = input("Enter your choice: ").strip()
        
        if choice in choices:
            save_file = None
            if choice == "q":
                break
            elif choice == "d":
                print(1, choices['1'][0], requests.get(f'{server_address}/api/1/consecutive_points?description=True').text)
                print(2, choices['2'][0], requests.get(f'{server_address}/api/1/consecutive_points_predict?description=True').text)
            elif choice == '1':
                n_files = input("Enter the no of files to export: ").strip()
                response, save_file = get_api_response(
                    f'{server_address}/api/1/consecutive_points?n_files={n_files}')
            elif choice == '2':
                n_files = input("Enter the no of files to export: ").strip()
                response, save_file = get_api_response(
                    f'{server_address}/api/1/consecutive_points_predict?n_files={n_files}')
                
            if save_file and save_file.lower() != 'no':
                try:
                    with open(save_file, 'w') as f:
                        f.write(response)
                    print(f'File saved at: {save_file}')
                except Exception as e:
                    print(f'Cannot save the file: {e}')
        else:
            print("Invalid choice! Try again.")

def main():
    """
    The main function that parses arguments and shows the menu.
    """
    parser = argparse.ArgumentParser(description="CLI Menu Example")
    subparsers = parser.add_subparsers(dest="command")

    args = parser.parse_args()

    if not args.command:  # If no argument is provided, show the menu
        menu()
    else:
        print(
            'invalid usage, command does not take any argument, please use the menu'
        )

if __name__ == "__main__":
    main()
