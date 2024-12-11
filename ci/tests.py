import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Name

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_name():
    def make_name(**kwargs):
        return Name.objects.create(**kwargs)
    return make_name


@pytest.mark.django_db
def test_list_names(api_client, create_name):
    create_name(name="John Doe")
    create_name(name="Jane Doe")

    response = api_client.get("/api/names/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "John Doe"
    assert response.data[1]["name"] == "Jane Doe"


@pytest.mark.django_db
def test_retrieve_name(api_client, create_name):
    name_instance = create_name(name="John Doe")

    response = api_client.get(f"/api/names/{name_instance.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "John Doe"


@pytest.mark.django_db
def test_create_name(api_client):
    data = {"name": "John Doe"}

    response = api_client.post("/api/names/", data)

    # Assert response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "John Doe"


@pytest.mark.django_db
def test_update_name(api_client, create_name):
    name_instance = create_name(name="John Doe")

    updated_data = {"name": "Jane Doe"}
    response = api_client.put(f"/api/names/{name_instance.id}/", updated_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Jane Doe"


@pytest.mark.django_db
def test_partial_update_name(api_client, create_name):
    name_instance = create_name(name="John Doe")

    partial_data = {"name": "Johnny"}

    response = api_client.patch(f"/api/names/{name_instance.id}/", partial_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Johnny"


@pytest.mark.django_db
def test_delete_name(api_client, create_name):
    name_instance = create_name(name="John Doe")
    response = api_client.delete(f"/api/names/{name_instance.id}/")


    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Name.objects.filter(id=name_instance.id).exists()
