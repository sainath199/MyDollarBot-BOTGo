# 💰 TrackMyDollar V5.0 - Budget On The Go(BOTGo) 💰

[YOUTUBE](https://youtu.be/h11X3BS5dg0?si=Zv__BysvKomxM2hD)

This video shows only the new features and enhancement of some older features. All the other features from phase 4 are working as it is.
<hr>
<p align="center">
<a><img  height=360 width=550 
  src="https://github.com/sainath199/MyDollarBot-BOTGo/blob/main/docs/trackmydollar.png" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/anuj672/MyDollarBot-BOTGo)](https://github.com/anuj672/MyDollarBot-BOTGo/graphs/contributors)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10023576.svg)](https://doi.org/10.5281/zenodo.10023576)
[![Test and Formatting](https://github.com/anuj672/MyDollarBot-BOTGo/actions/workflows/test.yml/badge.svg)](https://github.com/anuj672/MyDollarBot-BOTGo/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/f90d8ff63781978b73c28561177358b3/raw/coverage.json)](https://github.com/sainath199/MyDollarBot-BOTGo/actions/workflows/test.yml)
[![Static Code Analysis](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/6e6740fb4d21afa29af5a1eba71cedba/raw/Static_code_analysis.json)](https://github.com/sainath199/MyDollarBot-BOTGo/actions/workflows/test.yml)
[![Security Scans](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/e9d969e042f2cc3e639dbac2a074ba92/raw/Security_scan.json)](https://github.com/sainath199/MyDollarBot-BOTGo/actions/workflows/test.yml)


<!-- [![codecov](https://codecov.io/gh/sak007/MyDollarBot-BOTGo/branch/main/graph/badge.svg?token=5AYMR8MNMP)](https://codecov.io/gh/sak007/MyDollarBot-BOTGo) -->
[![GitHub issues](https://img.shields.io/github/issues/sainath199/MyDollarBot-BOTGo)](https://github.com/sainath199/MyDollarBot-BOTGo/issues)
![Fork](https://img.shields.io/github/forks/anuj672/MyDollarBot-BOTGo)

<hr>

## About TrackMyDollar

TrackMyDollar is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle 
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to
- Add a recurring expense 
- User can add a new category and delete an existing category 
- User can see the budget value for the total expense 
- Added pie charts, bar graphs with and without budget lines 
- Deployment on GCP 

## What's new? (From Phase 4 to Phase 5)

- Calendar Feature: Allows users to select dates for their transactions directly via a calendar interface.
- Income Feature: Tracks income in addition to expenses, allowing better financial planning.
- Multi-Currency Feature: Supports tracking expenses and income in different currencies.
- Improved Test Cases and new badges: Added more robust test cases for increased coverage and Added badges for coverage, static code analysis and Security scans.
- Automated Static Code Analysis & Security Scans: Integrates automatic static code analysis and security scans with GitHub Actions, ensuring code quality.


## What more can be done?
Check out the issue list [here](https://github.com/sainath199/MyDollarBot-BOTGo/issues) to see what more can be done to make MyDollarBot better. 

## Demo

https://user-images.githubusercontent.com/72677919/140454147-f879010a-173b-47b9-9cfb-a389171924de.mp4

## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. Clone this repository to your local system.

2. Start a terminal session in the directory where the project has been cloned. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```

3. In Telegram, search for "BotFather". Click on "Start", and enter the following command:
```
  /newbot
```
Follow the instructions on screen and choose a name for your bot. After this, select a username for your bot that ends with "bot".

4. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy and save this token for future use.

5. Copy the token provided by the bot and add/replace it in the user.properties file (in the format api_token=<your_token>).

6. In the directory where this repo has been cloned, please run the below command to execute a bash script to run the Telegram Bot:
```
   ./run.sh
```
(OR)
```
   bash run.sh
```

(Please Note: You may require to run `chmod +x run.sh` on mac/linux)

A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

7. In the Telegram app, search for your newly created bot by entering the username and open the same. Now, on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!

## Testing

We use pytest to perform testing on all unit tests together. The command needs to be run from the home directory of the project. The command is:
```
python -m pytest test/
```

## Code Coverage

Code coverage is part of the build. Every time new code is pushed to the repository, the build is run, and along with it, code coverage is computed. This can be viewed by selecting the build, and then choosing the codecov pop-up on hover.

Locally, we use the coverage package in python for code coverage. The commands to check code coverage in python are as follows:

```
coverage run -m pytest test/
coverage report
```

Please note: A coverage below 80% will cause the build to fail.

## Notes:
You can download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

## Authors (Iteration 5)
- Sainath Gorige
- Mona Sree Muppala
- Vishal Reddy Devireddy
  
<hr>
<p>Title:'Track My Dollar'</p>
<p>Version: '4.2'</p>
<p>Description: 'An easy to use Telegram Bot to track everyday expenses'</p>
<p>Authors(Iteration 4):'Anuj, Bhavesh, Jash, Vaibhavi'</p>
<p>Authors(Iteration 3):'Vraj, Alex, Leo, Prithvish, Seeya'</p>
<p>Authors(Iteration 2):'Athithya, Subramanian, Ashok, Zunaid, Rithik'</p>
<p>Authors(Iteration 1):'Dev, Prakruthi, Radhika, Rohan, Sunidhi'</p>
