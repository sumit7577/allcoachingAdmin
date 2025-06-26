import random,re

def generate_random_username(name: str) -> str:
    """
    Generates a sanitized username from name + random number.
    E.g., 'Sumit Kumar' → 'sumitkumar_8341'
    """
    # Sanitize the name: remove non-alphanumeric, lowercase it
    sanitized_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    random_number = random.randint(1000, 9999)
    return f"{sanitized_name}_{random_number}"