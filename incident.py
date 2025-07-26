import os
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai

# Load environment variables, including GOOGLE_API_KEY
load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Raw GitHub URL of the CSV file
csv_url = "https://github.com/19BCS4520/GENAI-AUTOMATION/raw/3dc4d8bdcc3859697263e646c73f92f7a55a446a/issue.csv"

# Load CSV into pandas DataFrame
df = pd.read_csv(csv_url)

# Iterate through each issue and summarize
for index, row in df.iterrows():
    issue_desc = row['Issue Description']
    explanation = row['Brief Explanation (2–3 Points)']

    prompt = (
        f"Summarize the following production issue in 2-3 sentences as bullet points:\n\n"
        f"Issue Description: {issue_desc}\n\n"
        f"Brief Explanation: {explanation}"
    )

    # Call Gemini API to generate content
    response = model.generate_content(prompt)

    print(f"Summary for Issue #{index + 1}:\n{response.text}\n{'-' * 60}\n")
