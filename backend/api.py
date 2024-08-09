import requests
from typing import List,Dict
def get_random_users(number_of_users: int) -> List[Dict]:
    url = f"https://randomuser.me/api/?results={number_of_users}"
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return data['results']
