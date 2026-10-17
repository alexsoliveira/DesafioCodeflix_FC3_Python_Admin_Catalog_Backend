import dataclasses
import uuid
from decimal import Decimal
from uuid import UUID

import pytest

from src.core.video.domain.value_objects import (
    AudioVideoMedia,
    ImageMedia,
    MediaStatus,
    Rating,
)
from src.core.video.domain.video import Video


class TestRating:
    def test_rating_enum_has_all_expected_values(self):
        assert set(Rating) == {
            Rating.ER,
            Rating.L,
            Rating.AGE_10,
            Rating.AGE_12,
            Rating.AGE_14,
            Rating.AGE_16,
            Rating.AGE_18,
        }

    @pytest.mark.parametrize(
        "rating",
        [
            Rating.ER,
            Rating.L,
            Rating.AGE_10,
            Rating.AGE_12,
            Rating.AGE_14,
            Rating.AGE_16,
            Rating.AGE_18,
        ],
    )
    def test_rating_enum_is_instance_of_rating(self, rating):
        assert isinstance(rating, Rating)


class TestMediaStatus:
    def test_media_status_enum_has_all_expected_values(self):
        assert set(MediaStatus) == {
            MediaStatus.PENDING,
            MediaStatus.PROCESSING,
            MediaStatus.COMPLETED,
            MediaStatus.ERROR,
        }

    @pytest.mark.parametrize(
        "status",
        [
            MediaStatus.PENDING,
            MediaStatus.PROCESSING,
            MediaStatus.COMPLETED,
            MediaStatus.ERROR,
        ],
    )
    def test_media_status_enum_is_instance_of_media_status(self, status):
        assert isinstance(status, MediaStatus)


class TestImageMedia:
    def test_create_image_media(self):
        image = ImageMedia(
            checksum="a1b2c3d4",
            name="banner.png",
            location="/images/banner.png",
        )

        assert image.checksum == "a1b2c3d4"
        assert image.name == "banner.png"
        assert image.location == "/images/banner.png"

    def test_image_media_is_immutable(self):
        image = ImageMedia(
            checksum="a1b2c3d4",
            name="banner.png",
            location="/images/banner.png",
        )

        with pytest.raises(dataclasses.FrozenInstanceError):
            image.name = "new_banner.png"

    def test_image_media_equality(self):
        image_1 = ImageMedia(
            checksum="a1b2c3d4",
            name="banner.png",
            location="/images/banner.png",
        )
        image_2 = ImageMedia(
            checksum="a1b2c3d4",
            name="banner.png",
            location="/images/banner.png",
        )

        assert image_1 == image_2

    def test_image_media_inequality(self):
        image_1 = ImageMedia(
            checksum="a1b2c3d4",
            name="banner.png",
            location="/images/banner.png",
        )
        image_2 = ImageMedia(
            checksum="different",
            name="banner.png",
            location="/images/banner.png",
        )

        assert image_1 != image_2


class TestAudioVideoMedia:
    def test_create_audio_video_media(self):
        media = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.PENDING,
        )

        assert media.checksum == "e5f6g7h8"
        assert media.name == "trailer.mp4"
        assert media.raw_location == "/raw/trailer.mp4"
        assert media.encoded_location == "/encoded/trailer.mp4"
        assert media.status == MediaStatus.PENDING

    def test_audio_video_media_is_immutable(self):
        media = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.PENDING,
        )

        with pytest.raises(dataclasses.FrozenInstanceError):
            media.status = MediaStatus.COMPLETED

    def test_audio_video_media_equality(self):
        media_1 = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.PROCESSING,
        )
        media_2 = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.PROCESSING,
        )

        assert media_1 == media_2

    def test_audio_video_media_inequality(self):
        media_1 = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.PENDING,
        )
        media_2 = AudioVideoMedia(
            checksum="e5f6g7h8",
            name="trailer.mp4",
            raw_location="/raw/trailer.mp4",
            encoded_location="/encoded/trailer.mp4",
            status=MediaStatus.COMPLETED,
        )

        assert media_1 != media_2


