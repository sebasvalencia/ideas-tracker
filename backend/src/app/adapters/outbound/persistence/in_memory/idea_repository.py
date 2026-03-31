from datetime import datetime
from src.app.application.idea.ports import IdeaRecord

class InMemoryIdeaRepository:
    def __init__(self) -> None:
        self._seq = 0
        self._items: list[IdeaRecord] = []
    
    def create(self, *, owner_id: int, title:str, description:str) -> IdeaRecord:
        self._seq += 1
        item = IdeaRecord(
            id=self._seq,
            owner_id=owner_id,
            title=title,
            description=description,
            status="idea",
            execution_percentage=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None,
        )
        self._items.append(item)
        return item
    
    def find_by_id(self, id: int) -> IdeaRecord | None:
        return next((item for item in self._items if item.id == id), None)
    
    def find_all(self) -> list[IdeaRecord]:
        return list(self._items)
    
    def update(self, *, id: int, owner_id: int, title:str, description:str) -> IdeaRecord:
        item = self.find_by_id(id)
        if item is None:
            raise ValueError(f"Idea with id {id} not found")