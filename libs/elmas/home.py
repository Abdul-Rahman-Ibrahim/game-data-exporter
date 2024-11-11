class Selection:
    def __init__(self, selection):
        self.gametype = selection.get('gametype', None)
        self.grade = selection.get('grade', None)
        self.player1data = selection.get('player1data')
        self.player2data = selection.get('player2data')
        self.playerdata = selection.get('playerdata')
        self.school = selection.get('school', None)
        

class Home:
    def __init__(self, home: dict):
        self.endtime = home.get('endtime', 0)
        self.selections = []
        if home.get('selections', None) is not None:      
            for selection in home['selections']:
                self.selections.append(Selection(selection))
        self.starttime = home.get('starttime', 0)