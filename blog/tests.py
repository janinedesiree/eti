from django.test import TestCase
from blog.apps import BlogConfig
from blog.models import Category, Post, Comment

from projects.apps import ProjectsConfig
from projects.models import Project

import time
import datetime

from django.test import Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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

class PostTest(TestCase):
    def create_new_post():
        post = Post(title='Valid Post',
                body='An actual valid post',
                created_on=datetime.datetime.now(),
                last_modified=datetime.datetime.now())
        comment = Comment(author='Test Author',
                          body='A test comment! You\'re so cooL!',
                          created_on=datetime.datetime.now())
        comment.post = post
        post.save()
        category = Category(name="TestCategory")
        category.save()
        post.categories.add(category)
        post.save()
        response = client.get(reverse('blog_detail', kwargs={'pk': post.id}))
        assert response.status_code == 200
