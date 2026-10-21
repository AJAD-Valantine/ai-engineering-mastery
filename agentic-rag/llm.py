from langchain_community.chat_models import ChatOllama
from state import EvidenceGrade, RouteDecision

llm = ChatOllama(model="llama3.1:8b")
router_llm = llm.with_structured_output(RouteDecision, method="json_mode")
kb_grader_llm = llm.with_structured_output(EvidenceGrade, method="json_mode")
web_grader_llm = llm.with_structured_output(EvidenceGrade, method="json_mode")
