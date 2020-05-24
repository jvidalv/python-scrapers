from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


def firefox():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=2')
    options.add_argument(f'user-agent={random_user_agent()}')
    return webdriver.Firefox(GeckoDriverManager().install(), options=options)


def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument('--disable-gpu')
    return webdriver.Chrome(chrome_options=chrome_options, )


def random_user_agent():
    ua = UserAgent()
    return ua.random
