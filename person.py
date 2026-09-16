class Person:

    def __init__(self, person_id, name):
        self.person_id = person_id

        #Encapsulation
        self._name = name

    def get_name(self):

        return self._name

    def set_name(self, name):

        if name.strip() == "":
            return False

        self._name = name
        return True