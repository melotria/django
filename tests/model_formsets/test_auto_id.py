from django.test import TestCase
from django.forms.models import inlineformset_factory
from .models import Author, Book

class InlineFormsetAutoIdTest(TestCase):
    def test_inline_formset_auto_id(self):
        """Test that BaseInlineFormSet accepts the auto_id parameter."""
        # Create an inline formset with a custom auto_id
        AuthorBooksFormSet = inlineformset_factory(
            Author, Book, can_delete=False, extra=1, fields="__all__"
        )
        author = Author.objects.create(name="Test Author")

        # Test with default auto_id
        formset = AuthorBooksFormSet(instance=author)
        self.assertEqual(formset.auto_id, "id_%s")

        # Test with custom auto_id
        custom_auto_id = "custom_%s"
        formset = AuthorBooksFormSet(instance=author, auto_id=custom_auto_id)
        self.assertEqual(formset.auto_id, custom_auto_id)

        # Verify that the auto_id is used in the rendered form
        form_html = formset.forms[0].as_p()
        self.assertIn(f'id="custom_book_set-0-title"', form_html)
