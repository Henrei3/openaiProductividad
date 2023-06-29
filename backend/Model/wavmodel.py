from marshmallow import Schema, fields


class WavModel:
    def __init__(self, name: str, path: str, size: float = None, cedente: str = None):
        self.name = name
        self.path = path
        self.size = size
        self.cedente = cedente

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def deserialize(self):
        wav_schema = WavModelSchema()
        return wav_schema.dump(self)

    @staticmethod
    def serialize(json_wav_model: dict):
        name = json_wav_model["name"]
        path = json_wav_model["path"]
        size = json_wav_model["size"]
        cedente = json_wav_model["cedente"]
        return WavModel(name, path, size, cedente)


class WavModelSchema(Schema):
    name = fields.String()
    path = fields.String()
    size = fields.Float()
    cedente = fields.String()

