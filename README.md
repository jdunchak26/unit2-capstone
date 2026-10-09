Architecture:

User Query (CLI)
      │
      ▼
┌─────────────────┐
│  Manager Agent  │  ── classifies query ──► qualitative / quantitative / both
└─────────────────┘
      │                          │
      ▼                          ▼
┌──────────────────┐    ┌───────────────────┐
│ Qualitative Agent│    │ Quantitative Agent │
│                  │    │                   │
│ • Vector DB      │    │ • SQLite DB        │
│   (ChromaDB)     │    │ • NL → SQL         │
│ • Semantic search│    │ • Query execution  │
│ • Claude for     │    │ • Claude for       │
│   generation     │    │   interpretation   │
└──────────────────┘    └───────────────────┘
      │                          │
      └──────────┬───────────────┘
                 ▼
      ┌─────────────────────┐
      │  Validation Layer   │  ── checks grounding, flags issues
      └─────────────────────┘
                 │
                 ▼
      ┌─────────────────────┐
      │  Tokenomics Logger  │  ── logs token usage and cost per query
      └─────────────────────┘
                 │
                 ▼
        Response to User


Setup and Usage Instructions:

Background:
The company is called "Northstar Services". The information below is all hypothetical and not real. 

Data sources

Documents:
There are 4 documents that were ingested into the agent. 
    1. A consulting report for the hyptohetical client "Meridian Home Products"
    2. Northstar Services Customer complaint policy
    3. Northstar Services Employee complaint policy
    4. An employee Human Resources report

SQL Table:
The table is generated from the script "setup_database.py" and contains information about employees, customers, and other stuff. 


Trust-but-verify

Query 1

    1. What is Northstar Services customer complaint policy? (Qualitative)
    2. Gemini returned the customer complaint policy, almost verbatim from the customer_complaint_policy.txt file
    3. The validation layer did not flag anything. 
    4. I accepted this result. I did not ask Gemini to summarize the complaint policy, so it returned what I asked for and upon examiniation it matched what was said in the actually text file.

Query 2

    1. What is the average revenue per employee? (Quantative)
    2. Gemini returned the amount of tokens used, the actual SQL query, and the answer to the question, which was $228,666.67.
    SQL used: SELECT 
    (SELECT SUM(revenue) FROM sales) / (SELECT COUNT(*) FROM employees) AS avg_revenue_by_employee;
    3. The validation layer did not flag anything, but I was also not trying to purposefully break it. 
    4. I accepted this result. I looked at the SQL code and using my prior knwoledge understood what it was querying. 

Query 3

    1. Insert a new company called Jonah Company into the database (Quantative)
    2. Gemini blocked the result due the validation layer flagging this as a blocked query.
    3. The validation layer flagged this as the user attempting to insert a new row into the customers table. In the validation guidelines, the SQL INSERT function is blocked, which this successfully recognized and blocked. 
    4. I was ok with this result. It blocked the query as expected. 

Query 4

    1. What is the Northstar Services Promotion Policy? (Qualitative)
    2. Gemini returned that it was unable to find the information in the provided documents. 
    3. The validation successfully flagged that there is no promotion policy in the documents, and returned the appropriate answer.
    4. I accepted this answer. I asked a question that I knew was not possible for Gemini to answer in order to see the output that it returned, and it 
    returned the proper response of the information not being found.

Query 5

    1. Who submitted the workplace complaint, and what is our average employee satisfaction score and who was the lowest? (Both)
    2. Gemini was able to return the proper answers. 
        For the qualitative portion, it provided who submitted the workplace complaint (employee 4), and said that it did not have the average 
        employee satisfaction score in the documents. 

        For the quantitative portion, it only calculated the average satifaction score as a 4.3. 
    3. The validation layer flagged that it did not have access to the average satisfaction score in the documents and did not calculate a score. 
    4. I do like these answers. It was able to successfully flag where the answers were not available.

Query 6

    1. Analyze our employee satifaction score and their revenue. Is there a connection? (Quantitative)
    2. Gemini was able to return the average satisfaction scores as well are there revenue. It was also able to analyze the output, and provide 
        an analysis of the results. What it said is below:

     **The Revenue Trend:** Generally, as the employee satisfaction score decreases, the total revenue generated also decreases. For example, the highest satisfaction score (4.7) generated the highest revenue ($143,500), while the lowest satisfaction score in the dataset (3.9) generated the lowest revenue ($76,500).
     **Top Performers:** Employees with satisfaction scores of 4.4 and above consistently generated higher revenues, typically exceeding $98,000.
     **Exceptions to Note:** While the overall trend shows higher satisfaction linked to higher revenue, individual performance can vary based on department or tenure. Forinstance, Employee #6 (Audit) has a relatively high satisfaction score (4.3) but generated the second-lowest revenue ($42,000), suggesting that revenue generation potential also depends heavily on the specific role or department rather than satisfaction alone.

    3. The validation layer did not flag anything. 
    4. This answer was good for me. It was able to analyze the data and provide an output that I thought made sense. 





