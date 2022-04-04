
from flask import Flask, request, jsonify
import os
import pandas as pd
from preprocessing.cleaning_data import X_train, regressor

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home() -> str:
    """Check if the API is alive"""
    return {'status': 'server is alive'}

@app.route('/predict', methods=['GET'])
def get_predict():
    return """
       {
           "data" : {
               "Living area": int,
               "Property type" : "APARTMENT" | "HOUSE" | "OTHERS",
               "Bedrooms" : int,
               "Postcode" : int,
               "Swimming pool" : str,
               "Garden" : str }
}
}
    """

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.get_json()
    
    living_area = user_input['data']['Living area']
    if type(living_area) == str:
        return {"Error": "Please give a number for Living Area"}
    
    property_type = user_input['data']['Property type']
    if property_type == "APPARTMENT":
        user_input['data']['Property type'] = 1
    elif property_type == "HOUSE":
        user_input['data']['Property type'] = 2
    else:
        user_input['data']['property_type'] = 0
        return {"Error": "Please choose between Appartment, House, or Others"}
    
    bedrooms = user_input['data']['Bedrooms']
    if type(bedrooms) == str:
        return{"Error": "Please give a number for Bedrooms"}
    
    postcode = user_input['data']['Post code']
    if type(postcode) == str:
        return {"Error": "Please give a number for Post code"}
    
    swimming_pool = user_input['data'].get('Swimming pool', 'no')
    if swimming_pool == 'yes':
        user_input['data']['Swimming pool'] = 10
    elif swimming_pool == 'no':
        user_input['data']['Swimming pool'] = 0
    else:
        return {"Error": "Please answer yes or no"}
        
    garden = user_input['data'].get('Garden', 'no')
    if garden == 'yes':
        user_input['data']['Garden'] = 1
    elif garden == 'no':
        user_input['data']['Garden'] = 0
    else:
        return {"Error": "Please answer yes or no for Garden"}
     
    print(user_input)
    #transpose
    data_df = pd.DataFrame(user_input).T
    data_df = data_df.reindex(X_train.columns, axis="columns")
    print(data_df)
    
    #query = pd.get_dummies(data_df)
    prediction = regressor.predict(data_df)
    return(jsonify(f"The price prediction is {prediction}"))
        

if __name__ == '__main__':
    # You want to put the value of the env variable PORT if it exist (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
    
