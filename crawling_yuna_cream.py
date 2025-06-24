import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 설정
options = Options()
driver = webdriver.Chrome(options=options)

# 상세정보 셀렉터 정의
info_selectors = {
    "내용물의 용량 또는 중량": "#artcInfo > dl:nth-child(2) > dd",
    "제품 주요 사양": "#artcInfo > dl:nth-child(3) > dd",
    "사용기한": "#artcInfo > dl:nth-child(4) > dd",
    "사용방법": "#artcInfo > dl:nth-child(5) > dd",
    "제조업자 등": "#artcInfo > dl:nth-child(6) > dd",
    "제조국": "#artcInfo > dl:nth-child(7) > dd",
    "성분": "#artcInfo > dl:nth-child(8) > dd",
    "기능성 여부": "#artcInfo > dl:nth-child(9) > dd",
    "주의사항": "#artcInfo > dl:nth-child(10) > dd",
    "품질보증기준": "#artcInfo > dl:nth-child(11) > dd",
    "소비자상담": "#artcInfo > dl:nth-child(12) > dd"
}

# 리뷰 전체 페이지 순회 함수
def collect_reviews_all_pages():
    reviews = []
    while True:
        review_elements = driver.find_elements(By.CSS_SELECTOR, "#gdasList > li")
        for r in review_elements:
            try:
                review_id = r.find_element(By.CSS_SELECTOR, "div.info > div > p.info_user > a.id").text.strip()
                rating = r.find_element(By.CSS_SELECTOR, "div.score_area > span.review_point > span").text.strip()
                skin_type = r.find_element(By.CSS_SELECTOR, "div.poll_sample > dl:nth-child(1) > dd > span").text
                concern = r.find_element(By.CSS_SELECTOR, "div.poll_sample > dl:nth-child(2) > dd > span").text
                sensitivity = r.find_element(By.CSS_SELECTOR, "div.poll_sample > dl:nth-child(3) > dd > span").text
                review_text = r.find_element(By.CSS_SELECTOR, "div.txt_inner").text.strip()

                reviews.append({
                    "리뷰 ID": review_id,
                    "별점": rating,
                    "피부타입": skin_type,
                    "피부고민": concern,
                    "자극도": sensitivity,
                    "리뷰": review_text
                })
            except:
                continue

        try:
            current = driver.find_element(By.CSS_SELECTOR, "#gdasContentsArea > div > div.pageing > strong").text
            pages = driver.find_elements(By.CSS_SELECTOR, "#gdasContentsArea > div > div.pageing > a")
            next_pages = [p for p in pages if p.text.isdigit() and int(p.text) > int(current)]
            if next_pages:
                next_pages[0].click()
                time.sleep(1.5)
                continue
        except:
            pass

        try:
            next_block = driver.find_element(By.CSS_SELECTOR, "#gdasContentsArea > div > div.pageing > a.next")
            if next_block.is_displayed():
                next_block.click()
                time.sleep(1.5)
                continue
        except:
            break
        break
    return reviews

product_data = []

# 전체 상품 페이지 순회 (1~16페이지)
for page in range(22, 32):
    print(f"📄 페이지 {page} 처리 중...")
    page_url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100010015&fltDispCatNo=&prdSort=02&pageIdx={page}&rowsPerPage=24&searchTypeSort=btn_thumb"
    driver.get(page_url)
    time.sleep(2)

    product_elements = driver.find_elements(By.CSS_SELECTOR, "#Contents > ul > li")

    for product in product_elements:
        try:
            img_tag = product.find_element(By.CSS_SELECTOR, "div > a > img")
            img_url = img_tag.get_attribute("src")
            product_name = img_tag.get_attribute("alt")
            detail_url = product.find_element(By.CSS_SELECTOR, "div > a").get_attribute("href")

            driver.execute_script("window.open(arguments[0]);", detail_url)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            try:
                driver.find_element(By.CSS_SELECTOR, "#buyInfo > a").click()
                time.sleep(1)
            except:
                print(f"[{product_name}] 구매정보 탭 없음")

            detail_info = {}
            for key, selector in info_selectors.items():
                try:
                    detail_info[key] = driver.find_element(By.CSS_SELECTOR, selector).text.strip()
                except:
                    detail_info[key] = ""

            try:
                driver.find_element(By.CSS_SELECTOR, "#reviewInfo > a").click()
                time.sleep(1.5)
            except:
                print(f"[{product_name}] 리뷰 탭 없음")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            reviews = collect_reviews_all_pages()
            for review in reviews:
                data = {
                    "제품명": product_name,
                    "이미지 URL": img_url
                }
                data.update(detail_info)
                data.update(review)
                product_data.append(data)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"제품 처리 실패: {e}")
            continue

df = pd.DataFrame(product_data)
df.to_csv("oliveyoung_cream_22_31.csv", index=False, encoding="utf-8-sig")
print("✅ 전체 페이지의 모든 제품 크롤링 완료")
driver.quit()
