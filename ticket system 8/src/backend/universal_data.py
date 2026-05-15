# Universal userdata
class CurrentUserdata:
    id = None
    rank = None

#mit CurrentUserdata.id in anderen Klassen darauf zugreifen

class ProgramData:

    support_categories = {
        "Installation or Updates":1,
        "Network or Connection Issues":1,
        "Licenses or Accounts":1,
        "Application Issues":1,
        "Files or Storage":1,
        "Security or Privacy":1,
        "Suggestions for Improvement / Missing Features":1,
        "Miscellaneous":1
    }


    myticket_columns = [
        "Category",
        "Problem",
        "Detailed description"
    ]


