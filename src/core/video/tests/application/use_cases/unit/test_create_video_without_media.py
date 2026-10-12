from decimal import Decimal
from unittest.mock import create_autospec
import uuid
from uuid import UUID

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelationEntitiesNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


@pytest.fixture
def action_genre() -> Genre:
    return Genre(name="Action")


@pytest.fixture
def drama_genre() -> Genre:
    return Genre(name="Drama")


@pytest.fixture
def mock_genre_repository(action_genre, drama_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = [action_genre, drama_genre]
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = []
    return repository


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="Keanu Reeves", type=CastMemberType.ACTOR)


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(name="Lana Wachowski", type=CastMemberType.DIRECTOR)


@pytest.fixture
def mock_cast_member_repository(actor_cast_member, director_cast_member) -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = [actor_cast_member, director_cast_member]
    return repository


@pytest.fixture
def mock_empty_cast_member_repository() -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = []
    return repository


class TestCreateVideoWithoutMedia:
    def test_create_video_without_media_with_valid_data(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_genre_repository,
        mock_cast_member_repository,
        movie_category,
        action_genre,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id},
        )

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)
        mock_video_repository.save.assert_called_once_with(
            Video(
                id=output.id,
                title="The Matrix",
                description="A sci-fi classic movie",
                launch_year=1999,
                duration=Decimal("136.0"),
                published=False,
                rating=Rating.AGE_14,
                categories={movie_category.id},
                genres={action_genre.id},
                cast_members={actor_cast_member.id},
            )
        )

    def test_create_video_without_media_with_empty_collections(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_genre_repository,
        mock_cast_member_repository,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        output = use_case.execute(input)

        assert isinstance(output.id, UUID)
        mock_video_repository.save.assert_called_once_with(
            Video(
                id=output.id,
                title="The Matrix",
                description="A sci-fi classic movie",
                launch_year=1999,
                duration=Decimal("136.0"),
                published=False,
                rating=Rating.AGE_14,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )
        )

    def test_when_categories_do_not_exist_then_raise_relation_entities_not_found(
        self,
        mock_video_repository,
        mock_empty_category_repository,
        mock_genre_repository,
        mock_cast_member_repository,
        action_genre,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_empty_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        non_existent_category_id = uuid.uuid4()
        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={non_existent_category_id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id},
        )

        with pytest.raises(RelationEntitiesNotFound, match="^Categories with provided IDs not found$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == "Categories with provided IDs not found"
        mock_video_repository.save.assert_not_called()

    def test_when_cast_members_do_not_exist_then_raise_relation_entities_not_found(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_genre_repository,
        mock_empty_cast_member_repository,
        movie_category,
        action_genre,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_empty_cast_member_repository,
        )

        non_existent_cast_member_id = uuid.uuid4()
        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={non_existent_cast_member_id},
        )

        with pytest.raises(RelationEntitiesNotFound, match="^Cast members with provided IDs not found$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == "Cast members with provided IDs not found"
        mock_video_repository.save.assert_not_called()

    def test_when_genres_do_not_exist_then_raise_relation_entities_not_found(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_empty_genre_repository,
        mock_cast_member_repository,
        movie_category,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_empty_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        non_existent_genre_id = uuid.uuid4()
        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={non_existent_genre_id},
            cast_members={actor_cast_member.id},
        )

        with pytest.raises(RelationEntitiesNotFound, match="^Genres with provided IDs not found$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == "Genres with provided IDs not found"
        mock_video_repository.save.assert_not_called()

    def test_when_categories_and_cast_members_do_not_exist_then_raise_multiple_notifications(
        self,
        mock_video_repository,
        mock_empty_category_repository,
        mock_genre_repository,
        mock_empty_cast_member_repository,
        action_genre,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_empty_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_empty_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={uuid.uuid4()},
            genres={action_genre.id},
            cast_members={uuid.uuid4()},
        )

        expected_message = "Categories with provided IDs not found,Cast members with provided IDs not found"
        with pytest.raises(RelationEntitiesNotFound, match=f"^{expected_message}$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == expected_message
        mock_video_repository.save.assert_not_called()

    def test_when_categories_and_genres_do_not_exist_then_raise_multiple_notifications(
        self,
        mock_video_repository,
        mock_empty_category_repository,
        mock_empty_genre_repository,
        mock_cast_member_repository,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_empty_category_repository,
            genre_repository=mock_empty_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={uuid.uuid4()},
            genres={uuid.uuid4()},
            cast_members={actor_cast_member.id},
        )

        expected_message = "Categories with provided IDs not found,Genres with provided IDs not found"
        with pytest.raises(RelationEntitiesNotFound, match=f"^{expected_message}$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == expected_message
        mock_video_repository.save.assert_not_called()

    def test_when_cast_members_and_genres_do_not_exist_then_raise_multiple_notifications(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_empty_genre_repository,
        mock_empty_cast_member_repository,
        movie_category,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_empty_genre_repository,
            cast_member_repository=mock_empty_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={uuid.uuid4()},
            cast_members={uuid.uuid4()},
        )

        expected_message = "Cast members with provided IDs not found,Genres with provided IDs not found"
        with pytest.raises(RelationEntitiesNotFound, match=f"^{expected_message}$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == expected_message
        mock_video_repository.save.assert_not_called()

    def test_when_all_related_entities_do_not_exist_then_raise_all_notifications(
        self,
        mock_video_repository,
        mock_empty_category_repository,
        mock_empty_genre_repository,
        mock_empty_cast_member_repository,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_empty_category_repository,
            genre_repository=mock_empty_genre_repository,
            cast_member_repository=mock_empty_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="The Matrix",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={uuid.uuid4()},
            genres={uuid.uuid4()},
            cast_members={uuid.uuid4()},
        )

        expected_message = (
            "Categories with provided IDs not found,"
            "Cast members with provided IDs not found,"
            "Genres with provided IDs not found"
        )
        with pytest.raises(RelationEntitiesNotFound, match=f"^{expected_message}$") as exc_info:
            use_case.execute(input)

        assert str(exc_info.value) == expected_message
        mock_video_repository.save.assert_not_called()

    def test_when_video_is_invalid_with_empty_title_then_raise_invalid_video(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_genre_repository,
        mock_cast_member_repository,
        movie_category,
        action_genre,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="",
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id},
        )

        with pytest.raises(InvalidVideo, match="title cannot be empty") as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidVideo
        assert "title cannot be empty" in str(exc_info.value)
        mock_video_repository.save.assert_not_called()

    def test_when_video_is_invalid_with_title_longer_than_255_then_raise_invalid_video(
        self,
        mock_video_repository,
        mock_category_repository,
        mock_genre_repository,
        mock_cast_member_repository,
        movie_category,
        action_genre,
        actor_cast_member,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository,
        )

        input = CreateVideoWithoutMedia.Input(
            title="a" * 256,
            description="A sci-fi classic movie",
            launch_year=1999,
            duration=Decimal("136.0"),
            rating=Rating.AGE_14,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id},
        )

        with pytest.raises(InvalidVideo, match="title cannot be longer than 255") as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidVideo
        assert "title cannot be longer than 255" in str(exc_info.value)
        mock_video_repository.save.assert_not_called()
