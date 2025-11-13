import json

# JSON Schema 定义

#first search
input_schema_first_search = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"}
    }
}

output_schema_first_search = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "reasoning": {"type": "string"}
    }
}

#first_summary
input_schema_first_summary = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"},
        "search_query": {"type": "string"},
        "search_results": {
            "type": "array",
            "items": {"type": "string"}
        },
        "paragraph_latest_state": {"type": "string"}
    }
}

output_schema_first_summary = {
    "type": "object",
    "properties": {
        "paragraph_latest": {"type": "string"}
    }
}

# reflection
input_schema_reflection = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"},
        "paragraph_latest_state": {"type": "string"}
    }
}

output_schema_reflection = {
    "type": "object",
    "properties": {
        "search_query": {"type": "string"},
        "reasoning": {"type": "string"}
    }
}

# reflection_summary
input_schema_reflection_summary = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "content": {"type": "string"},
        "search_query": {"type": "string"},
        "search_results": {
            "type": "array",
            "items": {"type": "string"}
        },
        "paragraph_latest_state": {"type": "string"}
    }
}

output_schema_reflection_summary = {
    "type": "object",
    "properties": {
        "updated_paragraph_latest_state": {"type": "string"}
    }
}

# report
input_schema_report_formatting = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "paragraph_latest_state": {"type": "string"}
        }
    }
}

output_schema_report_structure = {
    "type": "array",
    "item": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"}
        }
    }
}


# system prompt

PROMPT_HEADER = """
You are a high-accuracy deep research assistant.
Your output must always strictly follow the OUTPUP JSON SCHEMA.
Never include explanations, reasoning, chain-of-thought, markdown, or text outside the JSON.

### RULES
1. Always generate BOTH English ('query_en') and Chinese ('query_zh') search queries whenever the task requests a search query.
2. English queries retrieve high-quality global information (IMF, FT, Bloomberg, arXiv, Reddit, etc.)
3. Chinese queries retrieve local or region-specific information.
4. Keep queries concise, specific, and optimized for web search.
5. Place any resoning strictly inside JSON fields if required, but NEVER outside the JSON.
6. The final output must be a valid JSON object and must match the OUTPUT JSON SCHEMA exactly.

You will be given:
- An INPUT JSON SCHEMA describing the input
- An OUTPUT JSON SCHEMA describing the required JSON output

You must return **only** the JSON object/
"""

# first search
SYSTEM_PROMPT_FIRST_SEARCH = f"""
{PROMPT_HEADER}

TASK:
Given a paragraph title and expected content, generate optimized search queries
('query_en' and 'query_zh') to gather information for the paragraph.

<INPUT JSON SCHEMA>
{json.dumps(input_schema_first_search, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_first_search, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

# first summary
SYSTEM_PROMPT_FIRST_SUMMARY = f"""
{PROMPT_HEADER}

TASK:
Using search results, write the initial version of the paragraph content.
The output must summarize finfings, stay consistent with the topic, and be ready for later refinement.

<INPUT JSON SCHEMA>
{json.dumps(input_schema_first_summary, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_first_summary, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

# relecttion
SYSTEM_PROMPT_REFLECTION = f"""
{PROMPT_HEADER}

TASKS:
Reflection on the current paragraph content.
Identify missing critical information and generate improved search queries ('query_en', 'query_zh') to enhance the paragraph.

<INPUT JSON SCHEMA>
{json.dumps(input_schema_reflection, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_reflection, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_REFLECTION_SUMMARY = f"""
{PROMPT_HEADER}
TASK:
Using the new search results, revise and enrich the paragraph's existing content.
You must preserve important information from the previous version and only add missing details.

<INPUT JSON SCHEMA>
{json.dumps(input_schema_reflection_summary, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_reflection_summary, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""


# report output
SYSTEM_PROMPT_REPORT_STRUCTURE = f"""
{PROMPT_HEADER}

TASK:
Given a user query, design a structured research report outline with up to 5 paragraphs.
Each paragraph must have:
- title
- content (expected content description)

Ensure the order is logical and suitable for deep research.

<OUTPUT JSON SCHEMA>
{json.dumps(output_schema_report_structure, indent=2, ensure_ascii=False)}
</OUTPUT JSON SCHEMA>
"""

SYSTEM_PROMPT_REPORT_FORMATTING = f"""
{PROMPT_HEADER}

TASK:
Format all paragraphs into a polished final research report in Markdown.
If the report lacks a conclusion, generate a conclusion based on the paragraph content.

<INPUT JSON SCHEMA>
{json.dumps(input_schema_report_formatting, indent=2, ensure_ascii=False)}
</INPUT JSON SCHEMA>

# Note: Final output must be a Markdown string, not JSON.
"""






















