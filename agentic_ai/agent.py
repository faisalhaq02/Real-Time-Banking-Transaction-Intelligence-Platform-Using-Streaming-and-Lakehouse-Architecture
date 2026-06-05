from __future__ import annotations

from agentic_ai.tools.kpi_tool import get_kpi_summary, answer_kpi_question
from agentic_ai.tools.anomaly_tool import get_anomaly_summary, answer_anomaly_question
from agentic_ai.tools.streaming_tool import get_streaming_summary, answer_streaming_question
from agentic_ai.tools.label_tool import get_label_summary, answer_label_question
from agentic_ai.tools.risk_tool import get_risk_summary, answer_risk_question
from agentic_ai.tools.segment_tool import get_segment_summary, answer_segment_question

# Global memory instance — persists across requests in the same Flask session
try:
    from agentic_ai.utils.memory import memory as _memory
except Exception:
    _memory = None


def _has_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _respond_with_fallback(user_query: str, answer_fn, summary_fn) -> str:
    """
    Try the question-specific handler first.
    Fall back to the tool summary only if needed.
    Saves the exchange to memory.
    """
    try:
        answer = answer_fn(user_query)
        if answer and str(answer).strip():
            result = str(answer).strip()
            _save_to_memory(user_query, result)
            return result
    except Exception as exc:
        return f"Server error: {exc}"

    try:
        result = summary_fn()
        _save_to_memory(user_query, result)
        return result
    except Exception as exc:
        return f"Server error: {exc}"


def _save_to_memory(user_query: str, response: str):
    """Save a query/response pair to memory. Silent on failure."""
    try:
        if _memory:
            _memory.add("user", user_query)
            _memory.add("assistant", response)
    except Exception:
        pass


def _try_ollama_general(user_query: str) -> str:
    """
    Last-resort LLM handler for queries that don't match any keyword tool.
    Builds a combined context from all available summaries and asks Ollama.
    Passes conversation memory for follow-up question support.
    Returns empty string if Ollama is unavailable — never crashes.
    """
    try:
        from agentic_ai.utils.ollama_client import ask_ollama

        context_parts = []

        try:
            kpi = get_kpi_summary()
            if kpi and "unavailable" not in kpi.lower():
                context_parts.append(f"=== KPI Summary ===\n{kpi}")
        except Exception:
            pass

        try:
            risk = get_risk_summary()
            if risk and "unavailable" not in risk.lower():
                context_parts.append(f"=== Risk Summary ===\n{risk}")
        except Exception:
            pass

        try:
            anomaly = get_anomaly_summary()
            if anomaly and "unavailable" not in anomaly.lower():
                context_parts.append(f"=== Anomaly Summary ===\n{anomaly}")
        except Exception:
            pass

        try:
            segment = get_segment_summary()
            if segment and "unavailable" not in segment.lower():
                context_parts.append(f"=== Segment Summary ===\n{segment}")
        except Exception:
            pass

        if not context_parts:
            return ""

        context = "\n\n".join(context_parts)

        prompt = (
            f"Here is a snapshot of the current banking platform data:\n\n"
            f"{context}\n\n"
            f"User question: {user_query}\n\n"
            f"Answer using only the data above. "
            f"If the data does not contain the answer, say so clearly. "
            f"Be concise and use plain business language."
        )

        # Pass memory so Ollama has conversation context
        response = ask_ollama(prompt=prompt, memory=_memory)
        return response if response and response.strip() else ""

    except Exception:
        return ""


def _is_followup_question(q: str) -> bool:
    """
    Detect if the query is a follow-up referencing previous context.
    These should go straight to Ollama with memory rather than keyword routing.
    """
    followup_signals = [
        "which of those", "of those", "those customers", "those transactions",
        "from those", "in those", "among those", "for those",
        "tell me more", "more about", "more details", "elaborate",
        "what about them", "and them", "what else", "anything else",
        "how about", "what happened to", "why did", "what caused",
        "compare them", "show me those", "list them", "filter those",
        "in canada", "in the us", "in that segment", "in that group",
        "which ones", "how many of", "what percentage",
    ]
    return _has_any(q, followup_signals)


