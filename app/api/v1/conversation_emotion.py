"""Conversational emotion routes — schemas ready; endpoints optional in MVP."""

from fastapi import APIRouter

router = APIRouter(tags=["conversation"])

# POST /conversation can be added when ML pipeline is ready:
# @router.post("/conversation", response_model=ConversationEmotionResponse)
# def post_conversation_analysis(body: ConversationEmotionRequest) -> ConversationEmotionResponse:
#     return conversation_service.analyze_conversation(body)
