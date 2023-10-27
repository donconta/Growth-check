import requests, json, datetime
from key import API_KEY

#oldest year is 1st June 2000
#input the old date
year = "2000"
month = "06"
day = "01"


old_date = f"{year}-{month}-{day}"
old_salary = 1000000
current_date = datetime.date.today()
new_salary = 50000000


def old_calculate_usd_to_ngn_exchange_rate(old_date):
    url = f"http://api.exchangeratesapi.io/v1/{old_date}?access_key={API_KEY}"

    try:
        response = requests.get(url)

        # Get JSON response
        x = response.json()

        # Get the exchange rates
        base_currency = x["base"]
        usd_to_eur_rate = x["rates"]["USD"]
        eur_to_ngn_rate = x["rates"]["NGN"]

        # Calculate the exchange rate from USD to NGN
        usd_to_ngn_rate = usd_to_eur_rate * eur_to_ngn_rate

        return usd_to_ngn_rate
    except Exception as e:
        return f"Error: {e}"

def new_calculate_usd_to_ngn_exchange_rate(current_date):
    url = f"http://api.exchangeratesapi.io/v1/{current_date}?access_key={API_KEY}"

    try:
        response = requests.get(url)

        # Get JSON response
        x = response.json()

        # Get the exchange rates
        base_currency = x["base"]
        usd_to_eur_rate = x["rates"]["USD"]
        eur_to_ngn_rate = x["rates"]["NGN"]

        # Calculate the exchange rate from USD to NGN
        usd_to_ngn_rate = usd_to_eur_rate * eur_to_ngn_rate

        return usd_to_ngn_rate
    except Exception as e:
        return f"Error: {e}"

#calculate the exchange rate for the old date and the current date
old_fx = old_calculate_usd_to_ngn_exchange_rate(old_date)
new_fx = new_calculate_usd_to_ngn_exchange_rate(current_date)

#convert salary to USD
old_salary_in_USD = old_salary / old_fx
new_salary_in_USD = new_salary / new_fx

#calculate percentage changes
def calculate_usd_percentage_change(old_salary_in_USD, new_salary_in_USD):
    usd_percentage_change = ((new_salary_in_USD - old_salary_in_USD) / old_salary_in_USD) * 100
    return usd_percentage_change

usd_salary_percentage_change = calculate_usd_percentage_change(old_salary_in_USD, new_salary_in_USD)

def calculate_ngn_percentage_change(old_salary, new_salary):
    ngn_percentage_change = ((new_salary - old_salary) / old_salary) * 100
    return ngn_percentage_change

ngn_salary_percentage_change = calculate_ngn_percentage_change(old_salary, new_salary)


#conditional statements to determine if the salary is increased or decreased in both currencies
def salary_change(old_salary, new_salary, ngn_salary_percentage_change, usd_salary_percentage_change):
    if new_salary == old_salary:
        return f"""You earn {-usd_salary_percentage_change:.0f}% less today vs {old_date}. 
        This is because the official exchange rate of $/₦ moved from ₦{old_fx:.0f} in {year} to ₦{new_fx:.0f} today. 
        Even though your earnings in Naira never changed, you are actually poorer."""
    elif ngn_salary_percentage_change >= 0 and usd_salary_percentage_change <= 0:
        return f"""You earn {-usd_salary_percentage_change:.0f}% less today vs {old_date}.
                This is because the official exchange rate of $/₦ moved from ₦{old_fx:.0f} in {year} to ₦{new_fx:.0f} today.
                Despite the fact that your earnings in Naira increased by {ngn_salary_percentage_change:.0f}%  you are actually poorer today. """
    elif ngn_salary_percentage_change < 0 and usd_salary_percentage_change < 0:
        return f"""Although your earnings in Naira dropped by {-ngn_salary_percentage_change:.0f}%.
                The change in the official exchange rate of $/₦ from ₦{old_fx:.0f} in {year} to ₦{new_fx:.0f} today has made you poorer by {-usd_salary_percentage_change:.0f}%."""
    elif ngn_salary_percentage_change >= 0 and usd_salary_percentage_change >= 0:
        return f"""Congratulations!!! 
                You are one of the few Nigerians whose salary has increased in both Naira and Dollar values despite the change in the official exchange rate from ₦{old_fx:.0f} in {year} to ₦{new_fx:.0f} today.
                Your earnings increased by {ngn_salary_percentage_change:.0f}% in Naira and {usd_salary_percentage_change:.0f}% in Dollars."""
    else:
        return "no change"

print(salary_change(old_salary, new_salary, ngn_salary_percentage_change, usd_salary_percentage_change))