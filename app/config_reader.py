
import toml

class config:
    

    data = toml.load("config.toml")
    PHONE_NUMBER = data.get("PHONE_NUMBER", '')
    OUTPUT_GROUP_ID = data.get("OUTPUT_GROUP_ID", '')