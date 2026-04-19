import re
from collections import Counter
from infrastructure.database import get_user_by_email

from Helpers.hashing import HashedData

FILE_PATH = "data/Spring_2026_USW_Cyber_Esports_PoC.txt"
INVALID_CHARACTER = r"^[a-zA-Z0-9_]+"
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class UserValidator:
    ROLE_RULES = {
        "admin": {
            "min_length": 13,
            "uppercase": 1,
            "lowercase": 1,
            "numbers": 2,
            "symbols": 2
        },
        "gamer": {
            "min_length": 10,
            "uppercase": 0,
            "lowercase": 1,
            "numbers": 1,
            "symbols": 1
        }
    }

    SYMBOL_PATTERN = r"[!@#$%^&*(),.?\":{}|<>]"


    def validate(self, password: str, role: str):
        role = role.lower()
        rules = self.ROLE_RULES.get(role)

        if not rules:
            return ["Invalid role"]

        errors = []

        # Length check
        if len(password) < rules["min_length"]:
            errors.append(f"Password must be at least {rules['min_length']} characters long")

        # Single pass character classification
        counts = Counter({
            "uppercase": 0,
            "lowercase": 0,
            "numbers": 0,
            "symbols": 0
        })

        for char in password:
            if char.isupper():
                counts["uppercase"] += 1
            elif char.islower():
                counts["lowercase"] += 1
            elif char.isdigit():
                counts["numbers"] += 1
            elif re.match(self.SYMBOL_PATTERN, char):
                counts["symbols"] += 1

        for key in ["uppercase", "lowercase", "numbers", "symbols"]:
            if counts[key] < rules[key]:
                errors.append(f"Password Must contain at least {rules[key]} {key}")

        return errors

    @staticmethod
    def validate_user(user):
        errors = []

        if not user.username:
            errors.append("Username is required")
        elif not re.match(INVALID_CHARACTER, user.username):
            errors.append("Username contains invalid characters")

        if not user.email:
            errors.append("Email is required")
        elif not re.match(EMAIL_PATTERN, user.email):
            errors.append("Valid email address is required")

        if user.age is not None and user.age < 13:
            errors.append("User must be at least 13 years of age")

        password_validator = UserValidator()
        errors.extend(password_validator.validate(user.password, user.role))

        if user.twitch:
            if not re.match(INVALID_CHARACTER, user.twitch):
                errors.append("Twitch contains invalid characters")

        if user.discord:
            if not re.match(INVALID_CHARACTER, user.discord):
                errors.append("Discord contains invalid characters")

        if user.steam:
            if not re.match(INVALID_CHARACTER, user.steam):
                errors.append("Steam contains invalid characters")

        return errors

    @staticmethod
    def email_exists(email):
        try:
            with open(FILE_PATH, "r") as file:
                for line in file:
                    parts = line.strip().split("|")

                    if len(parts) < 2:
                        continue

                    stored_email = parts[1]

                    if stored_email.lower() == email.lower():
                        return True

            return False

        except FileNotFoundError:
            return False


    @staticmethod
    def username_exists(username):
        try:
            with open(FILE_PATH, "r") as file:
                for line in file:
                    parts = line.strip().split("|")

                    if len(parts) < 1:
                     continue

                    stored_username = parts[0]

                    if stored_username.lower() == username.lower():
                        return True

            return False

        except FileNotFoundError:
            return False

    @staticmethod
    def validate_login(login_model):
        errors = []

        user = get_user_by_email(login_model.email)

        if not user:
            errors.append("Email is not valid")
            return errors

        if not HashedData.verify_data(
                login_model.password,
                user["password"]
        ):
            errors.append("Password  is invalid")

        return errors

