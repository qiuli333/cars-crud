def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)
    
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"


def test_invalid_year_is_not_saved(client):
    # 提交非法年份的请求
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 1800,
        "color": "Black",
    }
    response = client.post("/api/cars", json=payload)

    # 断言：返回 422 校验失败
    assert response.status_code == 422

    # 断言：查询列表为空，数据没有被保存
    list_response = client.get("/api/cars")
    assert list_response.json() == []
