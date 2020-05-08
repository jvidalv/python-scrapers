from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent


def firefox():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    return webdriver.Firefox(GeckoDriverManager().install(), options=options)


def chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=2')
    chrome_options.add_argument(f'user-agent={random_user_agent()}')
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def random_user_agent():
    ua = UserAgent()
    return ua.random
