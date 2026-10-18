from fastapi import FastAPI
import os
import pandas as pd
import pyodbc
from openai import OpenAI
from db import get_db_connection
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Initialize OpenAI client (make sure OPENAI_API_KEY is set in your environment)


endpoint = "https://orderservicefm.services.ai.azure.com/openai/v1"
api_key = os.environ["AZURE_OPENAI_API_KEY"]

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)


def reconcile():
    # 1. Load CSV
    bank_df = pd.read_csv("bank.csv")

    # 2. Load SQL
    conn = get_db_connection()
    erp_df = pd.read_sql_query("SELECT * FROM Transactions", conn)

    # 3. Merge & detect mismatches
    merged = pd.merge(bank_df, erp_df, on=["TransactionID"], how="outer", suffixes=("_left","_right"), indicator=True)
    mismatches = merged[
    (merged["Amount_left"] != merged["Amount_right"]) |
    (merged["Date_left"] != merged["Date_right"]) |
    (merged["Description_left"] != merged["Description_right"]) |
    (merged["_merge"] != "both")
]


    # 4. Use GPT‑5 to explain mismatches
    
    explanation = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a reconciliation analyst. Provide a mismatch tabular report  with proper reason by analysis the given mismatches for the following columns: "
                "TransactionID,Date,ERP Value,Bank Value,Reason"
                "Rules:"
                "- Do not add extra columns,commentary, explanations, or text outside the table"
            )
        },
        {
            "role": "user",
            "content": f"Explain these mismatches:\n{mismatches.to_string()}"
        }
    ]
)




    

    # 5. Return JSON response
    return {
        "ai_explanation": explanation.choices[0].message.content
    }
