import pytest
import pytest_asyncio
from models import Category


@pytest_asyncio.fixture
async def add_category(test_db):
    category = Category(name="Документы", description="Паспорта, права, справки")
    test_db.add(category)
    await test_db.commit()
    await test_db.refresh(category)
    return category


@pytest.mark.asyncio
async def test_create_category(client):
    payload = {"name": "Электроника", "description": "Гаджеты и устройства"}
    response = await client.post("/categories/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert "id" in data


@pytest.mark.asyncio
async def test_read_category(client, add_category):
    db_category = add_category
    response = await client.get(f"/categories/{db_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == db_category.id
    assert data["name"] == db_category.name


@pytest.mark.asyncio
async def test_read_category_404(client):
    response = await client.get("/categories/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_category(client, test_db, add_category):
    db_category = add_category
    payload = {"name": "Документы и карты", "description": "Все виды документов"}
    response = await client.put(f"/categories/{db_category.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

    updated = await test_db.get(Category, db_category.id)
    assert updated.name == payload["name"]
    assert updated.description == payload["description"]


@pytest.mark.asyncio
async def test_update_category_404(client):
    payload = {"name": "Не существует", "description": "-"}
    response = await client.put("/categories/888", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category(client, test_db, add_category):
    db_category = await test_db.get(Category, add_category.id)
    assert db_category is not None

    response = await client.delete(f"/categories/{add_category.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Category deleted"}

    deleted = await test_db.get(Category, add_category.id)
    assert deleted is None


@pytest.mark.asyncio
async def test_delete_category_404(client):
    response = await client.delete("/categories/777")
    assert response.status_code == 404