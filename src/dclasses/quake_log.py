from dataclasses import dataclass, field, is_dataclass
import json


@dataclass
class QuakeLog:
    game_id: int
    # Save the players in a set to avoid duplicates (if a player connects more than once)
    players: set[str] = field(default_factory=set)
    kills: dict[str, int] = field(default_factory=dict)
    world_kill_count: int = 0

    def to_dict(self) -> dict[str, dict]:
        return {
            f"game_{self.game_id}": {
                "total_kills": sum(self.kills.values()),
                "players": list(self.players),
                "kills": self.kills,
                "world_kill_count": self.world_kill_count,
            }
        }

class QuakeLogEncoder(json.JSONEncoder):
    """
    Provides a custom JSON encoder for QuakeLog dataclass instances.
    """
    def default(self, obj):
        # If the object is a dataclass instance, convert it to a dictionary
        # which is serialized by the JSON encoder.
        if is_dataclass(obj):
            return obj.to_dict()
        return super().default(obj)
