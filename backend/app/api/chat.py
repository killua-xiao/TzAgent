from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional
from pydantic import BaseModel
import json
from ..services.chat_service import ChatService

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[list] = None
    suggestions: Optional[list] = None

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    """WebSocket实时聊天"""
    await websocket.accept()
    chat_service = ChatService()
    
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            session_id = data.get("session_id", "")
            context = data.get("context", {})
            
            # 处理消息并生成响应
            response = await chat_service.process_message(
                message, session_id, context
            )
            
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        print("WebSocket连接断开")
    except Exception as e:
        print(f"WebSocket聊天错误: {e}")

@router.post("/message")
async def send_message(chat_message: ChatMessage):
    """发送聊天消息（HTTP接口）"""
    try:
        chat_service = ChatService()
        response = await chat_service.process_message(
            chat_message.message,
            chat_message.session_id,
            chat_message.context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"消息处理失败: {str(e)}")

@router.get("/sessions/{session_id}")
async def get_chat_history(session_id: str):
    """获取聊天历史"""
    try:
        history = await ChatService.get_chat_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取聊天历史失败: {str(e)}")

@router.delete("/sessions/{session_id}")
async def clear_chat_history(session_id: str):
    """清空聊天历史"""
    try:
        await ChatService.clear_chat_history(session_id)
        return {"success": True, "message": "聊天历史已清空"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空聊天历史失败: {str(e)}")