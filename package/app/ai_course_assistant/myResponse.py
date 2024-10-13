class MyResponse:
    def __init__(self, status, message) -> None:
        self.status = status    # boolean
        self.message = message  # string

    @staticmethod
    def parse(response: dict) -> 'MyResponse':
        status = (response.get('code', 0) == 200)
        message = response.get('data') if status else response.get('message')

        return MyResponse(
            status=status,
            message=message
        )

    def json(self) -> dict:
        return {
            "status": self.status,
            "message": self.message
        }

    def __str__(self) -> str:
        if self.status:
            return f"Success: {self.message}"
        return f"Error: {self.message}"