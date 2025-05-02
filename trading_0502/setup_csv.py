import os
import csv

# Create the directory structure if it doesn't exist
def setup_csv_file():
    """
    # Create directories if they don't exist
    os.makedirs(os.path.join('_static', 'global'), exist_ok=True)
    
    # CSV file path
    csv_path = os.path.join('_static', 'global', 'player_parameters.csv')
    
    # Sample data from your requirements (list of dictionaries)
    # (data is already defined above)
    
    # Write data to CSV file
    with open(csv_path, 'w', newline='') as file:
        # Define the fieldnames from the first row
        fieldnames = data[0].keys()
        
        # Create CSV writer
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        writer.writerows(data)
    
    print(f"CSV file created successfully at: {csv_path}")
    print(f"Added data for {len(data)} students")


if __name__ == "__main__":
    setup_csv_file()
    Setup the CSV file with player parameters in the correct location for oTree
    
    This script should be run from the oTree project root directory.
    It will create the _static/global directory if it doesn't exist and
    create the player_parameters.csv file with the sample data.
    """
    # Create directories if they don't exist
    os.makedirs(os.path.join('_static', 'global'), exist_ok=True)
    
    # CSV file path
    csv_path = os.path.join('_static', 'global', 'player_parameters.csv')
    
    # Sample data from your requirements
    data = [
        {'student_id': '1', 'utility_type': 'CD', 'alpha': '0.29', 'beta': '0.48', 'endowment_a': '5', 'endowment_b': '5'},
        {'student_id': '2', 'utility_type': 'CD', 'alpha': '0.26', 'beta': '0.24', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '3', 'utility_type': 'LINEAR', 'alpha': '0.38', 'beta': '0.32', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '4', 'utility_type': 'LINEAR', 'alpha': '0.49', 'beta': '0.53', 'endowment_a': '10', 'endowment_b': '0'},
        {'student_id': '5', 'utility_type': 'CD', 'alpha': '0.56', 'beta': '0.65', 'endowment_a': '5', 'endowment_b': '5'},
        {'student_id': '6', 'utility_type': 'LINEAR', 'alpha': '0.37', 'beta': '0.46', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '7', 'utility_type': 'LINEAR', 'alpha': '0.47', 'beta': '0.37', 'endowment_a': '0', 'endowment_b': '10'},
        {'student_id': '8', 'utility_type': 'MIN', 'alpha': '0.68', 'beta': '0.29', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '9', 'utility_type': 'MIN', 'alpha': '0.49', 'beta': '0.26', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '10', 'utility_type': 'MIN', 'alpha': '0.6', 'beta': '0.77', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '11', 'utility_type': 'LINEAR', 'alpha': '0.74', 'beta': '0.5', 'endowment_a': '5', 'endowment_b': '5'},
        {'student_id': '12', 'utility_type': 'MIN', 'alpha': '0.46', 'beta': '0.79', 'endowment_a': '0', 'endowment_b': '10'},
        {'student_id': '13', 'utility_type': 'MIN', 'alpha': '0.63', 'beta': '0.32', 'endowment_a': '7', 'endowment_b': '3'},
        {'student_id': '14', 'utility_type': 'CD', 'alpha': '0.52', 'beta': '0.3', 'endowment_a': '9', 'endowment_b': '1'},
        {'student_id': '15', 'utility_type': 'LINEAR', 'alpha': '0.76', 'beta': '0.74', 'endowment_a': '5', 'endowment_b': '5'},
        {'student_id': '16', 'utility_type': 'MIN', 'alpha': '0.77', 'beta': '0.32', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '17', 'utility_type': 'LINEAR', 'alpha': '0.51', 'beta': '0.65', 'endowment_a': '9', 'endowment_b': '1'},
        {'student_id': '18', 'utility_type': 'CD', 'alpha': '0.43', 'beta': '0.39', 'endowment_a': '7', 'endowment_b': '3'},
        {'student_id': '19', 'utility_type': 'CD', 'alpha': '0.72', 'beta': '0.41', 'endowment_a': '3', 'endowment_b': '7'},
        {'student_id': '20', 'utility_type': 'CD', 'alpha': '0.55', 'beta': '0.39', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '21', 'utility_type': 'MIN', 'alpha': '0.69', 'beta': '0.51', 'endowment_a': '0', 'endowment_b': '10'},
        {'student_id': '22', 'utility_type': 'CD', 'alpha': '0.61', 'beta': '0.25', 'endowment_a': '0', 'endowment_b': '10'},
        {'student_id': '23', 'utility_type': 'MIN', 'alpha': '0.39', 'beta': '0.37', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '24', 'utility_type': 'LINEAR', 'alpha': '0.74', 'beta': '0.29', 'endowment_a': '3', 'endowment_b': '7'},
        {'student_id': '25', 'utility_type': 'LINEAR', 'alpha': '0.71', 'beta': '0.74', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '26', 'utility_type': 'MIN', 'alpha': '0.63', 'beta': '0.42', 'endowment_a': '3', 'endowment_b': '7'},
        {'student_id': '27', 'utility_type': 'LINEAR', 'alpha': '0.21', 'beta': '0.37', 'endowment_a': '10', 'endowment_b': '0'},
        {'student_id': '28', 'utility_type': 'CD', 'alpha': '0.46', 'beta': '0.26', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '29', 'utility_type': 'MIN', 'alpha': '0.6', 'beta': '0.55', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '30', 'utility_type': 'CD', 'alpha': '0.35', 'beta': '0.76', 'endowment_a': '10', 'endowment_b': '0'},
        {'student_id': '31', 'utility_type': 'LINEAR', 'alpha': '0.2', 'beta': '0.58', 'endowment_a': '1', 'endowment_b': '9'},
        {'student_id': '32', 'utility_type': 'MIN', 'alpha': '0.21', 'beta': '0.68', 'endowment_a': '3', 'endowment_b': '7'},
        {'student_id': '33', 'utility_type': 'LINEAR', 'alpha': '0.62', 'beta': '0.7', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '34', 'utility_type': 'CD', 'alpha': '0.38', 'beta': '0.4', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '35', 'utility_type': 'MIN', 'alpha': '0.22', 'beta': '0.21', 'endowment_a': '8', 'endowment_b': '2'},
        {'student_id': '36', 'utility_type': 'CD', 'alpha': '0.26', 'beta': '0.43', 'endowment_a': '1', 'endowment_b': '9'},
        {'student_id': '37', 'utility_type': 'CD', 'alpha': '0.42', 'beta': '0.34', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '38', 'utility_type': 'LINEAR', 'alpha': '0.33', 'beta': '0.23', 'endowment_a': '6', 'endowment_b': '4'},
        {'student_id': '39', 'utility_type': 'MIN', 'alpha': '0.54', 'beta': '0.63', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '40', 'utility_type': 'LINEAR', 'alpha': '0.76', 'beta': '0.6', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '41', 'utility_type': 'LINEAR', 'alpha': '0.21', 'beta': '0.6', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '42', 'utility_type': 'LINEAR', 'alpha': '0.8', 'beta': '0.49', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '43', 'utility_type': 'CD', 'alpha': '0.31', 'beta': '0.52', 'endowment_a': '8', 'endowment_b': '2'},
        {'student_id': '44', 'utility_type': 'CD', 'alpha': '0.34', 'beta': '0.78', 'endowment_a': '7', 'endowment_b': '3'},
        {'student_id': '45', 'utility_type': 'CD', 'alpha': '0.75', 'beta': '0.45', 'endowment_a': '2', 'endowment_b': '8'},
        {'student_id': '46', 'utility_type': 'MIN', 'alpha': '0.57', 'beta': '0.53', 'endowment_a': '0', 'endowment_b': '10'},
        {'student_id': '47', 'utility_type': 'CD', 'alpha': '0.27', 'beta': '0.27', 'endowment_a': '5', 'endowment_b': '5'},
        {'student_id': '48', 'utility_type': 'CD', 'alpha': '0.75', 'beta': '0.32', 'endowment_a': '4', 'endowment_b': '6'},
        {'student_id': '49', 'utility_type': 'LINEAR', 'alpha': '0.71', 'beta': '0.66', 'endowment_a': '10', 'endowment_b': '0'},
        {'student_id': '50', 'utility_type': 'MIN', 'alpha': '0.33', 'beta': '0.54', 'endowment_a': '1', 'endowment_b': '9'}