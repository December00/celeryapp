from celery import shared_task
from celery.app import task
from django.utils.timezone import now
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from myblog.celery import app
from .models import Blog


@shared_task()
def parse_tweet():
    driver = webdriver.Chrome()

    try:
        driver.get('https://x.com/elonmusk')

        time.sleep(5)

        tweets = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

        if tweets:
            latest_tweet = tweets[0].text
            tweet_lines = latest_tweet.split("\n")
            tweet_text = tweet_lines[5]

            if not Blog.objects.filter(content=tweet_text).exists():
                Blog.objects.create(
                    title="Закрепленный твит Илона Маска:",
                    content=tweet_text,
                    date=now()
                )
        else:
            print("Не удалось найти твиты.")
    finally:
        driver.quit()