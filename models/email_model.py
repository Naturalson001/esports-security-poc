class EmailModel:
    def __init__(self, body: str, subject: str):
        self.body = body
        self.subject = subject

class EmailMessage(EmailModel):
    def __init__(self, body: str, subject: str, to: str):
        super().__init__(body, subject)
        self.to = to
