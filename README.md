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
    <br>
    <i><b>Related Projects</b>:
        <a href="https://github.com/ContentAutomation/YouTubeWatcher">YouTube Watcher</a>,
        <a href="https://github.com/ContentAutomation/TwitchCompilationCreator">Twitch Compilation Creator</a>,
        <a href="https://github.com/ContentAutomation/NeuralNetworks">Neural Networks</a>
    </i>
</p>


<hr />

## About

This project aims to automate the upload process for YouTube Videos. Since videos can only be publicly uploaded through the [YouTube Data API](https://developers.google.com/youtube/v3) by using a [Google Workspaces Account](https://workspace.google.com/) (not free!), we decided to create a headless uploader using [Selenium](https://www.selenium.dev/) and [Docker](https://www.docker.com/). This approach also bypasses API restrictions (e.g. Rate Limits/Endcards can't be set through the API).

*Note: Because the upload process is often updated by Google, the code might not work when you try it! Often, there are only minor changes that have to be made. If you find yourself in this situation, please open an [Issue](https://github.com/ContentAutomation/YouTubeUploader/issues) or provide a quick fix in form of a [Pull Request](https://github.com/ContentAutomation/YouTubeUploader/pulls) to make sure that the codebase stays up to date!*

**This project is for educational purposes only. Automating video uploads to YouTube with automation software might be against [YouTube's Terms of Service](https://www.youtube.com/static?template=terms). Even though our tests went smoothly, one might encounter problems when using the YouTube Uploader extensively.**

## Setup

### Dockerized Browser
To run the uploader in a headless mode, it needs to connect to a docker container. To test the uploader locally without using docker, this section can be skipped. Otherwise, the docker container can be started by executing the following steps:
1. Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)

*Note: On Windows and Mac, docker-compose is already installed when installing docker.*

2. Clone/Download this repository
3. Navigate to the root of the repository
4. Run ```docker-compose up``` to start the docker container (append ```-d``` if you want to run it in a detached mode)

*Note: Selenium can now connect to the browser via port 4444. In Python the connection can be established with the following command.*

```python
driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.FIREFOX,
)
```

*See `main.py` for more information.*
    
6. Continue with the [YouTube Uploader Setup](#setup-uploader)

### <a name="setup-uploader"></a> YouTube Uploader


This project requires [Poetry](https://python-poetry.org/) to install the required dependencies.
Check out [this link](https://python-poetry.org/docs/) to install Poetry on your operating system.

Make sure you have installed [Python](https://www.python.org/downloads/) 3.8 or higher! Otherwise Step 3 will let you know that you have no compatible Python version installed.

1. Clone/Download this repository
2. Navigate to the root of the repository
3. Run ```poetry install``` to create a virtual environment with Poetry
4. In a browser of your choice, login into the YouTube account that you want to use the uploader with
5. Use a cookie extraction tool to extract the YouTube cookies into a JSON file (for example [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) [Chrome] or [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/) [Firefox])

*Note: This is required so that the uploader is automatically logged in into the YouTube account using the cookies. Performing a Google login through automated software is extremely hard due to Google's bot detection/Login safety features*

7. Either run the dockerized Browser with `docker-compose up`, install [geckodriver](https://github.com/mozilla/geckodriver/releases) for a local Firefox or [ChromeDriver](https://chromedriver.chromium.org/downloads) for Chromium. Ensure that geckodriver/ChromeDriver are in a location in your `$PATH`.
8. Run ```poetry run python main.py``` to run the program. Alternatively you can run ```poetry shell``` followed by ```python main.py```. By default this connects to the dockerized Firefox Browser (headless). To automate a different Browser (not-headless) use the `--browser [chrome/firefox]` command line option.


## Run Parameters
All of these parameters are optional and a default value will be used if they are not defined. 
You can also get these definitions by running ```main.py --help```
