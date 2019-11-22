import pytest
import os
import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

def test_create_comment_valid_params():
    driver.get("http://localhost:8000/blog/4/")
    author = driver.find_element_by_name("author")
    author.send_keys('Janine Desiree')
    body = driver.find_element_by_name("body")
    body.send_keys("HELP LA")
    driver.find_element_by_css_selector('button.btn.btn-primary').click()
    assert "Je veux dormir :(" in driver.page_source

@pytest.mark.parametrize("a, b", [
("", "mango"),
("mango", ""),
("", ""),
])
def test_create_comment_invalid_params(a,b):
    author = driver.find_element_by_name("author")
    author.send_keys(a)
    body = driver.find_element_by_name("body")
    body.send_keys(a)
    driver.find_element_by_css_selector('button.btn.btn-primary').click()
    author.clear_field()
    body.clear_field()
    assert "Please fill in this field" in driver.page_source
