import unittest # std library
import uuid
import pytest
from uuid import UUID

from core.category.domain.category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

        # with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
        #     Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Filmes")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="Filmes")
        assert category.name == "Filmes"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Filmes")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filmes",
            description="Filmes em geral",
            is_active=False,
        )

        assert category.id == cat_id
        assert category.name == "Filmes"
        assert category.description == "Filmes em geral"
        assert category.is_active is False
        # self.assertEqual(category.id, cat_id)
        # self.assertEqual(category.name, "Filmes")
        # self.assertEqual(category.description, "Filmes em geral")
        # self.assertEqual(category.is_active, False)

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")


    def test_category_string_representation(self):
        category = Category(name="Filmes", description="Filmes em geral", is_active=False)
        assert str(category) == "Filmes -Filmes em geral (False)"

    def test_category_repr_representation(self):
        cat_id = uuid.uuid4()
        category = Category(id=cat_id, name="Filmes")
        assert repr(category) == f"<Category: Filmes ({cat_id})>"
        # self.assertEqual(repr(category), f"<Category: Filmes ({cat_id})>")


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")

        category.update_category(name="Série", description="Séries em geral")

        assert category.name == "Série"
        assert category.description == "Séries em geral"

    def test_update_category_with_invalid_name(self):
        category = Category(name="Filme", description="Filmes em geral")

        with pytest.raises(ValueError, match="name cannot be longer than 255 characters"):
            category.update_category(name="a" * 256, description="Séries em geral")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

class TestActivateCategory:
    def test_activate_inactive_category(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=False,
        )

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=True,
        )

        category.activate()

        assert category.is_active is True

class TestDeactivateCategory:
    def test_deactivate_active_category(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=True,
        )

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="Filme", 
            description="Filmes em geral",
            is_active=False,
        )

        category.deactivate()

        assert category.is_active is False

class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(id=common_id, name="Filme")
        category_2 = Category(id=common_id, name="Filme")

        assert category_1 == category_2

    def test_equality_different_classes (self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(id=common_id, name="Filme")
        dummy = Dummy()
        dummy.id = common_id
        assert category != dummy