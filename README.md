<p align="center">
    <a href="https://github.com/ContentAutomation"><img src="https://contentautomation.s3.eu-central-1.amazonaws.com/logo.png" alt="Logo" width="150"/></a>
    <br />
    <br />
    <a href="http://choosealicense.com/licenses/mit/"><img src="https://img.shields.io/badge/license-MIT-3C93B4.svg?style=flat" alt="MIT License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <a href="https://www.youtube.com/channel/UCqq27nknJ3fe5IvrAbfuEwQ"><img src="https://img.shields.io/badge/YouTube-FF0000.svg?style=flat&logo=youtube" alt="Platform: YouTube"></a>
        <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED.svg?logo=Docker&logoColor=white" alt="Uses Docker"></a>
        <a href="https://www.selenium.dev/documentation/en/"><img src="https://img.shields.io/badge/Selenium-43B02A.svg?logo=Selenium&logoColor=white&labelColor=43B02A" alt="Automation supporting Firefox and Chrome"></a>
    <br />
         <a href="https://www.mozilla.org/en-US/firefox/new/"><img src="https://img.shields.io/badge/Firefox-FF7139.svg?logo=Firefox-Browser&logoColor=white" alt="Firefox supported"></a>
         <a href="https://www.google.com/chrome/"><img src="https://img.shields.io/badge/Chrome-4285F4.svg?logo=Google-Chrome&logoColor=white" alt="Chrome supported"></a>
    <br />
    <br />
    <i>An automated, headless YouTube Uploader</i>
    <br />
<br />
    <i><b>Authors</b>:
        <a href="https://github.com/ChristianCoenen">Christian C.</a>,
        <a href="https://github.com/MorMund">Moritz M.</a>,
        <a href="https://github.com/lucaSchilling">Luca S. </a>
    </i>
</p>


<hr />

Searches YouTube, queries recommended videos and watches them. All fully automated and anonymised through the [Tor network](https://www.torproject.org/). The project consists of two independently usable components, the YouTube automation written in Python and the dockerized Tor Browser.

**This project is for educational purposes only. Using Tor to watch YouTube videos is strongly discouraged, especially for Botting purposes. Please [inform yourself about the Tor network](https://2019.www.torproject.org/docs/faq.html.en), before using it extensively.**

## Setup

### YouTube automation

This project requires [Poetry](https://python-poetry.org/) to install the required dependencies.
Check out [this link](https://python-poetry.org/docs/) to install Poetry on your operating system.

Make sure you have installed [Python](https://www.python.org/downloads/) 3.8 or higher! Otherwise Step 3 will let you know that you have no compatible Python version installed.

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run ```poetry install``` to create a virtual environment with Poetry
4. Either run the dockerized Browser with `docker-compose up`, install [geckodriver](https://github.com/mozilla/geckodriver/releases) for a local Firefox or [ChromeDriver](https://chromedriver.chromium.org/downloads) for Chromium. Ensure that geckodriver/ChromeDriver are in a location in your `$PATH`.
5. Run ```poetry run python main.py``` to run the program. Alternatively you can run ```poetry shell``` followed by ```python main.py```. By default this connects to the dockerized Browser. To automate a different Browser use the `--browser [chrome/firefox]` command line option.

### Dockerized Tor Browser

Running the Container requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run `docker-compose up`. The image will be built automatically before startup.
4. Selenium can now connect to the browser via port 4444. In Python the connection can be established with the following command.

    ``` python
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        desired_capabilities=options,
    )
    ```

    See `main.py` for more information.

## Run Parameters
All of these parameters are optional and a default value will be used if they are not defined. 
You can also get these definitions by running ```main.py --help```