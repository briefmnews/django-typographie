from typographie.admin import apply_typographie_to_dict


class TestApplyTypographieToDict:
    def test_null_typographiable_fields_are_preserved(self):
        # GIVEN
        data = {
            "image": {
                "caption": None,
                "credit": None,
                "url": "https://example.com/image.jpg",
            },
            "title": "Un titre",
        }
        fields = ["caption", "credit", "title"]

        # WHEN
        result = apply_typographie_to_dict(data, fields)

        # THEN
        assert result["image"]["caption"] is None
        assert result["image"]["credit"] is None
        assert result["image"]["url"] == "https://example.com/image.jpg"
        assert result["title"] == "Un titre"

    def test_null_items_in_list_are_preserved(self):
        # GIVEN
        data = {"blocks": [None, {"caption": None, "text": "Bonjour"}]}
        fields = ["caption", "text"]

        # WHEN
        result = apply_typographie_to_dict(data, fields)

        # THEN
        assert result["blocks"][0] is None
        assert result["blocks"][1]["caption"] is None
        assert result["blocks"][1]["text"] == "Bonjour"
