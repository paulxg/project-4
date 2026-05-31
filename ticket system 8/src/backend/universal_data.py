# Universal userdata
class CurrentUserdata:
    id = None
    rank = None
    username = None

#mit CurrentUserdata.id in anderen Klassen darauf zugreifen

class ProgramData:

    support_categories = {
        "Installation or Updates": 5,
        "Network or Connection Issues": 8,
        "Licenses or Accounts": 5,
        "Application Issues": 6,
        "Files or Storage": 4,
        "Security or Privacy": 15,
        "Suggestions for Improvement / Missing Features": 1,
        "Others": 2
    }


    myticket_columns = [
        "Category",
        "Problem",
        "Detailed description"
    ]


