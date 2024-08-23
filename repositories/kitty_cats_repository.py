from azure.cosmos import ContainerProxy
from azure.cosmos.exceptions import CosmosAccessConditionFailedError
from typing import List, Optional
from models import Meow, MeowResponse
from errors import NotFoundError

class Database:
    def __init__(
            self,
            endpoint: str,
            key: str,
            name: str,
            container_name: str
        ):
            self._endpoint = endpoint
            self._key = key
            self.name = name
            self.container_name = container_name

class MeowRepository:
    def __init__(self, container_client: ContainerProxy):
        self.container_client = container_client

    def get_by_id(self, item_id: str) -> Optional[MeowResponse]:
        query = "SELECT * FROM c WHERE c.id = @id AND c.isDeleted = false"
        parameters = [
            { "name": "@id", "value": item_id }
        ]
        items = self.container_client.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        )
        for item in items:
            return MeowResponse.model_validate(item)

        raise NotFoundError()

    def get_list(self) -> List[MeowResponse | None]:
        query = "SELECT * FROM c WHERE c.isDeleted = false"
        items = self.container_client.query_items(query=query, enable_cross_partition_query=True)

        if items:
            return [MeowResponse.model_validate(item) for item in items]
        return []

    def create(self, item: Meow) -> MeowResponse:
        item_dict = item.model_dump(exclude_none=True)
        created_item = self.container_client.create_item(item_dict)

        return MeowResponse.model_validate(created_item)

    def update(self, item: Meow) -> Optional[MeowResponse]:
        new_item_dict = item.model_dump(exclude_none=True)
        previous_item = self.get_by_id(item.id)
        previous_item_dict = previous_item.model_dump(exclude_none=True)
        if not previous_item:
            raise NotFoundError()
        patched_item = {**previous_item_dict,**new_item_dict}
        updated_item = self.container_client.upsert_item(patched_item)

        return MeowResponse.model_validate(updated_item)

    def delete(self, item_id: str):
        filter = "from c WHERE c.isDeleted = false"
        operations: list[dict[str, str]] = [
            { 'op': 'replace', 'path': '/isDeleted', 'value': True }
        ]
        try:
            self.container_client.patch_item(
                item=item_id,
                partition_key=item_id,
                patch_operations=operations,
                filter_predicate=filter
            )
        except Exception as error:
            if isinstance(error, CosmosAccessConditionFailedError):
                raise NotFoundError()
