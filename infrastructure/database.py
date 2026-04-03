import email
import os
from configparser import DuplicateSectionError

from infrastructure.logger import log

FILE_PATH = "data/Spring_2026_USW_Cyber_Esports_PoC.txt"


def safe(value):
    return value if value is not None else ""

def save_user(user):
    file_exists = os.path.exists(FILE_PATH)

    with open(FILE_PATH, "a") as file:
        file.write("username|email|password|first_name|last_name|age|twitch|discord|steam|coin|role\n")

        user_record = (
            f"{safe(user.username)}|{safe(user.email)}|{safe(user.password)}|"
            f"{safe(user.first_name)}|{safe(user.last_name)}|{safe(user.age)}|"
            f"{safe(user.twitch)}|{safe(user.discord)}|{safe(user.steam)}|"
            f"{safe(user.coin)}|{safe(user.role)}\n"
        )
        file.write(user_record)

def get_user_by_email(email):
    try:
        with open(FILE_PATH, "r") as file:
            for line in file:
                parsed_line = line.strip().split("|")

                if len(parsed_line)  < 3:
                    continue

                stored_email = parsed_line[1].strip().lower()

                if stored_email == email.lower().strip():
                    return{
                        "username": parsed_line[0],
                        "email": parsed_line[1],
                        "password": parsed_line[2],
                    }
            return  None

    except FileNotFoundError:
        return None

def fetch_all_users():
    users = []

    try:
        with open(FILE_PATH, "r") as file:
            for i, line in enumerate(file):

                if i == 0:
                    continue

                parsed_line = line.strip().split("|")

                if len(parsed_line) < 10:
                    log(f"Invalid line skipped: {line.strip()}", "fetch_all_users", "WARNING")
                    continue

                user = {
                    "username": parsed_line[0],
                    "email": parsed_line[1],
                    "first_name": parsed_line[3],
                    "last_name": parsed_line[4],
                    "age": parsed_line[5],
                    "twitch": parsed_line[6],
                    "discord": parsed_line[7],
                    "steam": parsed_line[8],
                    "coin": parsed_line[9],
                    "role": parsed_line[10],
                }

                users.append(user)
        log(f"{len(users)} users loaded successfully", "fetch_all_users", "INFO")

        return users

    except FileNotFoundError as e:
        log(e, "fetch_all_users", "ERROR")
        return []

    except Exception as e:
        log(e, "fetch_all_users", "CRITICAL")
        return []