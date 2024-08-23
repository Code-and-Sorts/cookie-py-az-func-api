from typing import List
import azure.functions as func
from services import MeowService
from models import MeowResponse, Meow, MeowIdValidation

class MeowController:
    def __init__(self, service: MeowService):
        self.service = service

    def get_by_id(self, req: func.HttpRequest) -> MeowResponse:
        item_id: str = req.route_params.get('item_id')
        MeowIdValidation(id=item_id)
        return self.service.get_by_id(item_id)

    def get_list(self) -> List[MeowResponse]:
        return self.service.get_list()

    def create(self, req: func.HttpRequest) -> MeowResponse:
        item_json = req.get_json()
        item = Meow(**item_json)
        return self.service.create(item)

    def update(self, req: func.HttpRequest) -> MeowResponse:
        item_id = req.route_params.get('item_id')
        item_data = req.get_json()
        item = Meow(**item_data)
        item.id = item_id
        return self.service.update(item)

    def soft_delete(self, req: func.HttpRequest):
        item_id = req.route_params.get('item_id')
        self.service.soft_delete(item_id)
