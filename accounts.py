from pathlib import Path

import yaml

import sbook.models

DIR = Path(__file__).parent
ACCOUNTS = DIR/'accounts'

assert ACCOUNTS.exists(), f"accounts folder {ACCOUNTS!r} does not exists"


class Account:
    DEFAULT_PHOTO = "/image/default-photo.png"
    name:tuple[str]
    password:str
    data:dict
    folder:Path
    id:int
    def __init__(self:'Account', id:int):
        self.id = id
        self.folder = ACCOUNTS / str(self.id)
        self.data = yaml.safe_load((self.folder / 'data.yaml').read_text())

        self.password = self.data.get("password")
        self.firstname = self.data.get("firstname")
        self.lastname = self.data.get("lastname")

    @staticmethod
    def login_info(fname:str, lname:str, pswd:str) -> int:
        users = sbook.models.Account.objects.all()
        for user in users.values():
            if user.get("firstname") == fname and user.get("lastname") == lname:
                if user.get("password") == pswd:
                    return user.get("id")
                else:
                    return -1
        else:
            return -2

def create_account(data:dict) -> int:
    #users = sbook.models.Account.objects.all()
    _account = sbook.models.Account(
        firstname=data.get("firstname"),
        lastname=data.get("lastname"),
        password=data.get("password")
    )
    _account.save()
    id = _account.id

    folder = ACCOUNTS / str(id)

    folder.mkdir()

    profile = folder / "profile.png"
    profile.touch()
    profile.write_bytes(DIR / 'image' / 'default-photo.png')

    data_file = (folder/"data.yaml")
    data_file.touch()
    data_file.write_text(yaml.safe_dump(data))

    return Account(id)
