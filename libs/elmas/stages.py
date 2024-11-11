class Stages:
    def __init__(self, stages):
        self.data = {}
        self.endtime = None
        self.selections = None
        self.stagelevel = None
        self.starttime = None
        
        if stages.get('data') is not None:
            self.data = stages.get('data')
            self.endtime = self.data.get('endtime')
            self.selections = self.data.get('selections')
            self.stagelevel = self.data.get('stagelevel')
            self.starttime = self.data.get('starttime')
