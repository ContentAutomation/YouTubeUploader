import argparse
import logging
from argparse import ArgumentError
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector

from src.login import confirm_logged_in, login_using_cookie_file
from src.upload import upload_file


def main():
    logging.getLogger().setLevel(logging.INFO)

    # Setup Selenium web driver
    parser = get_arg_parser()
    args = parser.parse_args()

    if args.browser == "docker":
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.FIREFOX,
        )
    elif args.browser == "firefox":
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", "en-us")
        firefox_profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile)
    elif args.browser == "chrome":
        driver = webdriver.Chrome()
    else:
        raise ArgumentError(message="Unknown driver.")

    driver.set_window_size(1920, 1080)
    login_using_cookie_file(driver, cookie_file=args.login_cookies)
    driver.get("https://www.youtube.com")

    assert "YouTube" in driver.title

    try:
        confirm_logged_in(driver)
        driver.get("https://studio.youtube.com")
        assert "Channel dashboard" in driver.title
        driver.file_detector = LocalFileDetector()
        upload_file(
            driver,
            video_path=args.video_path,
            title=args.title,
            thumbnail_path=args.thumbnail,
            description=args.description,
            game=args.game,
            upload_time=args.upload_time,
        )
    except:
        driver.close()
        raise


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    today = datetime.now()
    parser.add_argument(
        "-B",
        "--browser",
        choices=["docker", "chrome", "firefox"],
        default="docker",
        type=str,
        help="Select the driver/browser to use for executing the script (default: docker).",
    )
    parser.add_argument(
        "-l",
        "--login-cookies-path",
        dest="login_cookies",
        type=str,
        help="A json file that contains the cookies required to sign into YouTube in the target browser.",
        required=True,
    )
    parser.add_argument(
        "video_path",
        help="Path to the video file. When using docker, this path has to be inside the container "
             "(default mount is /uploads/).",
    )
    parser.add_argument(
        "--thumbnail-path",
        "-T",
        help="Path to the thumbnail file (default: None).",
        dest="thumbnail",
        type=str,
        default=None,
        required=False,
    )
    parser.add_argument(
        "-t",
        "--title",
        help="This argument declares the title of the uploaded video.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--description",
        help="This argument declares the description of the uploaded video.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-g",
        "--game",
        help="This argument declares the game of the uploaded video (default: None).",
        default=None,
        required=False,
    )
    parser.add_argument(
        "-ut",
        "--upload_time",
        help="This argument declares the upload time of the uploaded video. Has to be a m",
        required=False,
        type=datetime,
        default=datetime(today.year, today.month, today.day, 20, 15),
    )
    return parser


if __name__ == "__main__":
    main()
