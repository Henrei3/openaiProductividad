from marshmallow import Schema, fields


class WavModel:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

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

        return WavModel(name, path)


class WavModelSchema(Schema):
    name = fields.String()
    path = fields.String()
