from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from portfolio_optimisation.classes.llm_model import LLMModel
from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize
import hydra
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()
model = None

class Prompt(BaseModel):
    text: str

@app.post("/generate/")
async def generate(prompt: Prompt):
    if prompt.text:
        response = model.create_message(prompt.text)
        return response
    else:
        raise HTTPException(status_code=400, detail="No prompt provided")

@hydra.main(config_path="../../configs", config_name="config", version_base="1.3",)
def main(cfg: DictConfig):
    global model
    model = LLMModel(
        model_name=cfg.model.model_name,
        system_prompt=cfg.model.system_prompt,
        api_key=cfg.model.api_key,
        endpoint=cfg.model.endpoint,
    )
    logger.info(f"Start app with model {cfg.model.model_name}")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()