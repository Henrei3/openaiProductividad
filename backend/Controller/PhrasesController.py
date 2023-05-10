from backend.Model.PhrasesModel import EncouragedPhrasesModel
from backend.Model.PhrasesModel import ProhibitedPhrasesModel


class EncouragedPhrasesController:

    @staticmethod
    def calculate_score(phrases_model: EncouragedPhrasesModel):
        text = phrases_model.phrase
        phrases = phrases_model.encouraged

        overall_score, management_score = phrases_model.get_phrase_score()

        for ticket in phrases:
            for tag in ticket.get(list(ticket)[0]):
                if tag in text:
                    overall_score += int(ticket.get("PUNTAJE"))
                    for management_tag in management_score:
                        if list(ticket)[0] in management_tag:
                            management_tag[list(ticket)[0]] += int(ticket.get("PUNTAJE"))
                        else:
                            management_score.append(
                                {
                                    list(ticket)[0]: 0
                                }
                            )
        return overall_score, management_score


class ProhibitedPhrasesController:

    @staticmethod
    def calculate_score(phrases_model: ProhibitedPhrasesModel):
        text = phrases_model.phrase.lower()

        negative_score = 0

        phrases = phrases_model.get_prohibited_phrases()

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

