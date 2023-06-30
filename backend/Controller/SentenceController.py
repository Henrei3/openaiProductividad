from backend.Model.SentenceModel import EncouragedSentenceModel
from backend.Model.SentenceModel import ProhibitedPhrasesModel
from backend.Model.RecordingModel import RecordingModel


class EncouragedSentencesController:

    @classmethod
    def calculate_score(cls, phrases_model: EncouragedSentenceModel):
        sentence = phrases_model.sentence.lower()
        encouraged_list = phrases_model.get_encouraged_list()

        overall_score = 0
        positive_score = list()

        for ticket_row in encouraged_list:
            sentence_category = list(ticket_row)[0]
            # We iterate throw all the sentences that are considered as positive
            for positive_sentence in ticket_row[sentence_category]:
                if positive_sentence.lower() in sentence:
                    positive_sentence_points = int(ticket_row.get("PUNTAJE"))
                    overall_score += positive_sentence_points
                    if len(positive_score) > 0:
                        for positive_score_element in positive_score:
                            if sentence_category in positive_score_element:
                                positive_score_element[sentence_category] += positive_sentence_points
                            elif positive_score_element == positive_score[-1]:
                                positive_score.append({
                                    sentence_category: 0
                                })
                    else:
                        positive_score.append({
                            list(ticket_row)[0]: positive_sentence_points
                        })
        return overall_score, positive_score


class ProhibitedSentencesController:

    @classmethod
    def calculate_score(cls, phrases_model: ProhibitedPhrasesModel):
        text = phrases_model.phrase.lower()

        negative_score = 0

        phrases = phrases_model.get_prohibited_phrases()

        for nonoword in phrases:
            treated_word = cls.normalize(nonoword[0].lower())
            if treated_word in text:
                negative_score -= nonoword[1]
        return negative_score

    @staticmethod
    def normalize(sentence: str):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for before, after in replacements:

            if before in sentence:
                return sentence.replace(before, after)
        return sentence

