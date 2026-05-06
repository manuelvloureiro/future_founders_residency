from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data import scenario
from models import ApproveRequest, ApproveResponse, Scenario

app = FastAPI(title="IDM Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/scenario", response_model=Scenario)
def get_scenario():
    return scenario


@app.post("/api/scenario/approve", response_model=ApproveResponse)
def approve_scenario(req: ApproveRequest):
    return ApproveResponse(
        message="Reallocation scheduled · Prices update tonight 00:00"
    )
