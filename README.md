Architecture:

```
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
```


Setup and Usage Instructions:

Background:
The company is called "Northstar Services". The information below is all hypothetical and not real. 

Data sources

Documents:
There are 3 documents that were ingested into the agent. 
    1. Northstar Services Customer complaint policy
    2. Northstar Services Employee complaint policy
    3. An employee Human Resources report

The documents must be ingested by running the ingest.py script. This script chunks the documents into information for the qualitative agent. 


SQL Table:
The table is generated from the script "setup_database.py" and contains information about employees, customers, and sales. This is what the quantitative agent reads. 

Testing:

test_qual and test_quant were both testing scripts to confirm that the script was able to connect to Gemini and successfully query information.


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

    1. What is the Northstar Services Promotion Policy? (Qualitative)
    2. Gemini returned that it was unable to find the information in the provided documents. 
    3. The validation successfully flagged that there is no promotion policy in the documents, and returned the appropriate answer.
    4. I accepted this answer. I asked a question that I knew was not possible for Gemini to answer in order to see the output that it returned, and it 
    returned the proper response of the information not being found.

Query 4

    1. Who submitted the workplace complaint, and what is our average employee satisfaction score and what was the lowest? (Both)
    2. Gemini was able to return the proper answers. 
        For the qualitative portion, it provided who submitted the workplace complaint (employee 4), and said that it did not have the average 
        employee satisfaction score in the documents. 

        For the quantitative portion, it only calculated the average satifaction score as a 4.3. 
    3. The validation layer flagged that it did not have access to the average satisfaction score in the documents and did not calculate a score. 
    4. I do like these answers. It was able to successfully flag where the answers were not available.

Query 5

    1. Analyze our average employee satifaction score and their revenue. Is there a connection? (Quantitative)
    2. Gemini was able to return the average satisfaction scores as well are there revenue. It was also able to analyze the output, and provide 
        an analysis of the results. What it said is below:

     **The Revenue Trend:** Generally, as the employee satisfaction score decreases, the total revenue generated also decreases. For example, the highest satisfaction score (4.7) generated the highest revenue ($143,500), while the lowest satisfaction score in the dataset (3.9) generated the lowest revenue ($76,500).
     **Top Performers:** Employees with satisfaction scores of 4.4 and above consistently generated higher revenues, typically exceeding $98,000.
     **Exceptions to Note:** While the overall trend shows higher satisfaction linked to higher revenue, individual performance can vary based on department or tenure. Forinstance, Employee #6 (Audit) has a relatively high satisfaction score (4.3) but generated the second-lowest revenue ($42,000), suggesting that revenue generation potential also depends heavily on the specific role or department rather than satisfaction alone.

    3. The validation layer did not flag anything. 
    4. This answer was good for me. It was able to analyze the data and provide an output that I thought made sense. 

Query 6

    1. What is our employee complaint policy, and which employee submitted the report? (both)
    2. Gemini returned both a qualitative and a quantitative result, which is not what I really wanted. It was able to successfully reply to the complaint policy
    and who submitted the report, but it should not have gone looking in the database.
    3. The validation for the SQL worked since it thought the question wasn't a select statement. 
    4. I was ok with the output.
    5. I did not trust the fact that it tried to find an answer in the database since there was no mathetmatical component to the question. In order to resolve this, I went to change the definition of the classify function in the manager.py script. I expanded it to be more comprehensive, and upon running this query again, it correctly categorized it as qualitative. I did realize this change made it so that prompts must be specific with what they are asking for. Prior, I could be relatively loose with some prompts and it would occasionally interpret it correctly, but now it is better to be precise. 


Query 7

    1. Insert a company called Jonah company into the database
    2. Gemini blocked the query since it was an insert and failed the validation.
    3. The validation worked as intended and failed the prompt so the user could not insert new rows into the database. 
    4. I accepted this result. I had to go into manager.py file and update some of the quantitative categorization logic since it kept thinking
    that "UPDATE" was qualitative. 









