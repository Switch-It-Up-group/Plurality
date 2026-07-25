import keyring
from plurality.core.updates.discord import webhook

webhook(keyring.get_password("plurality", "discord_webhook"),"Alastor", "He/Him", "Plurality test", "This is just a test of the front informing system")