"""
- Atributos:
    - Title: String
    - Description: String
    - LaunchedAt: Year
    - Duration: Double
    - Rating: Rating
    - Opened: Boolean
    - Published: Boolean
    
    - Categories: Set<CategoryID | Category>
    - Genres: Set<GenreID | Genre>
    - CastMembers: Set<CastMemberID | CastMember>

    - Banner: ImageMedia
    - Thumbnail: ImageMedia
    - ThumbnailHalf: ImageMedia
    - Trailer: AudioVideoMedia
    - Video: AudioVideoMedia

- Value Objects:
    - Rating: ENUM (ER, L, AGE_10, AGE_12, AGE_14, AGE_16, AGE_18)
    - ImageMedia:
        - Id: UUID | String
        - Checksum: String
        - Name: String
        - Location: String
    - AudioVideoMedia:
        - Id: UUID | String
        - Checksum: String
        - Name: String
        - RawLocation: String
        - EncondedLocation: String
        - Status: MediaStatus: ENUM (PENDING, PROCESSING, COMPLETED, ERROR)

"""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.video.domain.value_objects import Rating
from src.core._shared.entity import Entity


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating
    

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

    # TODO: adicionar atributos de mídia

    def __post_init__(self):
            self.validate()

    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255")
            
        if not self.title:
            self.notification.add_error("title cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
            

    