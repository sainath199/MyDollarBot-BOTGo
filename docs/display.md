# About MyDollarBot's /display Feature

![Income Tracking](display.png)
This feature enables the user to view their expenses for the past month or past day. The option to choose month or day pops up on the screen and they can choose their preference to be displayed afterwards.

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/prithvish-doshi-17/MyDollarBot-BOTGo/blob/main/code/display.py)

# Code Description
## Functions

1. run(message, bot):
This is the main function used to implement the delete feature. It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the main code.py function. 

It gets the options for the display period from the helper.py file's getSpendDisplayOptions() method and then makes the Telegram bot display them for the user to choose along with a message indicating this. It then passes control to the display_total() function for further processing.

2. display_total(message, bot):
It takes 2 arguments for processing - **message** which is the message from the user, and **bot** which is the telegram bot object from the  run(message, bot): function in the same file. This function loads the user's data using the helper file's getUserHistory(chat_id) method. After this, depending on the option user has chosen on the UI, it calls the  calculate_spendings(queryResult): to process the queried data to return to the user after which it finally passes the data to the UI for the user to view.

3. calculate_spendings(queryResult):
Takes 1 argument for processing - **queryResult** which is the query result from the display total function in the same file. It parses the query result and turns it into a form suitable for display on the UI by the user.

4. display_budget_by_text(history, budget_data) -> str:
It takes 2 arguments for processing - **history** which is the history expense of a user, and **budget_data** is the budget setting of a user. It collects the budget setting and calculates the remaining budget so far.

# How to run this feature?
Sri Athithya Kruth, [20.10.21 20:33]
/display

mydollarbot20102021, [20.10.21 20:33]
[In reply to Sri Athithya Kruth]
Please select a category to see the total expense

Sri Athithya Kruth, [20.10.21 20:33]
Day

mydollarbot20102021, [20.10.21 20:33]
Hold on! Calculating...

mydollarbot20102021, [20.10.21 20:33]

Here are your total spendings day:

CATEGORIES,AMOUNT 
----------------------
Transport $1022.0
Groceries $12.0
