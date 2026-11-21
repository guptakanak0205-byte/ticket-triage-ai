# Label changes

My first labels used everyday meaning. The training dataset defines categories more
narrowly (CANCEL = cancellation-fee questions, cancelling an order = ORDER, changing an
address = SHIPPING). I corrected 4 labels to match the system's category definitions.
This corrects the measurement. It is not a model improvement.
The original test set is kept in final_test_original.py.

| Ticket (start) | Old | New |
|---|---|---|
| I want to cancel my order because I accidentally... | CANCEL | ORDER |
| Please cancel my subscription before the next billing... | CANCEL | SUBSCRIPTION |
| I have contacted support twice to cancel my order... | CANCEL | ORDER (also a multi-issue ticket) |
| Please change the delivery address of my order... | ORDER | SHIPPING |
