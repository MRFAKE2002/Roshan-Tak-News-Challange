# Libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def get_article_links(archive_url="https://www.zoomit.ir/archive"):
    with create_driver() as driver:
        driver.get(archive_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.scroll-m-16 a"))
        )

        articles_links = driver.find_elements(By.CSS_SELECTOR, "div.scroll-m-16 a")

        links = []

        for article_link in articles_links:
            href = article_link.get_attribute("href")

            if href is not None and href.startswith("https://www.zoomit.ir"):
                links.append(href)

        return links


def extract_article_data(link):
    with create_driver() as driver:
        driver.get(link)
        wait = WebDriverWait(driver, 10)

        try:
            title = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="__next"]/div[2]/div[1]/main/article/header/div/div/h1',
                    )
                )
            ).text.strip()

            tag_list = driver.find_elements(
                By.XPATH,
                '//*[@id="__next"]/div[2]/div[1]/main/article/header/div/div/div[2]/div[1]/a/span',
            )

            tags = []
            for tag in tag_list:
                text = tag.text.strip()
                if text:
                    tags.append(text)

            paragraph_list = driver.find_elements(
                By.XPATH,
                '//*[@id="__next"]/div[2]/div[1]/main/article/div/div[5]/div/div/div/p',
            )
            paragraphs = [p.text.strip() for p in paragraph_list if p.text]

            return {"title": title, "tags": tags, "paragraphs": paragraphs, "url": link}

        except Exception as e:
            print(f"[!] Error extracting article info: {link}\n{e}")

            return None
