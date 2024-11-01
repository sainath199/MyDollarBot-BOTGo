# TrackMyDollar API Documentation

## Overview
The TrackMyDollar API enables developers to integrate expense and income tracking features into their own applications. Using this API, you can programmatically add expenses, track income, manage categories, and generate financial summaries.

This document provides details on all available endpoints, request formats, and example usage.

---


---

### Authentication
Each request to the TrackMyDollar API must include an API key. This key is generated for each registered user and should be passed as a header in the following format:

```plaintext
Authorization: Bearer <your_api_key>
```

### Endpoints
#### 1. Add Expense
   
- Endpoint: /api/expense
- Method: POST
- Description: Adds a new expense to the user’s account.
- Request Body
```
{
  "amount": 50.0,
  "currency": "USD",
  "category": "Food",
  "description": "Lunch at cafe",
  "date": "2024-01-15"
}

```
Response:

```
{
  "status": "success",
  "message": "Expense added successfully",
  "expense_id": "12345"
}

```

Example:
```
curl -X POST https://api.trackmydollar.com/api/expense \
     -H "Authorization: Bearer <your_api_key>" \
     -H "Content-Type: application/json" \
     -d '{
          "amount": 50.0,
          "currency": "USD",
          "category": "Food",
          "description": "Lunch at cafe",
          "date": "2024-01-15"
        }'
```

Here's the API documentation in Markdown format for your README.md or as a separate file, such as API.md:

markdown
Copy code
# TrackMyDollar API Documentation

## Overview
The TrackMyDollar API enables developers to integrate expense and income tracking features into their own applications. Using this API, you can programmatically add expenses, track income, manage categories, and generate financial summaries.

This document provides details on all available endpoints, request formats, and example usage.

---

## Base URL
For this example, we assume the API is hosted at `https://api.trackmydollar.com/`.

---

### Authentication
Each request to the TrackMyDollar API must include an API key. This key is generated for each registered user and should be passed as a header in the following format:

```plaintext
Authorization: Bearer <your_api_key>
Endpoints
1. Add Expense
Endpoint: /api/expense
Method: POST
Description: Adds a new expense to the user’s account.
Request Body:
json
Copy code
{
  "amount": 50.0,
  "currency": "USD",
  "category": "Food",
  "description": "Lunch at cafe",
  "date": "2024-01-15"
}
Response:
json
Copy code
{
  "status": "success",
  "message": "Expense added successfully",
  "expense_id": "12345"
}
Example:
bash
Copy code
curl -X POST https://api.trackmydollar.com/api/expense \
     -H "Authorization: Bearer <your_api_key>" \
     -H "Content-Type: application/json" \
     -d '{
          "amount": 50.0,
          "currency": "USD",
          "category": "Food",
          "description": "Lunch at cafe",
          "date": "2024-01-15"
        }'
```
#### 2. Add Income
- Endpoint: /api/income
- Method: POST
- Description: Adds a new income entry.
- Request Body
```
{
  "amount": 2000.0,
  "currency": "USD",
  "source": "Salary",
  "date": "2024-01-01"
}
```
Response:
```
{
  "status": "success",
  "message": "Income added successfully",
  "income_id": "67890"
}
```

#### 3. Get Expense Summary
- Endpoint: /api/summary/expenses
- Method: GET
- Description: Retrieves a summary of expenses for a specified period.
- Query Parameters:
  - start_date: Start date for the summary (format: YYYY-MM-DD).
   - end_date: End date for the summary (format: YYYY-MM-DD).
- Example Request

```
GET /api/summary/expenses?start_date=2024-01-01&end_date=2024-01-31
```

Response:
```
{
  "status": "success",
  "total": 500.0,
  "currency": "USD",
  "breakdown": [
    {
      "category": "Food",
      "amount": 200.0
    },
    {
      "category": "Transport",
      "amount": 100.0
    }
  ]
}

```
#### 4. Get Income Summary
- Endpoint: /api/summary/income
- Method: GET
- Description: Retrieves a summary of income for a specified period.
- Query Parameters:
  - start_date: Start date for the summary (format: YYYY-MM-DD).
  - end_date: End date for the summary (format: YYYY-MM-DD).
Example Request:
```
GET /api/summary/income?start_date=2024-01-01&end_date=2024-01-31

```
Response:
```
{
  "status": "success",
  "total_income": 3000.0,
  "currency": "USD",
  "sources": [
    {
      "source": "Salary",
      "amount": 2000.0
    },
    {
      "source": "Freelance",
      "amount": 1000.0
    }
  ]
}

```

#### 5. Get Budget and Spending Comparison
- Endpoint: /api/summary/budget
- Method: GET
- Description: Compares user’s spending against their set budget.
- Query Parameters:
  - period: Desired period (e.g., monthly, yearly).
- Response:
  ```
{
  "status": "success",
  "budget": 1000.0,
  "total_spent": 800.0,
  "remaining_budget": 200.0
}

  ```
