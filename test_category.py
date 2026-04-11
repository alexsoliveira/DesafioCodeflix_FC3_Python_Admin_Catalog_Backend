import unittest # std library
import uuid
import pytest
from uuid import UUID
from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Category()

        # with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
        #     Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must be less than 256 characters"):
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

    def test_category_string_representation(self):
        category = Category(name="Filmes", description="Filmes em geral", is_active=False)
        assert str(category) == "Filmes -Filmes em geral (False)"

    def test_category_repr_representation(self):
        cat_id = uuid.uuid4()
        category = Category(id=cat_id, name="Filmes")
        assert repr(category) == f"<Category: Filmes ({cat_id})>"
        # self.assertEqual(repr(category), f"<Category: Filmes ({cat_id})>")


# if __name__ == "__main__":
#     unittest.main()