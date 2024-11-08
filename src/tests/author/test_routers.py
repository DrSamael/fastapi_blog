from fastapi import status

from src.tests.fixtures import *


async def test_list_authors(async_client, test_authors_list, test_current_user_admin):
    response = await async_client.get("/authors/")
    result_authors_ids = [author['_id'] for author in response.json()]
    test_authors_ids = [str(author['_id']) for author in test_authors_list]

    assert response.status_code == status.HTTP_200_OK
    assert result_authors_ids == test_authors_ids


async def test_current_user_author_successful(async_client, test_users_author, test_author,
                                              test_current_user_author):
    response = await async_client.get("/authors/user-author")
    result_authors_ids = [author['_id'] for author in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert str(test_users_author['_id']) in result_authors_ids
    assert str(test_author['_id']) not in result_authors_ids


async def test_current_user_author_unauthorized(async_client):
    response = await async_client.get("/authors/user-author")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_show_author_successful(async_client, test_author, test_current_user_admin):
    author_id = str(test_author['_id'])
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == str(test_author['_id'])


async def test_show_author_invalid_data(async_client, test_current_user_admin):
    author_id = str(ObjectId())
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_show_author_admin_required(async_client, test_current_user_author):
    author_id = str(ObjectId())
    response = await async_client.get(f"/authors/{author_id}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_author_successful(async_client, test_user, test_current_user_admin):
    AuthorData["user_id"] = str(test_user['_id'])
    response = await async_client.post(f"/authors/", json=AuthorData)
    result_author = response.json()

    assert response.status_code == status.HTTP_200_OK
    for key in AuthorData:
        assert result_author[key] == AuthorData[key]


async def test_create_author_unauthorized(async_client):
    response = await async_client.post(f"/authors/", json=AuthorData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_author_admin_required(async_client, test_current_user_author):
    response = await async_client.post(f"/authors/", json=AuthorData)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_author_missing_data(async_client, test_current_user_admin):
    response = await async_client.post(f"/authors/", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_author_invalid_data(async_client, test_current_user_admin):
    invalid_data = {"company": "123",
                    "biography": faker.text(max_nb_chars=50),
                    "genre": ["social"]}
    response = await async_client.post(f"/authors/", json=invalid_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_author_invalid_user(async_client, test_current_user_admin):
    AuthorData["user_id"] = str(ObjectId())
    response = await async_client.post(f"/authors/", json=AuthorData)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User does not exist"


async def test_create_author_user_already_has_author(async_client, test_user, test_current_user_admin):
    AuthorData["user_id"] = str(test_user['_id'])

    response = await async_client.post(f"/authors/", json=AuthorData)
    assert response.status_code == status.HTTP_200_OK

    response2 = await async_client.post(f"/authors/", json=AuthorData)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert response2.json()["detail"] == "This user is already has an author"


async def test_edit_author_successful(async_client, test_author, test_current_user_admin):
    response = await async_client.patch(f"/authors/{test_author['_id']}", json=UpdatedAuthorData)
    result_author = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result_author['company'] == UpdatedAuthorData['company']


async def test_edit_author_unauthorized(async_client, test_author):
    response = await async_client.patch(f"/authors/{test_author['_id']}", json=UpdatedAuthorData)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_edit_author_invalid_author_id(async_client, test_current_user_admin):
    response = await async_client.patch(f"/authors/{str(ObjectId())}", json=UpdatedAuthorData)

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_edit_author_blank_data(async_client, test_author, test_current_user_admin):
    response = await async_client.patch(f"/authors/{test_author['_id']}", json={})

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_edit_author_invalid_data(async_client, test_author, test_current_user_admin):
    invalid_author_data = {"company": "Updated company title", "biography": "too long text" * 500}
    response = await async_client.patch(f"/authors/{test_author['_id']}", json=invalid_author_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_edit_author_admin_required(async_client, test_author, test_current_user_simple):
    response = await async_client.patch(f"/authors/{test_author['_id']}", json=UpdatedAuthorData)

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_destroy_author_successful(async_client, test_author, test_current_user_admin):
    response = await async_client.delete(f"/authors/{test_author['_id']}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Author deleted successfully'


async def test_destroy_author_unauthorized(async_client, test_author):
    response = await async_client.delete(f"/authors/{test_author['_id']}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_author_invalid_author_id(async_client, test_current_user_admin):
    response = await async_client.delete(f"/authors/{str(ObjectId())}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_author_admin_required(async_client, test_author, test_current_user_simple):
    response = await async_client.delete(f"/authors/{test_author['_id']}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
