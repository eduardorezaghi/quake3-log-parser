import json
from dataclasses import dataclass, field, is_dataclass


@dataclass
class QuakeLog:
    game_id: int
    # Save the players in a set to avoid duplicates (if a player connects more than once)
    players: set[str] = field(default_factory=set)
    kills: dict[str, int] = field(default_factory=dict)
    total_kills: int = 0

    def to_dict(self) -> dict[str, dict]:
        return {
            f"game_{self.game_id}": {
                "total_kills": self.total_kills + self.kills.get("<world>", 0),
                "players": list(self.players),
                "kills": dict(
                    # Sorts the kills dictionary by the number of kills in descending order
                    sorted(
                        # Remove the <world> player from the kills dictionary, but keep the kills totalized
                        {
                            player: kills
                            for player, kills in self.kills.items()
                            if player != "<world>"
                        }.items(),
                        # Uses the number of kills as the sorting key
                        key=lambda item: item[1],
                        # Descending order (highest number of kills first)
                        reverse=True,
                    )
                ),
            }
        }


# Don't worry about the QuakeLogEncoder class,
# because it only exists to provide a custom JSON encoder for QuakeLog dataclass instances.
class QuakeLogEncoder(json.JSONEncoder):  # pragma: no cover
    """
    Provides a custom JSON encoder for QuakeLog dataclass instances.
    """

    def default(self, obj):
        # If the object is a dataclass instance, convert it to a dictionary
        # which is serialized by the JSON encoder.
        if is_dataclass(obj):
            return obj.to_dict()
        return super().default(obj)
