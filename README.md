# BlackBoard Online Class Attender Bot

This bot attends the online classes held on BlackBoard, according to the given timetable using selenium and python3.

## Configure

There are few things you need to configure before running this bot.

- create .env, and put your blackboard credentials in the repective field.
- Example - `EMAIL=YourEmailHere PASSWORD=YourPasswordHere`
- Also add your discord webhook url in the .env file. Go to your discord server > Server Settings > Integrations > View Webhooks > New Webhook to get your webhook url.
- Example - `webhook_url = "https://discordapp.com/...."`
- Make sure that the timezone of the PC is correct. If you're running the bot on cloud, you may want to manually change the timezone of the virtual machine to an appropriate time zone (i.e., the timezone that your online classes follow)

## Install

- Clone the repository `git clone https://github.com/namankhare/blackboard-automatic-online-class-attender.git`
- Install requirements.txt `pip install -r requirements.txt`

## Run the bot

- Run the bot `python bot.py`

Written on Python3.

- Project is open to contribution.
