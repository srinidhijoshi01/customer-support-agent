from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import SupportAgent
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI(title="Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SupportAgent()

class ChatRequest(BaseModel):
    customer_name: str
    customer_id: str
    message: str

@app.post("/api/chat")
def chat(request: ChatRequest):
    response = agent.handle_support_request(
        customer_name=request.customer_name,
        customer_id=request.customer_id,
        message=request.message
    )
    return {"response": response}

@app.post("/api/chat/no-memory")
def chat_no_memory(request: ChatRequest):
    response = agent.handle_support_request_no_memory(
        customer_name=request.customer_name,
        customer_id=request.customer_id,
        message=request.message
    )
    return {"response": response}

@app.get("/api/history/{customer_id}")
def get_history(customer_id: str):
    history = agent.get_customer_history(customer_id)
    return {"history": history}

# Ensure the frontend directory exists before mounting
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
