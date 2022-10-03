# Introduction
Forms to record spendings. 

# Data Model

We capture below kind of data. Data model is ```SQLAlchemy``` ```Model``` defined in ```models.py```

- Spending name ```name``` of stype ```String```
- Spending date ```spent_at``` of type ```DateTime``` with default value of ```datetime.datetime.now```
- Spending amount ```amount``` of type ```Integer```
- Spending category ```category_id``` is a foreign key to ```SpendingCategory``` table
- Payment method ```payment_method_id``` is a foreign key to ```PaymentMethod```
- Created date DateTime
- Modified datetime

