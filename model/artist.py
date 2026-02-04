from dataclasses import dataclass

@dataclass
class Artist:
    artist_id : str
    name : str

    def __str__(self):
        return f"{self.artist_id}, {self.name}"

    def __repr__(self):
        return f"{self.artist_id}, {self.name}"

    def __hash__(self):
        return hash(self.artist_id)