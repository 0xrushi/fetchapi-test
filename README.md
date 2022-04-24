# Fetch Rewards Coding Exercise 
The API is built using the Python language. I am using fastAPI for the Backend API implementation.
### Clone and Install the libraries

```

git clone https://github.com/rushic24/fetchapi-test.git && cd fetchapi-test

pip install -r requirements.txt 

or

pip install pandas fastapi pydantic "uvicorn[standard]"
```

### How to run:

```
uvicorn main:app --reload
```

### Add Points Transaction

POST /add endpoint
```
http://127.0.0.1:8000/add/
```
Payload
```
{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
```

### Spend Points

POST /spend endpoint

```
http://127.0.0.1:8000/spend/
```

Payload

```
{
    "points": 5000
}
```

### Get points balance

GET /pointsbalance

```
http://127.0.0.1:8000/pointsbalance/
```

### Automated DOCS available at [http://localhost:8000/docs](http://localhost:8000/docs)