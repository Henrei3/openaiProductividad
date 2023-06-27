import sqlalchemy

from backend.Model.PhrasesModel import EncouragedPhrasesModel, ProhibitedPhrasesModel
from backend.Model.DB.SQLServer import SQLSERVERDBModel
from backend.Controller.CalculoPrecios import AudioPriceCalculation, Currency, EmbeddingsPriceCalculation
from backend.Model.RequestModel import AudioGPTRequestModel
from backend.Controller.PossibleWav import PossibleWav
from backend.Model.RequestModel import EmbeddingRequestModel
from backend.Controller.PostGreSQLController import PostgreController
import subprocess
import unittest


class PhrasesUnitTesting(unittest.TestCase):
    def test_get_encouraged_list_when_ced_unexistent(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "nonexistingced")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)

    def test_get_encouraged_list_when_ced_exists(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "diners")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)

    def test_cedente_general_exists(self):
        phrases_test = EncouragedPhrasesModel("Hola Que tal", "CEDENTE_GENERAL")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)


class ConexionTesting(unittest.TestCase):
    def test_cnxn_getserialced_working(self):
        cnxn = SQLSERVERDBModel()
        element = cnxn.get_serialced_fromname("diners")
        self.assertNotEquals(element, None)


class AudioClassCalculationTesting(unittest.TestCase):

    def setUp(self) -> None:
        subprocess.call(r"C:\Users\hjimenez\Desktop\Backup\backend\openRepo.bat")
        audios = PossibleWav.get_recordings("0980427196", "2023-04-27")

        self.audio_request = AudioGPTRequestModel("Test", audios[0].path, "out-0980427196-702-20230427-092354-1682605434.25")

    def test_audio_calculation_usd(self):
        price = AudioPriceCalculation.audio_request_price_calculation(self.audio_request, Currency.AudioPricing.USD)
        self.assertEquals(price, 0.048)

    def test_audio_calculation_eur(self):
        price = AudioPriceCalculation.audio_request_price_calculation(self.audio_request, Currency.AudioPricing.EUR)
        self.assertEquals(price, 0.044)

    def test_audio_calculation_cop(self):
        price = AudioPriceCalculation.audio_request_price_calculation(self.audio_request, Currency.AudioPricing.COP)
        self.assertEquals(price, 198.4)

    def test_audio_calculation_pen(self):
        price = AudioPriceCalculation.audio_request_price_calculation(self.audio_request, Currency.AudioPricing.PEN)
        self.assertEquals(price, 0.176)


class EmbeddingsClassCalculationTest(unittest.TestCase):

    a_thousand_tokens = " This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a token This is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a tokenThis is a toks a tokenThis is a toks a tokenThis is a tokeee"

    def setUp(self) -> None:
        self.embedding_request = EmbeddingRequestModel("test", "text")
        self.thousand_tokens_request = EmbeddingRequestModel("test", self.a_thousand_tokens)
        self.thousand_tokens_request_plus_one = EmbeddingRequestModel("test", self.a_thousand_tokens+" ")

    def test_token_rounded_correctly(self):
        a_thousand_tokens_price = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request,
            Currency.EmbeddingsPricing.USD
        )
        a_thousand_tokens_plus_one_price = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request_plus_one,
            Currency.EmbeddingsPricing.USD
        )
        self.assertNotEquals(a_thousand_tokens_price, a_thousand_tokens_plus_one_price)

    def test_price_calculation_eur(self):
        eur_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.embedding_request, Currency.EmbeddingsPricing.EUR
        )
        self.assertEquals(eur_value, Currency.EmbeddingsPricing.EUR)
        new_eur_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request_plus_one,
            Currency.EmbeddingsPricing.EUR)
        self.assertEquals(new_eur_value, Currency.EmbeddingsPricing.EUR*2)

    def test_price_calculation_usd(self):
        usd_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.embedding_request, Currency.EmbeddingsPricing.USD
        )
        self.assertEquals(usd_value, Currency.EmbeddingsPricing.USD)
        new_usd_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request_plus_one,
            Currency.EmbeddingsPricing.USD)
        self.assertEquals(new_usd_value, Currency.EmbeddingsPricing.USD * 2)

    def test_price_calculation_cop(self):
        cop_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.embedding_request, Currency.EmbeddingsPricing.COP
        )
        self.assertEquals(cop_value, Currency.EmbeddingsPricing.COP)
        new_usd_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request_plus_one,
            Currency.EmbeddingsPricing.COP)
        self.assertEquals(new_usd_value, Currency.EmbeddingsPricing.COP * 2)

    def test_price_calculation_pen(self):
        pen_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.embedding_request, Currency.EmbeddingsPricing.PEN
        )
        self.assertEquals(pen_value, Currency.EmbeddingsPricing.PEN)
        new_usd_value = EmbeddingsPriceCalculation.embeddings_calculation(
            self.thousand_tokens_request_plus_one,
            Currency.EmbeddingsPricing.PEN)
        self.assertEquals(new_usd_value, Currency.EmbeddingsPricing.PEN * 2)


class PostGreControllerUnitTest(unittest.TestCase):
    def test_get_recording_output(self):
        embedding_test = PostgreController.get_embedding('test')
        self.assertNotEquals(type(embedding_test), sqlalchemy.engine.row.Row)

    def test_get_records_if_record_dont_exist(self):
        embedding_test = PostgreController.get_embedding('fesfsa')
        self.assertEquals(embedding_test, None)

    def test_get_audio_text(self):
        embedding_test = PostgreController.get_audio_text('4')
        self.assertEquals(type(embedding_test[0]), dict)

    def test_get_audio_text_not_found(self):
        embedding_test = PostgreController.get_audio_text('5')
        self.assertNotEqual(type(embedding_test), None)
        self.assertEquals(embedding_test[0], None)

