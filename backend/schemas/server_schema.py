from pydantic import BaseModel, ConfigDict


class ServerResponse(BaseModel):
    id:int
    server_name :str
    is_premium : bool
    server_country :str

    model_config = {
        "from_attributes": True  # ORM objesinden veri alınmasını sağlar
    }

