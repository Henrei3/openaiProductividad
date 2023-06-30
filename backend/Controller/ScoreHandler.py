from __future__ import annotations
from backend.Controller.SentenceController import EncouragedSentencesController, ProhibitedSentencesController
from backend.Controller.SentenceController import EncouragedSentenceModel, ProhibitedPhrasesModel
from backend.Controller.PostGreSQLController import PostgreController
from backend.Model.DB.recordingsDB import Recording, Scores
from abc import ABC, abstractmethod
from typing import Any, Optional


class ScoreHandler(ABC):
    """
    The Score Handler interface implements two methods :

    A method for organizing the structure of the chain of responsibility
    And a second one to execute the chain of command
    """

    @abstractmethod
    def set_next(self, handler: ScoreHandler) -> ScoreHandler:
        pass

    @abstractmethod
    def handle(self, request, data: dict):
        pass


class AbstractScoreHandler(ScoreHandler):

    __next_handler: ScoreHandler = None

    def set_next(self, handler: ScoreHandler) -> ScoreHandler:
        self.__next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request, data: dict):
        if self.__next_handler:
            return self.__next_handler.handle(request, data)
        else:
            return None


"""
Here are all the concrete handlers
For the purpose of calculating the scores and storing them into a database we will need three handlers:
<li>
<ul> Positive Score calculation</ul>
<ul> Negative ScoreCalculation</ul>
<ul> Database Score Storing  </ul>

"""


class EncouragedPhrasesScoreHandler(AbstractScoreHandler):
    """
    First element of the chain of responsibility pattern

    It evaluates the audio and attributes the positive score part of the score evaluation
    """
    def handle(self, request: EncouragedSentenceModel, data: dict):
        """
        This method needs to receive one element from data to work:
        - The id of the recording for which the score is being calculated

        This handle method will only receive an EncouragedModel object as a request
        It will then return the result to the next link of the chain
        """
        positive, ticket_positive = EncouragedSentencesController.calculate_score(request)
        return super().handle(
            ProhibitedPhrasesModel(request.sentence),
            {"positive": positive, "ticket_positive": ticket_positive, "r_id": data["r_id"]}
        )


class ProhibitedPhrasesScoreHandler(AbstractScoreHandler):

    def handle(self, request: ProhibitedPhrasesModel, data: dict):
        negative_score = ProhibitedSentencesController.calculate_score(request)
        total = data["positive"] + negative_score

        score = {"total": total, "ticket_score": data["ticket_positive"]}

        return super().handle(
            Scores(data["r_id"], score),
            {})


class DatabaseStoringScoreHandler(AbstractScoreHandler):

    def handle(self, request: Scores, data: dict) -> Scores:
        score = PostgreController.add_scores(request)
        print("Chain of Responsibility: Database Storing -> Successfully added score")
        return score
