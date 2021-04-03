import logging
import re
from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def upload_file(
        driver: WebDriver,
        video_path: str,
        title: str,
        description: str,
        game: str,
        kids: bool,
        upload_time: datetime,
        thumbnail_path: str = None,
):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytcp-button#create-icon"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//paper-item[@test-id="upload-beta"]'))
    ).click()
    video_input = driver.find_element_by_xpath('//input[@type="file"]')
    video_input.send_keys(video_path)

    _set_basic_settings(driver, title, description, thumbnail_path)
    _set_advanced_settings(driver, game, kids)
    # Go to visibility settings
    for i in range(3):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "next-button"))).click()

    _set_time(driver, upload_time)
    _wait_for_processing(driver)
    # Go back to endcard settings
    driver.find_element_by_css_selector("#step-badge-1").click()
    _set_endcard(driver)

    for _ in range(2):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "next-button"))).click()
        # Sometimes, the done button is clickable but clicking it raises an error, so we add a "safety-sleep" here
        sleep(5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "done-button"))).click()

    # Wait for the dialog to disappear
    sleep(5)
    logging.info("Upload is complete")


def _wait_for_processing(driver):
    # Wait for processing to complete
    progress_label: WebElement = driver.find_element_by_css_selector("span.progress-label")
    pattern = re.compile(r"(finished processing)|(processing hd.*)|(check.*)")
    current_progress = progress_label.get_attribute("textContent")
    last_progress = None
    while not pattern.match(current_progress.lower()):
        if last_progress != current_progress:
            logging.info(f'Current progress: {current_progress}')
        last_progress = current_progress
        sleep(5)
        current_progress = progress_label.get_attribute("textContent")


def _set_basic_settings(driver: WebDriver, title: str, description: str, thumbnail_path: str = None):
    title_input: WebElement = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//ytcp-mention-textbox[@label="Title"]//div[@id="textbox"]',

            )
        )
    )

    # Input meta data (title, description, etc ... )
    description_input: WebElement = driver.find_element_by_xpath(
        '//ytcp-mention-textbox[@label="Description"]//div[@id="textbox"]'
    )
    thumbnail_input: WebElement = driver.find_element_by_css_selector(
        "input#file-loader"
    )

    title_input.clear()
    title_input.send_keys(title)
    description_input.send_keys(description)
    if thumbnail_path:
        thumbnail_input.send_keys(thumbnail_path)


def _set_advanced_settings(driver: WebDriver, game_title: str, made_for_kids: bool):
    # Open advanced options
    driver.find_element_by_css_selector("#toggle-button").click()
    if game_title:
        game_title_input: WebElement = driver.find_element_by_css_selector(
            ".ytcp-form-gaming > "
            "ytcp-dropdown-trigger:nth-child(1) > "
            ":nth-child(2) > div:nth-child(3) > input:nth-child(3)"
        )
        game_title_input.send_keys(game_title)

        # Select first item in game drop down
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#text-item-2",  # The first item is an empty item
                )
            )
        ).click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.NAME, "MADE_FOR_KIDS" if made_for_kids else "NOT_MADE_FOR_KIDS")
    )).click()


def _set_endcard(driver: WebDriver):
    # Add endscreen
    driver.find_element_by_css_selector("#endscreens-button").click()
    sleep(5)

    # Select endcard type from last video or first suggestion if no prev. video
    driver.find_element_by_css_selector("div.card:nth-child(1)").click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "save-button"))).click()


def _set_time(driver: WebDriver, upload_time: datetime):
    # Start time scheduling
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "SCHEDULE"))).click()

    # Open date_picker
    driver.find_element_by_css_selector("#datepicker-trigger > ytcp-dropdown-trigger:nth-child(1)").click()

    date_input: WebElement = driver.find_element_by_css_selector("input.tp-yt-paper-input")
    date_input.clear()
    # Transform date into required format: Mar 19, 2021
    date_input.send_keys(upload_time.strftime("%b %d, %Y"))
    date_input.send_keys(Keys.RETURN)

    # Open time_picker
    driver.find_element_by_css_selector(
        "#time-of-day-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
    ).click()

    time_list = driver.find_elements_by_css_selector("paper-item.paper-item")
    # Transform time into required format: 8:15 PM
    time_str = upload_time.strftime("%I:%M %p").strip("0")
    time = [time for time in time_list[2:] if time.text == time_str][0]
    time.click()
