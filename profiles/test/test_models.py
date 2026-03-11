from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.templatetags.static import static
from django.test import TestCase

from ..models import Follow, UserProfile


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testuser",
            first_name="juan",
            last_name="garcia",
        )

        self.user2 = User.objects.create_user(
            username="testuser2", password="testuser2"
        )

        self.profile1 = UserProfile.objects.create(user=self.user)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_profile_full_name_title_is_capitalized(self):
        self.assertEqual(self.profile1.full_name_title, "Juan Garcia")

    def test_profile_image_url_returns_default_when_no_picture(self):
        self.assertEqual(
            self.profile1.profile_image_url, static("img/default_profile.png")
        )

    def test_profile_image_url_returns_picture_when_exists(self):
        image = SimpleUploadedFile(
            name="text.jpg", content=b"file_content", content_type="image/jpeg"
        )

        self.profile1.profile_picture = image
        self.profile1.save()

        self.assertNotEqual(
            self.profile1.profile_image_url, static("img/default_profile.png")
        )


class FollowModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="123")
        self.user2 = User.objects.create_user(username="user2", password="123")
        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_cannot_create_duplicate_follow(self):
        Follow.objects.create(follower=self.profile1, following=self.profile2)

        with self.assertRaises(IntegrityError):
            Follow.objects.create(follower=self.profile1, following=self.profile2)
