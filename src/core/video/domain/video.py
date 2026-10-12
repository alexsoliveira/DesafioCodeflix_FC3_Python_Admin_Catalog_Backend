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

from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
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

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self):
            self.validate()

    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255")
            
        if not self.title:
            self.notification.add_error("title cannot be empty")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(self, title, description, launch_year, duration, published, rating):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating

        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def add_genre(self, genre_id: UUID):
        self.genres.add(genre_id)
        self.validate()

    def add_cast_member(self, cast_member_id: UUID):
        self.cast_members.add(cast_member_id)
        self.validate()

    def update_banner(self, banner: ImageMedia):
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia):
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia):
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia):
        self.trailer = trailer
        self.validate()

    def update_video(self, video: AudioVideoMedia):
        self.video = video
        self.validate()


    
            

    