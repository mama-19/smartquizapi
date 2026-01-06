# from fastapi.testclient import TestClient
# from app.main import app  # Import your FastAPI application
# import pytest
# import httpx
# from app.base.untility import settings


# client = TestClient(app)

# def test_read_root():
    
#     get_all_resp = client.get(
#          "/notifications/notifications/list",
#         params={"name": "tes"},
#         )
#     assert get_all_resp.status_code == 200 , f"list failed : {get_all_resp.text}"
#     print(f"All notification :  {get_all_resp.json}")
#     # response = client.get("/notificat")
#     # assert response.status_code == 200
#     # assert response.json() == {"message": "Hello World"}

# def test_read_item():
#     response = client.get("/items/1")
#     assert response.status_code == 200
#     assert response.json() == {"item_id": 1, "name": "Item 1"}

# def test_read_nonexistent_item():
#     response = client.get("/items/abc")  # Expecting a validation error
#     assert response.status_code == 422  # Unprocessable Entity
