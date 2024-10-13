
# Fetch Backend Assignment 2024

  

This project implements an API for managing user points based on transactions from different payers. It supports adding points, spending points, and checking a user's balance. The program uses Flask to serve the API and TinyDB as a local NoSQL database to store transaction data.

  

## Features

-  **Add points** to a user's account from various payers.

-  **Spend points** based on a user's current point balance, starting from the oldest transactions.

-  **View user balance** per payer to track the current points status.

  


## Prerequisites To run this program, you need the following: 

### 1. Install Python If Python is not installed, follow these steps: 
- **Windows**: 
1. Download the latest version of Python from [python.org](https://www.python.org/downloads/). 
2. Run the installer and make sure to check the box **"Add Python to PATH"** before clicking "Install". 
3. Once installed, open Command Prompt and type: ```bash python --version ``` 
This should return the installed version of Python. 
- **macOS**: 
1. Open Terminal. 
2. Use Homebrew to install Python (if Homebrew is not installed, you can install it from [brew.sh](https://brew.sh/)): ```bash brew install python ``` 
3. Verify the installation: ```bash python3 --version ``` 

- **Linux**: 
1. Open your terminal. 
2. Use the package manager specific to your distribution to install Python: 
`bash sudo apt-get install python3 # Debian/Ubuntu`
`sudo yum install python3 # CentOS/RHEL ` 
3. Verify the installation: ```bash python3 --version ``` 

### 2. Install Required Libraries Install the necessary Python libraries: 
`pip install Flask TinyDB`

## How  to  Run

Clone  this  repository  or  copy  the  code  into  a  new  Python  file (e.g., app.py).
`git clone https://github.com/abhinandan-SS25/be_fetch2024`

Run  the  application:  Navigate  to  the  folder  containing  the  Python  file  and  execute:
`python app.py`

This  will  start  the  Flask  server  on  localhost  port  `8000`.

## Using  the  API:  You  can  interact  with  the  API  using  tools  like  Postman  or  cURL.

API  Endpoints

1.  Add  Points (/add -  POST)
Adds  points  from  a  payer  to  a  user's account
- Endpoint: /add
- Method: POST
- Example Request Body:
`{
"payer": "DANNON",
"points": 1000,
"timestamp": "2024-10-10T10:00:00Z"
}`
- Response: HTTP 200 on success, HTTP 400 if required fields are missing or negative points greater than balance for the given payer and can't  be  added.

2.  Spend  Points (/spend -  POST)
Spend  a  specified  amount  of  points  from  a  user's account starting from the oldest transactions. 
- Endpoint: /spend
- Method: POST
- Example Request Body:
`{
"points": 5000
}`
- Response: A list showing points deducted from each payer:
`[
{ "payer": "DANNON", "points": -1000 },
{ "payer": "UNILEVER", "points": -3000 },
{ "payer": "MILLER COORS", "points": -1000 }
]`

3. Get Balance (/balance - GET)
Retrieve the current balance for each payer in the user's  account.
- Endpoint:  /balance
- Method:  GET
- Response:
`{
"DANNON":  1000,
"UNILEVER":  0,
"MILLER COORS":  5300
}`

## Notes

The  program  uses  a  generic  user_id (x01) for simplicity.
TinyDB  is  used  to  simulate  a  NoSQL  database  that  tracks  the  transactions  and  balances.

## Troubleshooting

Ensure  that  the  server  is  running  on  `localhost:8000`  and  that  you  are  making  requests  to  the  correct  endpoints.