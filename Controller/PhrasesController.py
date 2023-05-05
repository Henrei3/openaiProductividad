from Model.PhrasesModel import EncouragedPhrasesModel
from Model.PhrasesModel import ProhibitedPhrasesModel


class EncouragedPhrasesController:

    @staticmethod
    def calculate_score(open_text):
        text = open_text.upper()
        overall_score = 0

        phrases_model = EncouragedPhrasesModel()
        phrases = phrases_model.get_encouraged_list()

        management_score = list()

        for ticket in phrases:
            management_score.append({
                list(ticket)[0]: 0
            })
            for tag in ticket.get(list(ticket)[0]):
                if tag in text:
                    overall_score += int(ticket.get("PUNTAJE"))
                    for management_tag in management_score:
                        if list(ticket)[0] in management_tag:
                            management_tag[list(ticket)[0]] += int(ticket.get("PUNTAJE"))
        return overall_score, management_score


class ProhibitedPhrasesController:

    @staticmethod
    def calculate_score(open_text):
        text = open_text.lower()

        negative_score = 0

        phrases_model = ProhibitedPhrasesModel()
        phrases = phrases_model.get_prohibiited_phrases()

        for nonoword in phrases:
            if nonoword[0].lower() in text:
                negative_score -= nonoword[1]
        return negative_score


""" 
test = "cooperativa jep"

positive = EncouragedPhrasesController.calculate_score(test)

negative = ProhibitedPhrasesController.calculate_score(test)

total = negative + positive[0]
"""

