from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import joblib
import pandas as pd
from url_extractor import extractor

app = FastAPI()

# Load the pre-trained model
model = joblib.load(r"C:\Users\ameys\Desktop\Projects\Phishing URL Predictor\saved_models\xgb_model.pkl")

class URLData(BaseModel):
    url: HttpUrl

@app.post("/recieve_url")
async def receive_url(data: URLData):
    try:
        url = str(data.url)
        features = extractor(url)
        
        feature_columns = ['Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State','Request_URL', 'URL_of_Anchor', 'web_traffic']
        features_df = pd.DataFrame([features], columns=feature_columns)
        
        prediction = model.predict(features_df)[0]
        
        return {"prediction": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
