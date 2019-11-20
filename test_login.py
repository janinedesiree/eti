import pytest
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

def test_wrong_password():
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    assert "Log in | Django site admin" in driver.title
    username = driver.find_element_by_name("username")
    username.send_keys("limwanning")
    password = driver.find_element_by_name("password")
    password.send_keys("wrong")
    password.send_keys(Keys.RETURN)
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

@pytest.mark.parametrize("a, b", [
("janinedesiree", "T!t@nia_"),
("limwanning", "T!t@nia_"),
("galeellamae", "T!t@nia_"),
])
def test_correct_username_password(a, b):
    driver.get("http://localhost:8000/admin/logout/")
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    assert "Log in | Django site admin" in driver.title
    username = driver.find_element_by_name("username")
    username.send_keys(a)
    password = driver.find_element_by_name("password")
    password.send_keys(b)
    password.send_keys(Keys.RETURN)
    assert driver.current_url == "http://localhost:8000/admin/"

def test_logout():
    driver.get("http://localhost:8000/admin/logout/")
    assert "Logged out | Django site admin" in driver.title
    driver.close()
