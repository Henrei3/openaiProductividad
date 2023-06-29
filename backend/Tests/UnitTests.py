from backend.Controller.CalculoPrecios import AudioPriceCalculation, Currency, EmbeddingsPriceCalculation
from backend.Model.SentenceModel import EncouragedSentenceModel, ProhibitedPhrasesModel
from backend.Model.DB.PostGreSQLModel import PostGre, Recording, Scores, Embedding, Base
from backend.Model.RequestModel import EmbeddingRequestModel, AudioGPTRequestModel, RecordingModel
from backend.Controller.GPTCreator import OpenAIProxyAudio, OpenAIProxyEmbeddings
from backend.Controller.PostGreSQLController import PostgreController
from backend.Controller.SQLServerController import SQLSERVERDBModel, SQLServerController
from backend.Controller.PossibleWav import PossibleWav
from backend.Controller.pathFinder import WavFinder
from pydub import AudioSegment
from decouple import config
from unittest.mock import Mock
import subprocess
import sqlalchemy
import unittest
import openai
import os


class PhrasesUnitTesting(unittest.TestCase):
    def test_get_encouraged_list_when_ced_unexistent(self):
        phrases_test = EncouragedSentenceModel("Hola Que tal", "nonexistingced")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)

    def test_get_encouraged_list_when_ced_exists(self):
        phrases_test = EncouragedSentenceModel("Hola Que tal", "diners")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)

    def test_cedente_general_exists(self):
        phrases_test = EncouragedSentenceModel("Hola Que tal", "CEDENTE_GENERAL")
        encouraged_list = phrases_test.get_encouraged_list()
        self.assertNotEquals(encouraged_list, None)


class SQLServerModelTesting(unittest.TestCase):
    def test_cnxn_getserialced_working(self):
        cnxn = SQLSERVERDBModel()
        element = cnxn.get_serialced_from_cedente("diners")
        self.assertNotEquals(element, None)

    def test_setup_cedente_general(self):
        cnxn = SQLSERVERDBModel()
        cnxn.setup_cedente_general()
        serial_ced = cnxn.get_serialced_from_cedente("CEDENTE_GENERAL")

        self.assertNotEqual(serial_ced, None)

        sentences = cnxn.get_positive_sentences(serial_ced[0])
        for sentence in sentences:
            print(sentence)
        self.assertNotEqual(sentences, None)


class SQLServerControllerTesting(unittest.TestCase):
    def test_get_positive_sentences_from_cedente_general(self):
        controller = SQLServerController()
        sentences = controller.get_positive_sentences_from_cedente("CEDENTE_GENERAL")

        self.assertNotEqual(sentences, None, "Senteces seems to be None")
        for sentence in sentences:
            print(sentence)

    def test_get_positive_sentences_from_unexisting(self):
        controller = SQLServerController()

        sentences = controller.get_positive_sentences_from_cedente("unexisting")

        self.assertNotEqual(sentences, None, "Senteces seems to be None")
        for sentence in sentences:
            print(sentence)

    def test_get_positive_sentences_from_existing(self):
        controller = SQLServerController()

        sentences = controller.get_positive_sentences_from_cedente("diners")

        self.assertNotEqual(sentences, None, "Senteces seems to be None")
        for sentence in sentences:
            print(sentence)


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
        controller_result = PostgreController.get_embedding('test')
        self.assertNotEquals(type(controller_result), sqlalchemy.engine.row.Row)

    def test_get_records_if_record_dont_exist(self):
        controller_result = PostgreController.get_embedding('fesfsa')
        self.assertEquals(controller_result, None)

    def test_get_audio_text(self):
        controller_result = PostgreController.get_audio_text('4')
        self.assertEquals(type(controller_result[0]), dict)

    def test_get_audio_text_not_found(self):
        controller_result = PostgreController.get_audio_text('5')
        self.assertNotEqual(type(controller_result), None)
        self.assertEquals(controller_result[0], None)

    def test_get_recordings_given_date(self):
        results = PostgreController.get_recordings_given_date('2023', '04', '10')
        print(type(results))
        for result in results:
            self.assertEqual(type(result[0]), Recording)


class PostGreSQLModelTesting(unittest.TestCase):

    def test_if_exists(self, table: Base, identifier: str):
        postgre = PostGre()
        result = postgre.check_if_exists(table, identifier)

        self.assertTrue(result is not None)


class AudioGPTRequestControllerTesting(unittest.TestCase):

    def test_audio_segmentation_if_25_mb_or_more(self):
        wav_finder = WavFinder(r"Z:\Apache24\htdocs\rec\grabaciones\2023\04\10")
        wav_list = wav_finder.find_all()
        if wav_list != -1:
            for wav_model in wav_list:
                wav_model.size = os.stat(wav_model.path).st_size / (1024*1024)
                if wav_model.size > 24:
                    gpt_request_model = AudioGPTRequestModel("", wav_model.path, wav_model.name, wav_model.size)
                    response = OpenAIProxyAudio.check_access(gpt_request_model, True)

                    self.assertTrue(len(response) > 2000)
                    print(response)
                    break
        else:
            print('There has been an error searching for the wav files : ', wav_list)


class EmbeddingGPTRequestControllerTesting(unittest.TestCase):

    def test_embedding_data_base_storing(self):

        embedding = EmbeddingRequestModel("test_name0995206482", "This should be transformed into an embedding")
        embedding.set_recording('1234')
        proxy_response = OpenAIProxyEmbeddings.check_access(embedding, False)
        if type(proxy_response) is float:
            print("El calculo de este embedding de sera : ", proxy_response, "\n Desea Continuar ?  s/n ")
            response = input()
            if response == "s":
                proxy_response = OpenAIProxyEmbeddings.check_access(embedding, True)
                print(proxy_response)
                postgre_model_testing = PostGreSQLModelTesting()
                self.assertTrue(type(embedding.get_recording_row()[0]), int)
                postgre_model_testing.test_if_exists(Embedding, embedding.get_recording_row()[0])

        # Embeddings Vector has 1526 dimensions
        self.assertTrue(len(proxy_response) == 1536)


class RecordingClassTesting(unittest.TestCase):

    def test_set_recording_doesnt_double_store(self):
        for i in range(0, 10):
            recording = RecordingModel("dont_double_this_name")
            recording.set_recording('1111')
        postgre = PostGre()
        results = postgre.get_recording_given_name("dont_double_this_name")
        i = 0
        for result in results:
            print(result)
            i += 1
        self.assertTrue(i == 1)

    def test_cellphone_recognition(self):
        recording_model = RecordingModel("cell0994382958phone")
        recording_model.set_recording('1309874')

        postgre = PostGre()
        results = postgre.get_recording_given_name('cell0994382958phone')

        for result in results:
            recording: Recording = result[0]
            print(recording.cellphone)
            self.assertTrue(str(recording.cellphone) in "0994382958")

