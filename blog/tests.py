from django.test import TestCase
from blog.models import Category, Post

# Create your tests here.
class BlogTest(TestCase):

    #Test whether created Category object's title matches expected title
    def create_category(self, name="Janine Desiree"):
        return Category.objects.create(name=name)

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.name)

    #Test whether the name set is what will be displayed
    def test_category_representation(self):
        category = Category(name="My category title")
        self.assertEqual(str(category), category.name)

    def test_post_title_representation(self):
        post = Post(title="My category title")
        self.assertEqual(str(post), post.title)
