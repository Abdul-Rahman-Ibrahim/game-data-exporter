class Event:
    def __init__(self, event):
        self.blockId = event.get('blockId')
        self.blockType = event.get('blockType')
        self.code = event.get('code') # xml
        self.eventType = event.get('eventType')
        self.starttime = event.get('starttime')
        self.message = event.get('message')
        

class Player1Level:
    def __init__(self, player1level):
        self.endtime = player1level.get('endtime')
        self.events = []
        self.levelno = player1level.get('levelno')
        self.starttime = player1level.get('starttime')

        if player1level.get('events') is not None:
            for event in player1level['events']:
                self.events.append(Event(event))


class Player2Level:
    def __init__(self, player2level):
        self.endtime = player2level.get('endtime')
        self.events = []
        self.levelno = player2level.get('levelno')
        self.starttime = player2level.get('starttime')
        
        if player2level.get('events') is not None:
            for event in player2level['events']:
                self.events.append(Event(event))

                
class Stage2_3_4:
    def __init__(self, stage):
        self.endtime = stage.get('endtime')
        self.player1levels = [None] * 60
        self.player2levels = [None] * 60
        self.starttime = stage.get('starttime')

        if stage.get('player1levels') is not None:
            i = 0
            for player1level in stage['player1levels']:
                self.player1levels[i] = Player1Level(player1level)
                i += 1

        if stage.get('player2levels') is not None:
            i = 0
            for player2level in stage['player2levels']:
                self.player2levels[i] = Player2Level(player2level)
                i += 1