
HOLDOUT_TESTS = [

    # ACCOUNT
    ("I keep getting logged out whenever I try to access my profile. Can you fix this?", "ACCOUNT", "MEDIUM"),
    ("Someone is trying to access my account from an unknown device. Please secure it!", "ACCOUNT", "HIGH"),

    # CANCEL
    ("I changed my mind about purchasing this item. Is it possible to stop the order?", "CANCEL", "LOW"),

    # CONTACT
    ("Your automated replies are not helping. I need to speak with an actual support agent.", "CONTACT", "MEDIUM"),

    # DELIVERY
    ("The delivery status says delivered but nothing has arrived at my doorstep.", "DELIVERY", "MEDIUM"),
    ("Bhai parcel kab tak aayega? Tracking pichle 2 din se same hi hai.", "DELIVERY", "MEDIUM"),

    # FEEDBACK
    ("Just wanted to appreciate your team for handling my complaint so patiently. Great experience!", "FEEDBACK", "LOW"),

    # INVOICE
    ("Could you provide a tax invoice for my recent purchase? I need it for reimbursement.", "INVOICE", "LOW"),

    # ORDER
    ("I received the wrong colour of the product. I had ordered the black one.", "ORDER", "MEDIUM"),
    ("Can I add one more item to an order that I placed this morning?", "ORDER", "LOW"),

    # PAYMENT
    ("The checkout page froze after I entered my card details. I am not sure whether the transaction went through.", "PAYMENT", "MEDIUM"),
    ("My card was charged three times for one purchase. Please look into this immediately.", "PAYMENT", "HIGH"),

    # REFUND
    ("I returned the shoes last week and the refund is still not credited to my account.", "REFUND", "MEDIUM"),

    # SHIPPING
    ("I need to update the flat number in my shipping address before the package is dispatched.", "SHIPPING", "MEDIUM"),

    # SUBSCRIPTION
    ("I keep receiving promotional emails even though I unsubscribed. Please stop sending them.", "SUBSCRIPTION", "LOW"),

]
