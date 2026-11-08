"""
- Value Objects:
    - Rating: ENUM (ER, L, AGE_10, AGE_12, AGE_14, AGE_16, AGE_18)
    - ImageMedia:
        - Checksum: String
        - Name: String
        - Location: String
    - AudioVideoMedia:
        - Name: String
        - RawLocation: String
        - EncondedLocation: String
        - Status: MediaStatus: ENUM (PENDING, PROCESSING, COMPLETED, ERROR)

"""

from dataclasses import dataclass
from enum import StrEnum, auto, unique

@unique
class MediaStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()

@unique
class Rating(StrEnum):
    ER = auto()
    L = auto()
    AGE_10 = auto()
    AGE_12 = auto()
    AGE_14 = auto()
    AGE_16 = auto()
    AGE_18 = auto()

@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"
    BANNER = "BANNER"
    THUMBNAIL = "THUMBNAIL"
    THUMBNAIL_HALF = "THUMBNAIL_HALF"

@dataclass(frozen=True)
class ImageMedia:
    checksum: str
    name: str
    location: str

@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType = MediaType.VIDEO

    def complete(self, encoded_location: str):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=encoded_location,
            status=MediaStatus.COMPLETED,
            media_type=self.media_type,
        )

    def fail(self):
        return AudioVideoMedia(
            name=self.name,
            raw_location=self.raw_location,
            encoded_location=self.encoded_location,
            status=MediaStatus.ERROR,
            media_type=self.media_type,
        )
