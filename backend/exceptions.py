from fastapi import HTTPException, status

class TenderException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class TenderNotFound(TenderException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Тендер не найден."
    
class TenderVersionNotFound(TenderException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Версия тендера не найден."

class EmployeeException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserNotFound(EmployeeException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не существует или некорректен."

class PermissionDenied(EmployeeException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав для выполнения действия."

class BidException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class BidNotFound(BidException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Предложение не найдено."