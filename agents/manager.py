# agents/manager.py
from openai import OpenAI
from dotenv import load_dotenv
import os
from agents import qualitative, quantitative
from validation.validator import validate_qualitative, validate_quantitative
from tokenomics.logger import log
import re
load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), 
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/")


##original query
# def classify(query: str) -> str:
#     message = client.chat.completions.create(
#         model="gemini-3.5-flash-lite",
#         max_tokens=10,
#         messages=[{
#             "role": "user",
#             "content": f"""Classify this query as exactly one of: qualitative, quantitative, both.

# qualitative = questions about policies, processes, procedures, explanations, documentation
# quantitative = questions about numbers, metrics, trends, comparisons, SQL-queryable data
# both = questions that need both document search and data analysis

# Query: {query}

# Reply with one word only: qualitative, quantitative, or both."""
#         }]
#     )
#     route = message.choices[0].message.content.strip().lower()
#     log(query, "manager-classifier", message.usage.prompt_tokens, message.usage.completion_tokens)
#     return route if route in ["qualitative", "quantitative", "both"] else "qualitative"


###expanding on the original query classification logic
###this first checks for numeric/SQL intent before invoking the LLM for classification
def classify(query: str) -> str:
    numeric_intent = re.search(
        r"\b("
        r"how many|number of|count|sum|total|average|mean|median|"
        r"percentage|percent|rate|growth|trend|trends|over time|"
        r"variance|calculate|quantify|distribution|"
        r"insert|update|delete|upsert|merge|truncate|create|alter|drop"
        r")\b",
        query,
        re.IGNORECASE,
    )

    # Entity and document lookups—such as identifying an employee ARE qualitative,
    # even when the underlying data is stored in SQL.
    if not numeric_intent:
        log(query, "manager-classifier", 0, 0)
        return "qualitative"
    ##below is the classification logic and what should be regarded as qualitative or quantiative
    ##the original code was a good starter point, but there were occasional classifcation errors. 
    ##this should resolve that issue
    message = client.chat.completions.create(
        model="gemini-3.5-flash-lite",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": f"""Classify this query as exactly one of: qualitative, quantitative, both.

qualitative includes:
- policies, processes, procedures, explanations, and documentation
- factual lookups from documents or records
- identifying a person, employee, department, case, report, date, or policy
- questions beginning with who, which, what, or where

quantitative includes:
- counts, sums, averages, percentages, rates, trends, growth,
  numerical calculations, numeric comparisons, insert, update, delete, upsert, merge, truncate, create, alter, drop
- If the user asks to perform or generate a database operation, return quantitative. This includes INSERT, UPDATE, DELETE, UPSERT, MERGE, TRUNCATE, CREATE,
   ALTER, DROP, SQL generation, and natural-language requests such as: "insert a company into the database".

both means the same query explicitly requires document interpretation
AND numerical analysis.

A question is not quantitative merely because its answer is stored in SQL.
Do not classify a question as both merely because it contains "and".

Examples:
"What is our employee complaint policy?" -> qualitative
"Which employee submitted the report?" -> qualitative
"How many complaints were submitted?" -> quantitative
"What is the complaint policy and how many complaints were submitted?" -> both

Query: {query}

Reply with one word only: qualitative, quantitative, or both.""",
            }
        ],
    )

    raw_route = (message.choices[0].message.content or "").strip().lower()
    route = raw_route.split()[0].strip("`.,:;") if raw_route else ""

    log(
        query,
        "manager-classifier",
        message.usage.prompt_tokens,
        message.usage.completion_tokens,
    )

    return route if route in {"qualitative", "quantitative", "both"} else "qualitative"












def run(query: str):
    print(f"\nQuery: {query}")
    route = classify(query)
    print(f"Route: {route}")

    qual_result = None
    quant_result = None

    if route in ["qualitative", "both"]:
        qual_result = qualitative.run(query)
        validation = validate_qualitative(qual_result["answer"], qual_result["chunks"])
        log(query, "qualitative", qual_result["input_tokens"], qual_result["output_tokens"])
        if validation["flag"]:
            print(f"\n⚠️  VALIDATION WARNING: {validation['warning']}")
        print(f"\n[Qualitative]\n{qual_result['answer']}")

    if route in ["quantitative", "both"]:
        quant_result = quantitative.run(query)
        validation = validate_quantitative(
            quant_result["answer"],
            quant_result["sql"],
            quant_result["validation"]
        )
        log(query, "quantitative", quant_result["input_tokens"], quant_result["output_tokens"])
        if validation["flag"]:
            print(f"\n⚠️  VALIDATION WARNING: {validation['warning']}")
        print(f"\n[Quantitative]\n{quant_result['answer']}")
        print(f"SQL used: {quant_result['sql']}")
    return {
        "route": route,
        "qualitative": qual_result,
        "quantitative": quant_result,
    }