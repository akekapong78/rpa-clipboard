import hashlib
from datetime import datetime

def generate_activation_key():
    # Generate the salt based on the current date (UTC midnight)
    utc_midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    salt = utc_midnight.strftime('%Y-%m-%d')

    # Encrypt the salt using SHA-256 to create the activation key
    activation_key = hashlib.sha256(salt.encode()).hexdigest()

    return activation_key

if __name__ == "__main__":
    key = generate_activation_key()
    print(f"Generated Activation Key: {key}")
