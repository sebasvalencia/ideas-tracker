from datetime import datetime
from src.app.application.idea.ports import IdeaRecord


class InMemoryIdeaRepository:
    def __init__(self) -> None:
        self._seq = 0
        self._items: list[IdeaRecord] = []

    def create(self, *, owner_id: int, title: str, description: str) -> IdeaRecord:
        self._seq += 1
        now = datetime.now()
        item = IdeaRecord(
            id=self._seq,
            owner_id=owner_id,
            title=title,
            description=description,
            status="idea",
            execution_percentage=0.0,
            created_at=now,
            updated_at=now,
            deleted_at=None,
        )
        self._items.append(item)
        return item

    def list_active(self, *, owner_id: int, status: str | None, limit: int, offset: int) -> list[IdeaRecord]:
        rows = [item for item in self._items if item.owner_id == owner_id and item.deleted_at is None]
        if status is not None:
            rows = [item for item in rows if item.status == status]
        rows.sort(key=lambda item: item.created_at, reverse=True)
        return rows[offset : offset + limit]

    def get_active_by_id(self, *, idea_id: int) -> IdeaRecord | None:
        item = next((row for row in self._items if row.id == idea_id and row.deleted_at is None), None)
        return item

    def update(self, *, idea: IdeaRecord) -> IdeaRecord:
        for idx, existing in enumerate(self._items):
            if existing.id == idea.id:
                self._items[idx] = idea
                return idea
        raise ValueError(f"Idea with id {idea.id} not found")

    def soft_delete(self, *, idea_id: int, deleted_at: datetime) -> None:
        item = self.get_active_by_id(idea_id=idea_id)
        if item is None:
            return
        self.update(
            idea=IdeaRecord(
                id=item.id,
                owner_id=item.owner_id,
                title=item.title,
                description=item.description,
                status=item.status,
                execution_percentage=item.execution_percentage,
                created_at=item.created_at,
                updated_at=deleted_at,
                deleted_at=deleted_at,
            )
        )