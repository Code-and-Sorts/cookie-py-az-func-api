
from typing import List
from repositories import MeowRepository
from models import Meow, MeowResponse


class MeowService:
    def __init__(self, repository: MeowRepository):
        self.repository = repository

    def get_by_id(self, item_id: str) -> MeowResponse:
        return self.repository.get_by_id(item_id)

    def get_list(self) -> List[MeowResponse]:
        return self.repository.get_list()

    def create(self, item: Meow) -> MeowResponse:
        return self.repository.create(item)

    def update(self, item: Meow) -> MeowResponse:
        return self.repository.update(item)

    def soft_delete(self, item_id: str):
        self.repository.delete(item_id)
