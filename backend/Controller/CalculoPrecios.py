from backend.Model.RequestModel import AudioGPTRequestModel,EmbeddingRequestModel
from pydub import AudioSegment
from enum import Enum
import tiktoken
import makeobj
import math


class Currency(makeobj.Obj):
    class EmbeddingsPricing(makeobj.Obj):
        # Euro
        EUR = 0.000092
        # Dollar
        USD = 0.0001
        # Peso Colombia
        COP = 0.41
        # Peso Peru
        PEN = 0.00036

    class AudioPricing(makeobj.Obj):
        # Euro
        EUR = 0.0055
        # Dollar
        USD = 0.006
        # Peso Colombia
        COP = 24.80
        # Peso Peru
        PEN = 0.022


class AudioPriceCalculation:

    @staticmethod
    def audio_request_price_calculation(recording: AudioGPTRequestModel, currency: Currency.AudioPricing.mro()) -> float:
        """ This method calculates the price of an API call in the currency specified with a certain recording"""
        duration: str
        audio_recording = AudioSegment.from_wav(recording.get_audio_path())
        duration = audio_recording.duration_seconds
        duration_in_minutes = float(duration)/60
        return math.ceil(duration_in_minutes) * currency


class EmbeddingsPriceCalculation:

    @staticmethod
    def embeddings_calculation(embedding_model: EmbeddingRequestModel, currency: Currency.EmbeddingsPricing.mro()):
        """ This method calculates the price of an embeddings API call in
        the currency Specified with a certain text """
        tiktoken_tool = tiktoken.get_encoding("cl100k_base")
        nb_tokens = len(tiktoken_tool.encode(embedding_model.get_text()))
        tokens_rounded_to_the_nearest_thousand = math.ceil(nb_tokens/1000)
        return tokens_rounded_to_the_nearest_thousand * currency
