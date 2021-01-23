# NUS-SU-Calculator
NUS-SU-Calculator is a telegram bot specially built for AY19/20 Semester 2. It provides a guide on which modules to S/U in order to maximise one's CAP. The bot is stable, fast and accurate. It is officially pushed out for use on 24/05/2020 and has received an overwhelming 10000+ users till date. Bot address: https://t.me/nusacadplan_bot

## Installation
```bash
pip install logging
pip install inflect
pip install telegram
```

## Usage
```python
import logging
import inflect
import os
import telegram

PORT = int(os.environ.get('PORT', < Port Number > ))
bot = telegram.Bot(token= < API Key >)

updater = Updater(
        < API Key > , use_context=True)
      
#For webhook
updater.start_webhook(listen= < Listen Address >,
                          port=int(PORT),
                          url_path= < API Key >)

updater.bot.setWebhook( < Server Name > +
                           < API Key > )
```