class TestVideo:
    def test_title_is_required(self):
        with pytest.raises(TypeError, match="missing 9 required positional arguments"):
            Video()

    def test_video_must_be_created_with_id_as_uuid_by_default(self):
        video = Video(
            title="The Matrix",
            description="A sci-fi classic",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert isinstance(video.id, UUID)

    def test_create_video_with_provided_values(self):
        video_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre_id = uuid.uuid4()
        cast_member_id = uuid.uuid4()

        video = Video(
            id=video_id,
            title="The Matrix",
            description="A computer hacker learns from mysterious rebels about the true nature of his reality.",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )

        assert video.id == video_id
        assert video.title == "The Matrix"
        assert video.description == "A computer hacker learns from mysterious rebels about the true nature of his reality."
        assert video.launch_year == 1999
        assert video.duration == Decimal("136.0")
        assert video.published is True
        assert video.rating == Rating.AGE_14
        assert video.categories == {category_id}
        assert video.genres == {genre_id}
        assert video.cast_members == {cast_member_id}

    @pytest.mark.parametrize(
        "rating",
        [
            Rating.ER,
            Rating.L,
            Rating.AGE_10,
            Rating.AGE_12,
            Rating.AGE_14,
            Rating.AGE_16,
            Rating.AGE_18,
        ],
    )
    def test_create_video_with_different_ratings(self, rating):
        video = Video(
            title="Any Title",
            description="Any description",
            launch_year=2024,
            duration=Decimal("120.0"),
            published=False,
            rating=rating,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video.rating == rating

    def test_cannot_create_video_with_empty_title(self):
        with pytest.raises(ValueError, match="title cannot be empty"):
            Video(
                title="",
                description="Some description",
                launch_year=2020,
                duration=Decimal("90.0"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_title_cannot_be_longer_than_255_characters(self):
        with pytest.raises(ValueError, match="title cannot be longer than 255"):
            Video(
                title="a" * 256,
                description="Some description",
                launch_year=2020,
                duration=Decimal("90.0"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_title_with_exact_255_characters_is_valid(self):
        video = Video(
            title="a" * 255,
            description="Some description",
            launch_year=2020,
            duration=Decimal("90.0"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video.title == "a" * 255

    def test_valid_video_has_no_notification_errors(self):
        video = Video(
            title="The Matrix",
            description="A sci-fi classic",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video.notification.has_errors is False

    def test_create_video_with_multiple_associated_entities(self):
        cat_1 = uuid.uuid4()
        cat_2 = uuid.uuid4()
        genre_1 = uuid.uuid4()
        genre_2 = uuid.uuid4()
        cast_1 = uuid.uuid4()
        cast_2 = uuid.uuid4()

        video = Video(
            title="Inception",
            description="A thief who steals corporate secrets through dream-sharing.",
            launch_year=2010,
            duration=Decimal("148.0"),
            published=True,
            rating=Rating.AGE_14,
            categories={cat_1, cat_2},
            genres={genre_1, genre_2},
            cast_members={cast_1, cast_2},
        )

        assert video.categories == {cat_1, cat_2}
        assert video.genres == {genre_1, genre_2}
        assert video.cast_members == {cast_1, cast_2}


class TestEquality:
    def test_when_videos_have_same_id_and_attributes_they_are_equal(self):
        common_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre_id = uuid.uuid4()
        cast_member_id = uuid.uuid4()

        video_1 = Video(
            id=common_id,
            title="The Matrix",
            description="Sci-fi",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )
        video_2 = Video(
            id=common_id,
            title="The Matrix",
            description="Sci-fi",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )

        assert video_1 == video_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        video = Video(
            id=common_id,
            title="The Matrix",
            description="Sci-fi",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        dummy = Dummy()
        dummy.id = common_id

        assert video != dummy

    def test_when_videos_have_different_id_they_are_not_equal(self):
        video_1 = Video(
            id=uuid.uuid4(),
            title="The Matrix",
            description="Sci-fi",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_2 = Video(
            id=uuid.uuid4(),
            title="The Matrix",
            description="Sci-fi",
            launch_year=1999,
            duration=Decimal("136.0"),
            published=True,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video_1 != video_2
