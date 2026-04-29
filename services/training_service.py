from infrastructure.database import update_user_score

class TrainingService:

    def __init__(self):
        self.score = 0

    def start_training(self):
        print("\n  ESPORTS SECURITY TRAINING\n")

        self.password_security()
        self.phishing_awareness()
        self.communication_safety()
        self.personal_data_protection()

        print(f"\n✅ Training Completed! Your Score: {self.score}\n")

        print(f"\n✅ Please enter your email to save your point")

        email = input("Email: ").strip()

        result = update_user_score(email, self.score)

        if result:
            print("✅ Score updated successfully")
        else:
            print("❌ Email not found")

    def password_security(self):
        print("🔐 PASSWORD SECURITY")
        print("A strong password should be long, unique, and hard to guess.")
        print("Using the same password across platforms is dangerous.\n")

        answer = input("❓ Should you reuse the same password for multiple accounts? (yes/no): ")

        if answer.lower() == "no":
            print("✅ Correct! Reusing passwords increases risk.\n")
            self.score += 10
        else:
            print("❌ Incorrect. Never reuse passwords.\n")

        answer2 = input("❓ Which is stronger?\n1. password123\n2. G@m3r!Secure#2026\nChoose 1 or 2: ")

        if answer2 == "2":
            print("✅ Correct! Strong passwords use symbols, numbers, and length.\n")
            self.score += 10
        else:
            print("❌ Incorrect. That password is weak.\n")


    def phishing_awareness(self):
        print("🎣 PHISHING AWARENESS")
        print("Phishing attacks trick you into giving away your login details.\n")

        answer = input(
            "❓ You receive a message: 'Click here to claim free skins!' What do you do?\n(a) Click the link\n(b) Ignore/report it\n: ")

        if answer.lower() == "b":
            print("✅ Correct! It could be a phishing attack.\n")
            self.score += 10
        else:
            print("❌ Incorrect. That link could steal your account.\n")

        answer2 = input("❓ Should you enter your password on unknown websites? (yes/no): ")

        if answer2.lower() == "no":
            print("✅ Correct! Always verify websites.\n")
            self.score += 10
        else:
            print("❌ Incorrect. Never trust unknown sites.\n")

    def communication_safety(self):
        print("💬 SAFE COMMUNICATION")
        print("Online chats can be risky if you share personal info.\n")

        answer = input("❓ A player asks for your email and password. What do you do?\n(a) Share it\n(b) Refuse\n: ")

        if answer.lower() == "b":
            print("✅ Correct! Never share sensitive info.\n")
            self.score += 10
        else:
            print("❌ Incorrect. This could lead to account theft.\n")

    def personal_data_protection(self):
        print("🛡 PERSONAL DATA PROTECTION")
        print("Keep your personal information safe.\n")

        answer = input("❓ Should you share your OTP code with anyone? (yes/no): ")

        if answer.lower() == "no":
            print("✅ Correct! OTPs must be kept secret.\n")
            self.score += 10
        else:
            print("❌ Incorrect. Sharing OTP gives access to your account.\n")