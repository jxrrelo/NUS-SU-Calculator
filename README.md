# NUS-SU-Calculator
In view of the COVID 19 situation, NUS has granted 10 additional MCs worth of S/U and lifted most of the S/U restrictions for students. NUS-SU-Calculator is a telegram bot specially built for AY19/20 Semester 2. It provides a guide on which modules to S/U in order to maximise one's CAP. The bot is stable, fast and accurate. It is officially pushed out for use on 24/05/2020 and has received an overwhelming 1000+ users till date. Bot address: https://t.me/nusacadplan_bot
<<<<<<< HEAD

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
<<<<<<< HEAD
=======
>>>>>>> aaa96ae6a045fcde34d0449080b00fc225bd6547
=======
>>>>>>> f2d8eb4d89f0f3d2296cc47a1bfc3cae034ed37d
