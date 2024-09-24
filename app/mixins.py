# from django.conf import settings
# from twilio.rest import Client
# # import 


# class MessaHandler:
#     phone_number = None
#     otp = None


#     def __init__(self, phone_number, otp) -> None:
#         self.phone_number = phone_number
#         self.otp=otp

#     def send_opt_on_phone(self):
# ACCOUNT_SID = 'AC0f36c1cb50bae7fabbc54e01dcc27bb7'
# AUTH_TOKEN = '8bf1f913729105d54493577b25ea2257'
#         client = Client(settings.ACCOUNT_SID, AUTH_TOKEN)

#         message = client.messages .create(
#             from_='+15557771212',
#             body='Ahoy! This message was sent from my Twilio phone number!',
#             to='+15559991111'
#         )

# # print(message.body)
