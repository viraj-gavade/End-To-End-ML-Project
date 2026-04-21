from fastapi import FastAPI
from pydantic import BaseModel
from src.pipelines.inference import InferencePipeline , InputDataSchema

app = FastAPI()
from typing import Literal

class InputData(BaseModel):
    reading_score: int
    writing_score: int
    gender: Literal["male", "female"]
    race_ethnicity: str
    parental_level_of_education: str
    test_preparation_course: Literal["none", "completed"]
    lunch: Literal["standard", "free/reduced"]

@app.post("/predict")
def predict(data: InputData):
    input_data = InputDataSchema(**data.dict())
    df = input_data.get_data_as_frame()

    pipeline = InferencePipeline()
    prediction = pipeline.predict(df)

    return {"prediction": prediction.tolist()}