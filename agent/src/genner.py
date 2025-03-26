from typing import List, Dict, Any

class Genner:
    def __init__(self):
        self.generated_data = {}

    def generate_text(self, prompt: str) -> str:
        """Δημιουργεί κείμενο με βάση ένα prompt."""
        return f"Generated response for: {prompt}"

    def store_data(self, key: str, data: Any) -> None:
        """Αποθηκεύει δεδομένα για μεταγενέστερη χρήση."""
        self.generated_data[key] = data

    def get_data(self, key: str) -> Any:
        """Επιστρέφει τα αποθηκευμένα δεδομένα."""
        return self.generated_data.get(key, None)

# Χρήση του Genner για δοκιμή
if __name__ == "__main__":
    g = Genner()
    response = g.generate_text("Hello, AI!")
    g.store_data("greeting", response)
    print(g.get_data("greeting"))
