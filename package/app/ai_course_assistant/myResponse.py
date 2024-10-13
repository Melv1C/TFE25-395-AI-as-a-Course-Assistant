class MyResponse:
    def __init__(self, success, message) -> None:
        self.success = success    # boolean
        self.message = message  # string

    @staticmethod
    def parse(response: dict) -> 'MyResponse':
        success = (response.get('code', 0) == 200)
        message = response.get('data') if success else response.get('message')

        return MyResponse(
            success=success,
            message=message
        )

    def json(self) -> dict:
        return {
            "success": self.success,
            "message": self.message
        }

    def __str__(self) -> str:
        if self.success:
            return f"Success: {self.message}"
        return f"Error: {self.message}"