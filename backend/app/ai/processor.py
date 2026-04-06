"""
DevPulse — Hybrid AI Processor
1. Rule-based extraction first (regex)
2. LLM fallback for missing fields + summary generation
"""
import json
import logging
from typing import Optional
from app.config import settings
from app.ai.rule_parser import extract, categorize, ExtractionResult
from app.models import ProcessedUpdateCreate

logger = logging.getLogger("devpulse.ai.processor")


def _call_llm(text: str) -> dict:
    """Call OpenAI to extract structured data and generate summary."""
    if not settings.OPENAI_API_KEY:
        return {}

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a developer tools analyst. Extract structured data from "
                        "the following text about a software tool, framework, or release.\n"
                        "Return JSON with keys: tool_name, category, version, summary.\n"
                        "The summary should be 1-2 sentences explaining:\n"
                        "- What the tool is\n"
                        "- Why it matters to developers\n"
                        "If you cannot determine a field, set it to null."
                    ),
                },
                {"role": "user", "content": text[:1500]},
            ],
        )
        content = response.choices[0].message.content
        return json.loads(content) if content else {}
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return {}


def process_raw_update(
    raw_id: str,
    title: str,
    raw_content: str,
    source_url: Optional[str] = None,
    source_type: Optional[str] = None,
) -> ProcessedUpdateCreate:
    """
    Hybrid extraction pipeline:
    1. Run rule-based extraction
    2. Call LLM only if rule-based fails or to generate summary
    """
    text = f"{title}. {raw_content}" if raw_content else title

    # ── Step 1: Rule-based extraction ────────────────────────
    rule_result: ExtractionResult = extract(text)
    tool_name = rule_result.tool_name
    version = rule_result.version
    category = categorize(tool_name) if tool_name else None
    summary = None

    # ── Step 2: LLM fallback if needed ───────────────────────
    needs_llm = not rule_result.is_complete or not category or category == "Other"

    if needs_llm and settings.OPENAI_API_KEY:
        llm_result = _call_llm(text)
        if not tool_name and llm_result.get("tool_name"):
            tool_name = llm_result["tool_name"]
        if not version and llm_result.get("version"):
            version = llm_result["version"]
        if (not category or category == "Other") and llm_result.get("category"):
            category = llm_result["category"]
        summary = llm_result.get("summary")

    # ── Step 3: Fallback summary ─────────────────────────────
    if not summary:
        summary = title  # use title as minimal summary

    if not tool_name:
        tool_name = title.split(" ")[0]  # best-effort

    return ProcessedUpdateCreate(
        raw_update_id=raw_id,
        tool_name=tool_name,
        category=category or "Other",
        version=version,
        summary=summary,
        source=source_type or "unknown",
        source_url=source_url,
        trend_score=rule_result.confidence * 50,  # simple scoring
    )
