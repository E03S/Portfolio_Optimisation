from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from portfolio_optimisation.classes.llm_model import LLMModel
from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize
import hydra
import logging
import uvicorn
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()
model = None

class Prompt(BaseModel):
    text: str
@app.get("/first_example/")
async def first_example():
    df = pd.read_csv("datasets/news_sp_500_weekly.csv")
    first_text = df["body"][0]
    response = model.create_message(first_text)
    json = model.parse_json_from_response(response)
    return json

@app.post("/generate/")
async def generate(prompt: Prompt):
    if prompt.text:
        response = model.create_message(prompt.text)
        json = model.parse_json_from_response(response)
        return json
    else:
        raise HTTPException(status_code=400, detail="No prompt provided")

@hydra.main(config_path="../../configs", config_name="config", version_base="1.3",)
def main(cfg: DictConfig):
    global model
    config = cfg.model.openai
    model = LLMModel(
        model_name=config.model_name,
        system_prompt=cfg.model.system_prompt,
        api_key=config.api_key,
        endpoint= config.endpoint,
    )
    logger.info(f"Start app with model {config.model_name}")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()