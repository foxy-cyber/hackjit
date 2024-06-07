import pandas as pd
import joblib

def load_model(model_path):
    return joblib.load(model_path)

def load_data(csv_file):
    return pd.read_csv(csv_file)

def preprocess_data(df):
    # Convert categorical variables to numerical
    df['Mouth Open'] = df['Mouth Open'].fillna(0).astype(int)  # Fill NaN with 0 before converting
    df['Head Pose'] = df['Head Pose'].map({'Looking at screen': 1, 'Looking away from screen': 0})
    df['Eye Tracking'] = df['Eye Tracking'].map({'Looking at screen': 1, 'Looking away from screen': 0})
    
    # Convert 'Spoof Face Detected' to numerical
    df['Spoof Face Detected'] = df['Spoof Face Detected'].map({'TRUE': 1, 'FALSE': 0})
    
    return df

def make_predictions(model, data):
    # Define features
    X_test = data[['Banned Objects', 'Number of Faces Detected', 'Mouth Open', 'Head Pose', 'Eye Tracking', 'Spoof Face Detected']]
    
    # Make predictions using the trained model
    y_pred = model.predict(X_test)
    return y_pred

def save_predictions(predictions, output_path):
    predictions.to_csv(output_path, index=False)

def ml_model(csv_file_path):
    model_path = 'C:/Users/tilak/Desktop/hackathon/exam_project/exam_app/ml/best_model.joblib'
    output_path = 'C:/Users/tilak/Desktop/hackathon/exam_project/exam_app/ml/predictions.csv'
    
    # Load model and data
    model = load_model(model_path)
    data = load_data(csv_file_path)
    
    # Preprocess data
    processed_data = preprocess_data(data)
    
    # Drop the 'Image Name' column if it exists
    if 'Image Name' in processed_data.columns:
        processed_data = processed_data.drop(columns=['Image Name'])
    
    # Make predictions
    predictions = make_predictions(model, processed_data)
    
    # Add predicted cheating column to the dataframe
    processed_data['Predicted Cheating'] = predictions
    
    # Save predictions
    save_predictions(processed_data, output_path)
    
    # Display count of predicted cheating values greater than 7
    count_greater_than_7 = (predictions > 7).sum()
    
    # Check the 'Number of People' column for values greater than 1
    if 'Number of People' in data.columns:
        # Handle NA values by filling them with a default value, for example, 0
        data['Number of People'] = data['Number of People'].fillna(0)
        num_people_greater_than_one = (data['Number of People'] > 1).sum()
        
        
        print(f"More than {num_people_greater_than_one} people attending the exam.")
    
    return count_greater_than_7

# csv_file_path = "C:/Users/tilak/Desktop/hackathon/exam_project/exam_app/cv/Code/csv/student3/proctoring_results.csv"
# count_gt_7 = ml_model(csv_file_path)
# print(f"Count of predicted cheating values greater than 7: {count_gt_7}")