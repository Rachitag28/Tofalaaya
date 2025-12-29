def test_get_products_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_fetch_products(client):
    payload = {
        "name": "Welcome Box",
        "description": "Perfect box to welcome new members.",
        "category": "Welcome Kits",
        "price": 1500,
        "images": [
            "image1.jpg",
            "image2.jpg"
        ],
        "items": [
            "Coffee Mug",
            "T-Shirt",
            "Sticker Pack",
            "Notebook"
        ],
        "stock": 100,
        "rating": 4.5,
        "offers": {
            "offer": "-10%",
            "offer_type": "Discount",
            "offer_valid_till": "2024-12-31T23:59:59",
            "offer_start_date": "2024-01-01T00:00:00"
        }
    }

    create_resp = client.post("/products/", json=payload)
    assert create_resp.status_code == 200

    fetch_resp = client.get("/products/")
    data = fetch_resp.json()

    assert len(data) == 1
    assert data[0]["name"] == "Welcome Box"



def test_modify_products(client):
    payload = {
        "name": "Wedding Gift Box",
        "description": "Perfect box to thank family members.",
        "category": "Wedding",
        "price": 1100,
        "images": [
            "image1.jpg",
            "image2.jpg"
        ],
        "items": [
            "250g Cahsewer Nuts",
            "250g Almonds",
            "Assorted Chocolates",
        ],
        "stock": 100,
        "rating": 4.5,
        "offers": {
            "offer": "-10%",
            "offer_type": "Discount",
            "offer_valid_till": "2024-12-31T23:59:59",
            "offer_start_date": "2024-01-01T00:00:00"
        }
    }

    create_resp = client.post("/products/", json=payload)
    assert create_resp.status_code == 200
    create_product_data = create_resp.json()

    update_resp = client.patch(f"/products/{create_product_data.get('product_id')}", json={
        "price": 1200,
        "stock": 90
    })
    assert update_resp.status_code == 200

    fetch_resp = client.get("/products/", params={"product_id": create_product_data.get("product_id")})
    get_product_data = fetch_resp.json()

    assert len(get_product_data) == 1
    assert get_product_data[0]["price"] == 1200
    assert get_product_data[0]["stock"] == 90