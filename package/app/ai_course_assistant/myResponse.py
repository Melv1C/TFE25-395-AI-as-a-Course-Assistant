class MyResponse:
    def __init__(self, success, message) -> None:
        self.success = success          # boolean
        self.message = message          # string

    @staticmethod
    def parse(isAsync: bool, response: dict) -> 'MyResponse':
        success = (response.get('code', 0) == 200)

        if not success:
            return ErrorResponse(response.get('message'))
        
        if isAsync:
            return AsyncResponse(response.get('data'))
        else:
            return SyncResponse(response.get('data'))
    
class AsyncResponse(MyResponse):
    def __init__(self, id) -> None:
        super().__init__(True, f"Get the feedback using the id: {id}")
        self.id = id

class SyncResponse(MyResponse):
    def __init__(self, feedback) -> None:
        super().__init__(True, "Feedback received")
        self.feedback = feedback

class ErrorResponse(MyResponse):
    def __init__(self, message) -> None:
        super().__init__(False, message)

