import re
from time import sleep
from typing import List

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class ChromeOption(ChromeOptions):
    def __init__(self):
        super().__init__()
        self._arguments = ['--headless', '--disable-gpu']
        self.add_experimental_option('excludeSwitches', ['enable-logging'])


class ChromeDriver(WebDriver):
    def __init__(self):
        super().__init__(options=ChromeOption())
        self.number_regular = re.compile("([0-9]+(.[0-9]{1,3})?)")
        self.date_regular = re.compile("(\d+-\d+-\d+).?")
        self.text_zero = ["投币", "分享", "收藏人数"]
        self.js_500 = "window.scrollTo(0,500);"
        self.js_400 = "window.scrollTo(0,400);"
        self.index_to_key = {"0": "coin", "1": "collect", "2": "comment", "3": "share"}


    def get_node_or_nodes(self, *, driver: WebDriver, find_mode: str, param: str, multi: bool = False):
        exec_statements = f"result = driver.find_element_by_{find_mode}('{param}')"

        if multi:
            exec_statements = f"result = driver.find_elements_by_{find_mode}('{param}')"

        exec(exec_statements)

        return locals()["result"]

    def get_node_value(self, node: WebElement, attribute: str = "", text: bool = False,
                       regular: bool = False, regular_pattern = None) -> str:
        result = ""
        if text:
            text_value = node.text
            result = "0" if text_value in self.text_zero else text_value

        if attribute:
            result = node.get_attribute(attribute)

        if regular:
            if not regular_pattern:
                regular_pattern = self.number_regular
            res = re.search(regular_pattern, result)
            if res is None:
                return ""
            regular_res = res.group()
            if "万" in result or "w" in result:
                regular_res = str(float(regular_res) * 10000)

            result = regular_res
        return result

    def get_node_value_by_while(
            self,
            driver,
            param:str,
            find_mode: str = "class_name",
            attribute:str = "title",
            text:bool = False,
            regular:bool = True,
            regular_pattern = None,
            value: str = ""
    ):
        if not regular_pattern:
            regular_pattern = self.number_regular
        index = 1
        while not value:
            index += 1
            node = self.get_node_or_nodes(driver=driver, find_mode=find_mode, param=param)
            value = self.get_node_value(node, attribute=attribute, text=text, regular=regular, regular_pattern=regular_pattern)
            if text or index >= 10:
                value = self.get_node_value(node, text=True, regular=regular, regular_pattern=regular_pattern)
            if index >= 20:
                value = ""
                break
            sleep(0.5)
        if not value:
            raise Exception(f"driver: {driver}, find_mode: {find_mode}, param: {param}")

        return value

    def get_nodes_value(
            self,
            nodes: List[WebElement],
            attribute: str = "",
            text: bool = False,
            regular: bool = False
    ) -> List[str]:
        return [
            self.get_node_value(node, attribute=attribute, text=text, regular=regular)
            for node in nodes
        ]


class Driver:
    def __init__(self, url: str = None):
        self.url = url
        self.driver = ChromeDriver()
        super().__init__()

    def __enter__(self):
        print(f"WebDriver Engine Starting")
        if self.url:
            self.driver.get(self.url)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("WebDriver Engine Ending")
        self.driver.quit()


class DriverOpen:
    def __init__(self, file_type: str, operation_type: str):
        self.file = open(f'txt/{file_type}.txt', operation_type)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
