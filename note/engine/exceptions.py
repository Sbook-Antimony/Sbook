class NoteException(BaseException):
    pass

class TagDoesNotExistsException(NoteException, ValueError):
    pass
