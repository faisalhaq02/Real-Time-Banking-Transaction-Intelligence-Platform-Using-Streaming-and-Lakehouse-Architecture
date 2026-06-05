# agentic_ai/utils/langchain_router.py
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM 

llm = OllamaLLM(model="llama3.1:8b", temperature=0)

ROUTE_PROMPT = PromptTemplate.from_template("""
You are a query router for a banking analytics system.
Classify this query into exactly ONE category:

Categories:
- kpi: questions about totals, averages, transaction counts, revenue, spend
- anomaly: suspicious transactions, fraud, flagged, outliers
- risk: customer risk scores, high risk customers, fraud risk
- segment: customer groups, segments, demographics
- streaming: live transactions, latest batch, real-time data
- label: customer labels, classifications, tags
- general: anything else

Query: {query}

Respond with ONLY the category name, nothing else.
""")

def classify_intent(query: str) -> str:
    try:
        chain = ROUTE_PROMPT | llm
        result = chain.invoke({"query": query}).strip().lower()
        valid = {"kpi", "anomaly", "risk", "segment", "streaming", "label", "general"}
        return result if result in valid else "general"
    except Exception:
        return "general"  # fall back to existing keyword routing