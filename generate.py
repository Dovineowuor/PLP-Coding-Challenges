import string
import random

class PasswordGenerator:
    def __init__(self):
        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special_chars = string.punctuation

    def generate_password(self, length):
        """Generate a random password with the given length."""
        password = ""
        password += random.choice(self.letters)  # Ensure at least one letter
        password += random.choice(self.digits)  # Ensure at least one digit
        password += random.choice(self.special_chars)  # Ensure at least one special character

        # Fill the rest of the password with random characters
        password += "".join(
            random.choices(
                self.letters + self.digits + self.special_chars, k=length - 7
            )
        )

        # Shuffle the password to make it more random
        password_list = list(password)
        random.shuffle(password_list)
        password = "".join(password_list)

        return password

