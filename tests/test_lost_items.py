import pytest
import pytest_asyncio
from models import LostItem, Category


@pytest_asyncio.fixture
async def add_item(test_db):
    item = {"name": "TestLostItem1", "location": "test location"}
    db_item = LostItem(**item)
    test_db.add(db_item)
    await test_db.commit()
    await test_db.refresh(db_item)
    return db_item


@pytest_asyncio.fixture
async def add_category(test_db):
    category = Category(name="Документы", description="Паспорта, права, справки")
    test_db.add(category)
    await test_db.commit()
    await test_db.refresh(category)
    return category


@pytest.mark.asyncio
async def test_get_lost_items_empty_db(client):
    response = await client.get("/lost_items/")
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_lost_items(client, add_item):
    db_item = add_item
    response = await client.get("/lost_items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == db_item.name
    assert data[0]["location"] == db_item.location


@pytest.mark.asyncio
async def test_create_lost_items(client):
    item_data = {"name": "Часы", "location": "на остановке"}
    response = await client.post("/lost_items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["location"] == item_data["location"]
    assert "id" in data


@pytest.mark.skip(reason="Эндпоинт не реализован (routers/lost_items.read_lost_item)")
@pytest.mark.asyncio
async def test_get_lost_item_by_id(client, add_item):
    db_item = add_item
    response = await client.get(f"/lost_items/{db_item.id}")
    assert response.status_code == 200
    assert response.json()["name"] == db_item.name


@pytest.mark.asyncio
async def test_update_lost_items(client, test_db, add_item):
    new_data = {"name": "TestLostItem2"}
    db_item = add_item
    assert add_item.id == 1
    assert db_item.name != new_data["name"]
    response = await client.put("/lost_items/1", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_data["name"]
    db_item = await test_db.get(LostItem, 1)
    assert db_item.name == new_data["name"]


@pytest.mark.skip(reason="Эндпоинт не реализован (routers/lost_items.delete_lost_item)")
@pytest.mark.asyncio
async def test_delete_lost_item(client, test_db, add_item):
    db_item = await test_db.get(LostItem, 1)
    assert db_item is not None
    await client.delete("/lost_items/1")
    db_item = await test_db.get(LostItem, 1)
    assert db_item is None


# negative tests
@pytest.mark.asyncio
async def test_create_lost_items_incorrect_data(client):
    """
    Проверяем, что если при создании нового объекта передать недостаточно данных,
    post("/lost_items/") завершится с кодом ошибки 422
    """
    response = await client.post("/lost_items/", json={})
    assert response.status_code == 422


@pytest.mark.skip(reason="Эндпоинт не реализован (routers/lost_items.read_lost_item)")
@pytest.mark.asyncio
async def test_get_lost_item_by_id_404(client):
    response = await client.get(f"/lost_items/{1}")
    assert response.status_code == 404


@pytest.mark.skip(reason="Эндпоинт не реализован (routers/lost_items.delete_lost_item)")
@pytest.mark.asyncio
async def test_delete_lost_item_404(client):
    response = await client.delete("/lost_items/1")
    assert response.status_code == 404


# category linking tests
@pytest.mark.asyncio
async def test_update_lost_item_category_success(client, test_db, add_item, add_category):
    item = add_item
    category = add_category
    response = await client.put(f"/lost_items/{item.id}/category", json={"category_id": category.id})
    assert response.status_code == 200
    data = response.json()
    assert data["category_id"] == category.id

    updated = await test_db.get(LostItem, item.id)
    assert updated.category_id == category.id


@pytest.mark.asyncio
async def test_update_lost_item_category_lost_item_404(client, add_category):
    category = add_category
    response = await client.put("/lost_items/999/category", json={"category_id": category.id})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_lost_item_category_category_404(client, add_item):
    item = add_item
    response = await client.put(f"/lost_items/{item.id}/category", json={"category_id": 999})
    assert response.status_code == 404
