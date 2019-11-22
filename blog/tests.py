from django.test import TestCase
from blog.models import Category, Post

# Create your tests here.
class BlogTest(TestCase):
    #MODELS
    #Test whether created Category object's name matches expected name
    def create_category(self, name="Janine Desiree"):
        return Category.objects.create(name=name)

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.name)

    #Test whether created Post object's title matches expected title
    def create_post(self, title="je ne sais pas"):
        return Post.objects.create(title=title)

    def test_post_creation(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertEqual(p.__str__(), p.title)
