from __future__ import annotations
import requests

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"

BANKING_SYSTEM_PROMPT = """
You are a banking intelligence analytics assistant.
Rules:
1. Only answer using the data provided in the prompt context.
2. Do not invent metrics, customer IDs, dates, or model outputs.
3. If the data does not answer the question, say so clearly.
4. Explain results in plain business language.
5. Keep answers concise and structured.
6. Highlight risk, anomaly, customer behaviour, and KPI trends when relevant.
7. If the user asks a follow-up question referencing previous answers, use the conversation history to provide context.
"""


def ask_ollama(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: str = BANKING_SYSTEM_PROMPT,
    temperature: float = 0.1,
    memory=None,
) -> str:
    """
    Send a prompt to Ollama.
    If memory is provided, includes conversation history for context.
    Returns empty string on any failure — never crashes.
    """
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Inject conversation history if memory provided
    if memory:
        messages.extend(memory.get_messages())

    messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()["message"]["content"].strip()

        # Save to memory if provided
        if memory and result:
            memory.add("user", prompt)
            memory.add("assistant", result)

        return result

    except requests.exceptions.ConnectionError:
        return ""
    except requests.exceptions.Timeout:
        return ""
    except Exception:
        return ""