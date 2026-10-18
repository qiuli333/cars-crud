import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    
    # 填写表单
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    
    # 点击创建
    page.get_by_role("button", name="Create car").click()

    # 断言：跳转详情页，标题正确
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()
def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建一辆 Honda Civic
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("White")
    page.get_by_role("button", name="Create car").click()

    # 等待详情页加载完成
    page.wait_for_url(re.compile(r"/cars/\d+$"))

    # 2. 点击编辑链接
    page.get_by_role("link", name="Edit car").click()
    # 等待编辑页表单加载
    page.wait_for_selector('input[name="model"]')

    # 3. 修改型号和年份（先全选原有内容再输入，确保完全替换）
    model_input = page.get_by_label("Model", exact=True)
    model_input.click()
    model_input.press("Control+A")  # 全选原有文本
    model_input.fill("Accord")

    year_input = page.get_by_label("Year", exact=True)
    year_input.click()
    year_input.press("Control+A")
    year_input.fill("2023")

    page.get_by_role("button", name="Save changes").click()

    # 4. 等待保存后跳转回详情页，先等标题元素出现再断言可见
    page.wait_for_url(re.compile(r"/cars/\d+$"))
    heading = page.get_by_role("heading", name="Honda Accord")
    heading.wait_for(timeout=10000)
    expect(heading).to_be_visible()

    # 5. 刷新页面，再次断言修改依然存在
    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
