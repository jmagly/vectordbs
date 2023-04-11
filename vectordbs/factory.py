import os
import json
from abc import ABC, abstractmethod
from typing import Type
from datastore import DataStore

class VectorDataStore(ABC, DataStore):
    # (same as previous implementation)

class DataStoreFactory():
    @staticmethod
    async def get_datastore() -> DataStore:
        datastore = os.environ.get("DATASTORE")
        assert datastore is not None
        
        with open('mapping.json', 'r') as file:
            mapping = json.load(file)

        class_path = mapping.get(datastore)
        if class_path is not None:
            module_name, class_name = class_path.rsplit('.', 1)
            try:
                datastore_module = __import__(module_name, fromlist=[class_name])
                datastore_class: Type[VectorDataStore] = getattr(datastore_module, class_name)

                if issubclass(datastore_class, VectorDataStore):
                    return datastore_class()
                else:
                    raise TypeError(f"Class {class_name} is not a subclass of VectorDataStore")

            except (ModuleNotFoundError, AttributeError) as e:
                raise ValueError(f"Unsupported vector database: {datastore}") from e
        else:
            raise ValueError(f"Unsupported vector database: {datastore}")
