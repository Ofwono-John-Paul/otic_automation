import phonenumbers
from phonenumbers import geocoder

phone_number1 = phonenumbers.parse("+256706647669")
phone_number2 = phonenumbers.parse("+256758324842")
phone_number3 = phonenumbers.parse("+918878586271")
phone_number4 = phonenumbers.parse("+971551830825")

print("\nPhone Numbers Location")
print(geocoder.description_for_number(phone_number1, "en"))
print(geocoder.description_for_number(phone_number2, "en"))
print(geocoder.description_for_number(phone_number3, "en"))
print(geocoder.description_for_number(phone_number4, "en"))