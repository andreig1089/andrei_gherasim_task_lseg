# Challenge text
### Challenge 2: Backend – Predict next 3 values of Stock price (timeseries data)

### Objective
For each stock exchange, select the specified number of files, and for each file provided, predict the next 3 values of stock price for that specific file.

### Requirements
Your solution should utilize 2 APIs/Functions
- [ ] 1st API/Function that, for each file provided, returns 10 consecutive data points starting from a random
timestamp.  
- [ ] 2nd API/function that gets the output from 1st one and predicts the next 3 values in the timeseries data.  
#### Data & Inputs
Sample data is provided as a set of folders, one for each exchange, .csv files. Each file has
- Stock-ID, Timestamp (dd-mm-yyyy), stock price value.
Input parameter to your solution: The recommended number of files to be sampled for each Stock Exchange.
Possible input values are 1 or 2. If there aren’t enough files present for a given exchange, process whatever
number of files are present even if it is lower. E.g., input is 2 but only 1 file is present, so you process 1 file.
Prediction Logic: You can write your own prediction algorithm (in such case pls provide the logic and rationale)
or go by below for the sake of simplicity:
- first predicted (n+1) data point is same as the 2nd highest value present in the 10 data points
- n+2 data point has half the difference between n and n +1
- n+3 data point has 1/4th the difference between n+1 and n+2
#### Output Format
One .csv output file for each file processed. Each .csv file should have 3 columns on each row as shown below.
Timestamp & stock price have same format as input file

| Stock-ID | Timestamp | Stock Price |
|----------|-----------|-------------|
| Stock-ID | Timestamp-1 | stock price 1 |
| ...      | ...         | ...         |
| Stock-ID | Timestamp-n | stock price n |
| Stock-ID | Timestamp-n+1 | stock price n+1 |
| Stock-ID | Timestamp-n+2 | stock price n+2 |
| Stock-ID | Timestamp-n+3 | stock price n+3 |

#### Error Handling
The application should gracefully handle exceptions, such as no files,
empty files etc., feel free to include as much exception handling as
possible. It provides insights into your ability to anticipate what can
go wrong.  

#### Documentation
Include a README file explaining how to set up and run your
application.  

#### Optional Enhancements
Feel free to add enhancements that could improve the
extensibility/maintainability for future enhancement, user
experience etc., Some suggestions include:  
• additional functionality or checks (e.g., your own prediction algorithm using AIML etc.)  
• more insights added in the report you generate  
• optimizations for performance and scalability  