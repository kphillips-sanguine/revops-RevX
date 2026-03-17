"""LLM-enhanced schema documentation using Gemini Flash.

Called by the schema crawler when --enhance is passed.
Takes raw schema markdown and produces enriched, contextual documentation.
"""

import json
import logging
import os
import sys
import urllib.request
import urllib.error

log = logging.getLogger("rag.enhance")

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL = os.environ.get("ENHANCE_MODEL", "gemini-2.0-flash")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def call_gemini(prompt: str, max_tokens: int = 4096) -> str:
    """Call Gemini Flash API and return text response."""
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not set — cannot enhance schema")

    url = f"{API_URL}?key={GOOGLE_API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.3,
        }
    }).encode()

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        log.error(f"Gemini API error {e.code}: {error_body[:500]}")
        raise
    except Exception as e:
        log.error(f"Gemini API call failed: {e}")
        raise


def enhance_object_schema(object_name: str, raw_schema: str, org_alias: str = "dev") -> str:
    """Enhance a raw object schema dump with contextual descriptions."""

    prompt = f"""You are a Salesforce documentation expert. You're documenting the schema for a biotech company (Sanguine Bio) that connects patients with clinical research opportunities and facilitates biological sample collection.

Below is the raw schema for the **{object_name}** object from the **{org_alias}** org. Enhance this into clear, useful documentation:

1. **Object Overview** — Write 2-3 sentences explaining what this object is used for in the context of a biotech/clinical research company. If it's a standard object, explain how Sanguine Bio likely uses it.

2. **Field Groups** — Organize the fields into logical groups (e.g., "Contact Information", "Billing", "Custom Business Logic", "System Fields"). For each group, briefly explain its purpose.

3. **Key Fields** — For important custom fields and key standard fields, add a one-line description of what they're likely used for and why they matter.

4. **Relationships** — Call out any lookup/master-detail relationships and explain what they connect.

5. **Record Types** — If record types exist, explain when each is used.

6. **Validation Rules** — If validation rules exist, explain what business rules they enforce.

Keep the original field table data intact (API names, types, etc.) but reorganize and annotate it. Use markdown formatting. Be concise — this is reference documentation, not a novel.

---

RAW SCHEMA:

{raw_schema}

---

Write the enhanced documentation in markdown. Start with a level-1 heading: # {object_name}"""

    return call_gemini(prompt, max_tokens=6000)


def enhance_object_inventory(raw_inventory: str, org_alias: str = "dev") -> str:
    """Enhance the object inventory with descriptions and categorization."""

    prompt = f"""You are a Salesforce documentation expert for Sanguine Bio, a biotech company that connects patients with clinical research and facilitates biological sample collection.

Below is a raw list of Salesforce objects from the **{org_alias}** org. Enhance it by:

1. **Categorize objects** into logical groups (e.g., "Core CRM", "Clinical Research", "Revenue Operations", "DevOps/Internal Tools", "System/Config")
2. **Add brief descriptions** for each object (1 sentence — what it's for)
3. **Highlight key relationships** between objects
4. **Note which objects are most important** for the business

Keep it concise — this is a reference index, not a deep dive.

---

RAW INVENTORY:

{raw_inventory}

---

Write the enhanced inventory in markdown. Start with: # Salesforce Object Inventory — {org_alias} org"""

    return call_gemini(prompt, max_tokens=4000)


def enhance_permissions(raw_permissions: str, org_alias: str = "dev") -> str:
    """Enhance permission set/profile docs with context."""

    prompt = f"""You are a Salesforce security expert for Sanguine Bio, a biotech company.

Below are the permission sets and profiles from the **{org_alias}** org. Enhance by:

1. **Group permission sets** by app/feature area
2. **Describe what each likely grants** based on the naming convention
3. **Note any security considerations** (portal users, API access, admin rights)
4. **Suggest best practices** if you see patterns worth calling out

Keep it concise — reference documentation style.

---

RAW DATA:

{raw_permissions}

---

Write enhanced documentation in markdown."""

    return call_gemini(prompt, max_tokens=3000)


# ---------------------------------------------------------------------------
# CLI interface — called from schema-crawler.sh
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(description="Enhance schema docs with Gemini Flash")
    parser.add_argument("--type", required=True, choices=["object", "inventory", "permissions"],
                        help="Type of schema to enhance")
    parser.add_argument("--name", default="", help="Object API name (for type=object)")
    parser.add_argument("--org", default="dev", help="Org alias")
    parser.add_argument("--input", required=True, help="Input file (raw schema markdown)")
    parser.add_argument("--output", required=True, help="Output file (enhanced markdown)")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        raw_content = f.read()

    try:
        if args.type == "object":
            enhanced = enhance_object_schema(args.name, raw_content, args.org)
        elif args.type == "inventory":
            enhanced = enhance_object_inventory(raw_content, args.org)
        elif args.type == "permissions":
            enhanced = enhance_permissions(raw_content, args.org)
        else:
            print(f"Unknown type: {args.type}", file=sys.stderr)
            sys.exit(1)

        with open(args.output, "w") as f:
            f.write(enhanced)

        print(f"  🧠 Enhanced: {args.output}")

    except Exception as e:
        print(f"  ⚠️ Enhancement failed ({e}), keeping raw version", file=sys.stderr)
        # Fall back to raw content
        with open(args.output, "w") as f:
            f.write(raw_content)
