import pandas as pd
import pickle
import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor

def load_data():
    data = pd.read_csv("predictor/BR_data.csv")
    data = data.drop(columns=['Unnamed: 0', 'STATE', 'SITE_TYPE', 'WLCODE'])
    data.iloc[:, 3:] = data.iloc[:, 3:].apply(lambda row: row.fillna(int(row.mean())), axis=1)
    
    districts = ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur',
       'Bhojpur', 'Buxar', 'Darbhanga', 'Gaya', 'Gopalganj', 'Jamui',
       'Jehanabad', 'Kaimur (bhabua)', 'Katihar', 'Khagaria',
       'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Nawada',
       'Munger', 'Muzaffarpur', 'Nalanda', 'Pashchim Champaran', 'Patna',
       'Purba Champaran', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur',
       'Saran (chhapra)', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan',
       'Supaul','Vaishali']
    district_mapping = {district: index for index, district in enumerate(districts)}
    data['DISTRICT'] = data['DISTRICT'].map(district_mapping)
    return data, district_mapping

data, district_mapping = load_data()

def train_models(data):
    models_and_scalers = {}

    for _, row in data[['DISTRICT', 'LAT', 'LON']].drop_duplicates().iterrows():
        district_input = int(row['DISTRICT'])
        latitude_input = round(row['LAT'], 6)
        longitude_input = round(row['LON'], 6)

        row_data = data[(data['DISTRICT'] == district_input) &
                        (round(data['LAT'], 6) == latitude_input) &
                        (round(data['LON'], 6) == longitude_input)]
        
        if row_data.empty:
            continue

        groundwater_data = row_data.iloc[0, 3:].values.flatten().astype(float)
        groundwater_data = groundwater_data.reshape(-1, 1)
        
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(groundwater_data).flatten()

        X, y = [], []
        for i in range(12, len(scaled_data)):
            X.append(scaled_data[i - 12:i])
            y.append(scaled_data[i])
        
        model = LinearRegression()
        model.fit(np.array(X), np.array(y))

        models_and_scalers[(district_input, latitude_input, longitude_input)] = {
            'model': model,
            'scaler': scaler
        }
    
    with open('predictor/BR_LR.pkl', 'wb') as file:
        pickle.dump(models_and_scalers, file)

def predict_groundwater(district, latitude, longitude, month, year):
    try:
        with open('predictor/BR_LR.pkl', 'rb') as file:
            models_and_scalers = pickle.load(file)

        key = (district, round(latitude, 6), round(longitude, 6))
        if key not in models_and_scalers:
            return "No model found for the specified location."

        model_and_scaler = models_and_scalers[key]
        model = model_and_scaler['model']
        scaler = model_and_scaler['scaler']

        groundwater_data = data[(data['DISTRICT'] == district) &
                                (round(data['LAT'], 6) == round(latitude, 6)) &
                                (round(data['LON'], 6) == round(longitude, 6))]
        groundwater_data = groundwater_data.iloc[0, 3:].values.flatten().astype(float).reshape(-1, 1)
        scaled_data = scaler.transform(groundwater_data).flatten()

        current_input = scaled_data[-12:]
        index = (month - 1) + (year - 2017) * 4

        for _ in range(index):
            prediction = model.predict([current_input[-12:]])[0]
            current_input = np.append(current_input, prediction)

        final_prediction = scaler.inverse_transform([[current_input[-1]]])
        a= round(final_prediction[0][0], 2)
        if a>30 :
            return "This well does not contain enough data to predict"
        else:
            if a>10:
                return f"You are in the danger zone. \nPredicted value : {round(final_prediction[0][0], 2)}"
            
            else:
                return f"You are in the safe zone. \nPredicted value : {round(final_prediction[0][0], 2)}"
        

    except FileNotFoundError:
        return "Model file not found. Please train the models."