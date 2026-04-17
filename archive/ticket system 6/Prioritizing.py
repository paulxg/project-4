from UniversalData import CurrentUserdata

class Prioritizing:
    def __init__(self):
        self.final_factor = None

    def status_calculation(self):
        if CurrentUserdata.company == "company":
            self.final_factor = self.factor * 1.1

        else:
            self.final_factor = self.factor