class QuestionNSP:
    def __init__(self, question_nsp):
        self.answers = question_nsp.get('answer')
        self.clicktime = question_nsp.get('clicktime')
        self.questionno = question_nsp.get('questionno')
        

class QuestionSP:
    def __init__(self, question_sp):
        self.endtime = question_sp.get('endtime')
        self.answers = question_sp.get('answers')
        self.questionno = question_sp.get('questionno')
        self.starttime = question_sp.get('starttime')


class Stage1_5:
    def __init__(self, stage):
        self.endtime = stage.get('endtime')
        self.finalanswers = stage.get('finalanswers')
        self.questions = stage.get('questions')
        self.selected_player = stage.get('selected_player')
        self.starttime = stage.get('starttime')
        self.finalanswers_nsp = None
        self.finalanswers_sp = None

        if self.finalanswers is not None:
            self.finalanswers_nsp = self.finalanswers.get('nonselectedplayer')
            self.finalanswers_sp = self.finalanswers.get('selected_player')

        self.questions_nsp = []
        if self.questions is not None:
            if self.questions.get('nonselectedplayer') is not None:
                for question in self.questions.get('nonselectedplayer'):
                    self.questions_nsp.append(QuestionNSP(question))

        self.questions_sp = []
        if self.questions is not None:
            if self.questions.get('selected_player') is not None:
                for question in self.questions.get('selected_player'):
                    self.questions_sp.append(QuestionSP(question))