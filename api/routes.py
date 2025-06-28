from fastapi import APIRouter
from pydantic import BaseModel
from chatbot.agent import generate_response

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/chat/")
async def chat_endpoint(data: Message):
    reply = await generate_response(data.message)
    return {"response": reply}