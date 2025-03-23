import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class TwitterRotator:
    def __init__(self):
        self.configs = self._load_configs()
        self.current_index = 0

    def _load_configs(self) -> List[Dict]:
        """Φορτώνει όλες τις διαμορφώσεις από το .env αρχείο."""
        configs = []
        for i in range(1, 12):  # Για 11 API keys
            config = {
                "headers": {
                    "API-Key": os.getenv(f"TWITTER_API_KEY_{i}"),
                    "API-Secret": os.getenv(f"TWITTER_API_SECRET_{i}"),
                    "Authorization": f"Bearer {os.getenv(f'TWITTER_BEARER_TOKEN_{i}')}",
                },
                "auth": {
                    "access_token": os.getenv(f"TWITTER_ACCESS_TOKEN_{i}"),
                    "access_token_secret": os.getenv(f"TWITTER_ACCESS_TOKEN_SECRET_{i}"),
                },
                "proxy": os.getenv(f"PROXY_{i}") if i != 11 else None,  # Το 11ο API δεν χρησιμοποιεί proxy
            }
            configs.append(config)
        return configs

    def get_next(self) -> Dict:
        """Επιστρέφει την επόμενη διαμόρφωση από τη λίστα."""
        config = self.configs[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.configs)  # Κυκλική περιστροφή
        return config