def run_agent(user_query: str) -> str:
    if not user_query or not user_query.strip():
        return "Please enter a question."

    q = user_query.strip().lower()

    # ----------------------------
    # STEP 0 — FOLLOW-UP DETECTION
    # If the query references previous context, go straight to
    # Ollama with memory rather than routing to a specific tool.
    # ----------------------------
    if _is_followup_question(q) and _memory and _memory.get_messages():
        try:
            from agentic_ai.utils.ollama_client import ask_ollama

            # Build current data context as well
            context_parts = []
            try:
                risk = get_risk_summary()
                if risk and "unavailable" not in risk.lower():
                    context_parts.append(f"=== Risk Summary ===\n{risk}")
            except Exception:
                pass

            try:
                anomaly = get_anomaly_summary()
                if anomaly and "unavailable" not in anomaly.lower():
                    context_parts.append(f"=== Anomaly Summary ===\n{anomaly}")
            except Exception:
                pass

            context = "\n\n".join(context_parts) if context_parts else ""

            prompt = (
                f"Current platform data for reference:\n{context}\n\n"
                f"User follow-up question: {user_query}\n\n"
                f"Answer using the conversation history and data above. "
                f"Be concise and use plain business language."
            ) if context else user_query

            response = ask_ollama(prompt=prompt, memory=_memory)
            if response and response.strip():
                _save_to_memory(user_query, response)
                return response
        except Exception:
            pass  # fall through to normal routing

    # ----------------------------
    # STEP 1 — LANGCHAIN SEMANTIC ROUTING
    # Handles natural language queries without exact keywords.
    # ----------------------------
    try:
        from agentic_ai.utils.langchain_router import classify_intent
        intent = classify_intent(user_query)

        if intent == "kpi":
            return _respond_with_fallback(user_query, answer_kpi_question, get_kpi_summary)
        elif intent == "anomaly":
            return _respond_with_fallback(user_query, answer_anomaly_question, get_anomaly_summary)
        elif intent == "risk":
            return _respond_with_fallback(user_query, answer_risk_question, get_risk_summary)
        elif intent == "segment":
            return _respond_with_fallback(user_query, answer_segment_question, get_segment_summary)
        elif intent == "streaming":
            return _respond_with_fallback(user_query, answer_streaming_question, get_streaming_summary)
        elif intent == "label":
            return _respond_with_fallback(user_query, answer_label_question, get_label_summary)
        # intent == "general" falls through to keyword matching
    except Exception:
        pass

    # ----------------------------
    # STEP 2 — KEYWORD ROUTING
    # ----------------------------

    anomaly_keywords = [
        "anomaly", "anomalies", "suspicious transaction", "suspicious transactions",
        "suspicious atm", "atm anomaly", "flagged transaction", "flagged transactions",
        "outlier", "outliers", "show anomalies", "show suspicious", "why was this flagged",
        "why flagged", "top suspicious", "top suspicious transactions", "highest anomaly",
        "anomaly score", "declined transaction", "declined transactions",
    ]
    if _has_any(q, anomaly_keywords):
        return _respond_with_fallback(user_query, answer_anomaly_question, get_anomaly_summary)

    streaming_keywords = [
        "stream", "streaming", "live transaction", "live transactions", "latest timestamp",
        "latest transaction", "last transaction", "last 10 transactions", "recent transactions",
        "transaction feed", "new transactions", "latest batch", "recent batch",
        "latest stream", "live feed",
    ]
    if _has_any(q, streaming_keywords):
        return _respond_with_fallback(user_query, answer_streaming_question, get_streaming_summary)

    risk_keywords = [
        "risk", "risk score", "risk overview", "high risk", "high-risk",
        "risky customer", "risky customers", "high-risk customer", "high-risk customers",
        "riskiest customer", "top risk customers", "fraud risk", "customer risk",
        "risk distribution",
    ]
    if _has_any(q, risk_keywords):
        return _respond_with_fallback(user_query, answer_risk_question, get_risk_summary)

    segment_keywords = [
        "segment", "segments", "customer segment", "customer segments", "segment summary",
        "segment breakdown", "largest segment", "smallest segment", "segment distribution",
        "customer group", "customer groups", "mass market", "high net worth",
        "high value customers", "affluent", "business segment",
    ]
    if _has_any(q, segment_keywords):
        return _respond_with_fallback(user_query, answer_segment_question, get_segment_summary)

    label_keywords = [
        "label", "labels", "customer labels", "classification", "classifications",
        "tag", "tags", "customer category", "customer categories",
    ]
    if _has_any(q, label_keywords):
        return _respond_with_fallback(user_query, answer_label_question, get_label_summary)

    kpi_keywords = [
        "kpi", "kpis", "executive summary", "executive metrics", "business summary",
        "dashboard summary", "latest kpi", "latest kpis", "transaction volume",
        "total transaction volume", "total spend", "average transaction",
        "average transaction amount", "avg amount", "transaction count",
        "total customers", "customer count", "merchant summary", "channel summary",
        "geo summary", "city has the highest spend", "highest spend",
        "top merchant categories", "top channels",
    ]
    if _has_any(q, kpi_keywords):
        return _respond_with_fallback(user_query, answer_kpi_question, get_kpi_summary)

    # Smart fallbacks
    if "timestamp" in q or "latest time" in q:
        return _respond_with_fallback(user_query, answer_streaming_question, get_streaming_summary)

    if "flagged" in q or "suspicious" in q:
        return _respond_with_fallback(user_query, answer_anomaly_question, get_anomaly_summary)

    if "riskiest" in q or "risk score" in q:
        return _respond_with_fallback(user_query, answer_risk_question, get_risk_summary)

    if "segment" in q:
        return _respond_with_fallback(user_query, answer_segment_question, get_segment_summary)

    # ----------------------------
    # STEP 3 — OLLAMA GENERAL FALLBACK
    # ----------------------------
    ollama_response = _try_ollama_general(user_query)
    if ollama_response:
        _save_to_memory(user_query, ollama_response)
        return ollama_response

    # ----------------------------
    # STEP 4 — FINAL FALLBACK
    # ----------------------------
    return (
        "I can help with KPI summaries, anomaly detection, risk scores, "
        "customer segments, streaming transactions, and customer labels.\n\n"
        "Try asking:\n"
        "- Show KPI summary\n"
        "- What is the average transaction amount?\n"
        "- Which city has the highest spend?\n"
        "- Show anomalies\n"
        "- Show suspicious ATM transactions\n"
        "- Show anomaly by country\n"
        "- Why was this transaction flagged?\n"
        "- Show high-risk customers\n"
        "- Who is the riskiest customer?\n"
        "- Summarize customer segments\n"
        "- Which segment is the largest?\n"
        "- Show segment breakdown\n"
        "- Show last 10 transactions\n"
        "- What is the latest timestamp?\n"
        "- Show customer labels\n"
        "- Give me executive summary"
    )
