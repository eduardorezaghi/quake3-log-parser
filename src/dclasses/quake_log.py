import json
from dataclasses import dataclass, field, is_dataclass


@dataclass
class QuakeLog:
    game_id: int
    # Save the players in a set to avoid duplicates (if a player connects more than once)
    players: set[str] = field(default_factory=set)
    kills_score: dict[str, int] = field(default_factory=dict)
    kills_by_means: dict[str, int] = field(default_factory=dict)
    _total_kills: int = 0

    @property
    def get_total_kills(self) -> int:
        return self._total_kills + self.kills_score.get("<world>", 0)

    @property
    def get_kill_by_player(self) -> dict[str, int]:
        # Create a copy of the kills dictionary to avoid modifying the original,
        # and remove the "<world>" key from the copy
        kills = self.kills_score.copy()
        kills.pop("<world>", None)

        return dict(
            # Sorts the kills dictionary by the number of kills in descending order
            sorted(
                kills.items(),
                # Uses the number of kills as the sorting key
                key=lambda item: item[1],
                # Descending order (highest number of kills first)
                reverse=True,
            )
        )

    @property
    def get_kill_by_means_report(self) -> dict[str, int]:
        return dict(
            # Sorts the kills by means dictionary by the number of kills in descending order
            sorted(
                self.kills_by_means.items(),
                # Uses the number of kills as the sorting key
                key=lambda item: item[1],
                # Descending order (highest number of kills first)
                reverse=True,
            )
        )

    def kill_by_means_dict(self) -> dict[str, dict]:
        return {
            f"game_{self.game_id}": {"kills_by_means": self.get_kill_by_means_report}
        }

    def to_dict(self) -> dict[str, dict]:
        return {
            f"game_{self.game_id}": {
                "total_kills": self.get_total_kills,
                "players": list(self.players),
                "kills": self.get_kill_by_player,
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
