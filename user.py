# this class stores user_id, username and _password
# and provides login(), logout(), get_username(), and verify_password()

class User:

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username

        # Encapsulation
        self._password = password

        self.logged_in = False

    def login(self, username, password):

        if (
            self.username == username
            and
            self._password == password
        ):
            self.logged_in = True
            return True

        return False

    def logout(self):

        self.logged_in = False

    def get_username(self):

        return self.username

    def verify_password(self, password):

        return self._password == password