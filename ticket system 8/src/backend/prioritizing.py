from backend.universal_data import ProgramData


class Prioritizing:
    def __init__(self):
        super().__init__()
        self.prio = None

    def setprio(self,category):
        self.prio = ProgramData.support_categories[category]
