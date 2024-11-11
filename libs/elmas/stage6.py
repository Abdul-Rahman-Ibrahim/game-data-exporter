class Stage6:
    def __init__(self, stage):
        self.puanlar = {}
        self.selected_stage = stage.get('selected_stage')

        if stage.get('puanlar') is not None:
            for s in stage['puanlar']:
                self.puanlar[s] = stage['puanlar'][s]