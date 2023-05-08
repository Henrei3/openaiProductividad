from backend.Model.pathFinder import WavFinder
from backend.Model.AudioGPTRequestModel import AudioGPTRequestModel
from backend.Model.ChatGPTRequestModel import ChatGPTRequestModel
from backend.Controller.GPTCreator import OpenAIRequestCreator
from backend.Controller.analyser import SpeechRefinement
from backend.Controller.analyser import PatternController
from decouple import config
import os


def gestiones_de_pago():
    prompt = config('PROMPT')
    wavfinder = WavFinder("./")

    if not os.path.exists("./analysed_records"):
        os.makedirs("./analysed_records")
        os.makedirs("./analysed_records/audio_text")
        os.makedirs("./analysed_records/gptAnswer")
        os.makedirs("./analysed_records/patterns")

    wavs = wavfinder.find_all()
    for audio_file in wavs:
        """ Speech To Text """
        audio_gpt = AudioGPTRequestModel(prompt, audio_file[1], audio_file[0])
        audio_response = OpenAIRequestCreator.audio_request(audio_gpt)
        audio_gpt.set_response(audio_response)

        """ text IA text """
        outjson = audio_gpt.get_response()
        refined_speech = SpeechRefinement.refine_speech_textOpenAI(outjson["text"])
        system = "Vas a leer una llamada de un agente de cobranzas exitosa. Dame los patrones que permitieron que eso sea posible. Ten en cuenta que la llamada fue traducida por whisper-1 (speechToText)"
        chat_gpt = ChatGPTRequestModel(system, refined_speech, audio_file[0])
        chat_response = OpenAIRequestCreator.chat_request(chat_gpt)
        chat_gpt.set_response(chat_response)

        """  Patterns """
        PatternController.countWords(audio_file[0])


"""

--gestiones con pago
select c.serial_ced, a.accion_ges, a.respuesta_ges, a.telefono_ges, a.fecha_ges, b.id_arbol, a.cedente
from CEDENTE c inner join  GESTIONES a on c.nombre_ced=a.cedente inner join ARBOL b on a.accion_ges=b.accion_arbol and a.respuesta_ges=b.descripcion_arbol and a.tipo_ges = 1 and b.cod_accion = 1 and b.seleccionable_arbol='TRUE'
where b.id_cedente like '%,'+cast(c.serial_ced as nvarchar(5))+',%' and convert(date,a.fecha_ges,120)=convert(date,'2023-04-28',120) --and a.cedente='COOP_JEP'
order by a.fecha_ges DESC

--traducir grabaciones a texto QA
select id_gestion, accion_ges, respuesta_ges, telefono_ges, fecha_ges, cedente, serial_ced from CEDENTE a inner join GESTIONES b  on a.nombre_ced=b.cedente where tipo_ges = 1 and convert(date,fecha_ges,120)=convert(date,'2023-04-28',120) and cedente='COOP_JEP'
select count(id_gestion) from GESTIONES  where tipo_ges = 1 and convert(date,fecha_ges,120)=convert(date,'2023-04-28',120) and cedente='COOP_JEP'

select * from CCALIDAD_PALABRA -- resta puntos a la calificacion de la gestion
--select * from CCALIDAD_FRASE where etiqueta_ccf='SALUDO' and serial_ced=235 and tipo_ccf='ACTIVO'
select * from CCALIDAD_FRASE where serial_ced=235 and tipo_ccf='ACTIVO' order by etiqueta_ccf

select top 10 * from CALIFICA_GESTION


--server: 192.168.0.198
--user: userphp
--pass: Siccec2014


select top 10 * from GESTIONES

"""