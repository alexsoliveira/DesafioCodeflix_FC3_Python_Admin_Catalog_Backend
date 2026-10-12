
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.notification import Notification
from src.core.video.domain.video_repository import VideoRepository
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelationEntitiesNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video

class CreateVideoWithoutMedia:

    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    @dataclass
    class Output:
        id: UUID

    def __init__(
            self, 
            video_repository: VideoRepository,
            category_repository: CategoryRepository,
            genre_repository: GenreRepository,
            cast_member_repository: CastMemberRepository) -> None:
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository

    def execute(self, input: Input) -> Output:
        notification = Notification()

        self.validate_categories(input, notification)
        self.validate_cast_members(input, notification)
        self.validate_genres(input, notification)

        if notification.has_errors:
            raise RelationEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                published=False,
                rating=input.rating,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as err:
            raise InvalidVideo(err)

        self.video_repository.save(video)

        return self.Output(id=video.id)

    def validate_categories(self, input: Input, notification: Notification) -> None:
        category_ids = {category.id for category in self.category_repository.list()}
        if not category_ids.issubset(category_ids):
           notification.add_error("Categories with provided IDs not found")

    def validate_cast_members(self, input: Input, notification: Notification) -> None:
        cast_member_ids = {cast_member.id for cast_member in self.cast_member_repository.list()}
        if not input.cast_members.issubset(cast_member_ids):
           notification.add_error("Cast members with provided IDs not found")

    def validate_genres(self, input: Input, notification: Notification) -> None:
        genre_ids = {genre.id for genre in self.genre_repository.list()}
        if not input.genres.issubset(genre_ids):
            notification.add_error("Genres with provided IDs not found")