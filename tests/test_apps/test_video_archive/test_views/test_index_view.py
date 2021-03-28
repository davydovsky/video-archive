import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
def test_main_page(client: Client, main_heading: str) -> None:
    """This test ensures that main page works."""
    response = client.get('/')

    assert response.status_code == 200
    assert main_heading in str(response.content)


@pytest.mark.django_db()
def test_video_archive_page(client: Client, main_heading: str) -> None:
    """This test ensures that hello page works."""
    response = client.get(reverse('video_archive:video-feed'))

    assert response.status_code == 200
    assert main_heading in str(response.content)
