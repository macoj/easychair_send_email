# easychair_send_email
Simple script for spamming about a conference or similar.



#Usage:
```bash
$ send_email.py message.txt recipient.csv sender@email.com "subject" delay batch_size
```
The script will send ```message.txt``` as the content of  ```batch_size``` e-mails every ```delay``` seconds using the list of recipients in ```recipient.csv``` (you need to include a header ```email```). 

Optionally you can add columns in ```recipient.csv``` for personalizing the message. For instance, if there is a column named ```$NAME$```, every occurrence of ```$NAME$``` in ```message.txt``` will be replaced by the value for this column in ```recipient.csv``` of a particular row (recipient).
