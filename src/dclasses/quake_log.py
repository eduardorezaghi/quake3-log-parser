from dataclasses import dataclass, field


@dataclass
class QuakeLog:
    game_id: int
    # Save the players in a set to avoid duplicates (if a player connects more than once)
    players: set[str] = field(default_factory=set)
    kills: dict[str, int] = field(default_factory=dict)
    world_kill_count: int = 0

    def __dict__(self) -> str:
        return {
            f"game_{self.game_id}": {
                "total_kills": sum(self.kills.values()),
                "players": list(self.players),
                "kills": self.kills,
                "world_kill_count": self.world_kill_count,
            }
        }
