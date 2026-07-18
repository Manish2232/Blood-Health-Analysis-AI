def get_llm_text(response):
    if isinstance(response.content, list):
        for item in response.content:
            if item.get("type") == "text":
                return item.get("text", "").strip()

    return str(response.content).strip()