import uuid


async def FileNameGenerator(filename):
    extension = filename.split(".")[-1]
    id = uuid.uuid4()
    return f"{id}.{extension}"
