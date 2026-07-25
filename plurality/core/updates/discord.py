import requests


def webhook(url, name, pronouns, title, description):
    WEBHOOK_URL = url

    payload = {
        "username": "Plurality",
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": 0xFF4500,
                "fields": [
                    {
                        "name": "Name",
                        "value": name,
                        "inline": True
                    },
                    {
                        "name": "Pronouns",
                        "value": pronouns,
                        "inline": True
                    }
                ]
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    print(response.status_code)
    return response