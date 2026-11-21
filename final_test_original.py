
FINAL_TESTS = [

    # ACCOUNT (3 tickets)
    ("I am unable to login to my account even after entering the correct password.", "ACCOUNT", "MEDIUM"),
    ("Bhai password reset ka link send kar do, account open nahi ho raha.", "ACCOUNT", "MEDIUM"),
    ("Someone changed my account password without my permission. Please help immediately!", "ACCOUNT", "HIGH"),

    # CANCEL (3 tickets)
    ("I want to cancel my order because I accidentally selected the wrong product.", "CANCEL", "LOW"),
    ("Please cancel my subscription before the next billing cycle. I don't want to pay again.", "CANCEL", "MEDIUM"),
    ("I have contacted support twice to cancel my order but nobody has responded. This is really frustrating.", "CANCEL", "MEDIUM"),

    # CONTACT (3 tickets)
    ("Can you please share your customer support helpline number?", "CONTACT", "LOW"),
    ("Kisi real person se baat karni hai, chatbot meri problem solve nahi kar raha.", "CONTACT", "MEDIUM"),
    ("I have been trying to contact your support team since yesterday regarding my lost money, but nobody is answering.", "CONTACT", "HIGH"),

    # DELIVERY (3 tickets)
    ("My package was supposed to arrive yesterday but it has still not been delivered.", "DELIVERY", "MEDIUM"),
    ("Delivery wala abhi tak nahi aaya, tracking mein bhi koi update nahi hai.", "DELIVERY", "MEDIUM"),
    ("Can you tell me how many days standard delivery usually takes?", "DELIVERY", "LOW"),

    # FEEDBACK (3 tickets)
    ("The customer service representative was very helpful and resolved my issue quickly.", "FEEDBACK", "LOW"),
    ("Your product quality is pathetic and the customer support team is even worse. Not happy at all.", "FEEDBACK", "MEDIUM"),
    ("I really liked the service, but the delivery experience could have been better.", "FEEDBACK", "LOW"),

    # INVOICE (3 tickets)
    ("I downloaded my invoice but the GST number is missing from it.", "INVOICE", "MEDIUM"),
    ("Mujhe last month's bill chahiye, please email kar do.", "INVOICE", "LOW"),
    ("The invoice amount is different from the amount I was charged. Please check this urgently.", "INVOICE", "MEDIUM"),

    # ORDER (3 tickets)
    ("I want to know the current status of my order number 45821.", "ORDER", "LOW"),
    ("I placed an order for two items but received only one. What should I do?", "ORDER", "MEDIUM"),
    ("Please change the delivery address of my order. I entered the wrong address by mistake.", "ORDER", "MEDIUM"),

    # PAYMENT (3 tickets)
    ("My payment failed but the amount has been deducted from my bank account.", "PAYMENT", "HIGH"),
    ("UPI se payment kiya tha but app mein abhi bhi pending show ho raha hai.", "PAYMENT", "MEDIUM"),
    ("Which payment methods do you accept on your website?", "PAYMENT", "LOW"),

    # REFUND (3 tickets)
    ("I returned my product five days ago but haven't received my refund yet.", "REFUND", "MEDIUM"),
    ("Mera paisa abhi tak refund nahi hua, please kuch update do.", "REFUND", "MEDIUM"),
    ("I was charged twice for the same order and need the extra amount refunded immediately.", "REFUND", "HIGH"),

    # SHIPPING (3 tickets)
    ("I entered an incorrect shipping address. Can I update it before dispatch?", "SHIPPING", "MEDIUM"),
    ("Why are you charging so much for shipping when my order value is already high?", "SHIPPING", "LOW"),
    ("The package was sent to my old address even though I updated my shipping details. Please resolve this.", "SHIPPING", "MEDIUM"),

    # SUBSCRIPTION (3 tickets)
    ("How can I unsubscribe from your weekly newsletter?", "SUBSCRIPTION", "LOW"),
    ("I cancelled my membership last month but you are still charging me every month.", "SUBSCRIPTION", "HIGH"),
    ("Can I change my current subscription plan to the premium one?", "SUBSCRIPTION", "LOW"),

]
