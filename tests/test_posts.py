import pytest
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

#functions that are used throughout
def login(name, passwrd):
    driver.delete_all_cookies()
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    username = driver.find_element_by_name("username")
    username.send_keys(name)
    password = driver.find_element_by_name("password")
    password.send_keys(passwrd)
    password.send_keys(Keys.RETURN)
    return True

def post_input(title, body, index):
    driver.get("http://localhost:8000/admin/blog/post/add/")
    driver.find_element_by_name("title").send_keys(title)
    driver.find_element_by_name("body").send_keys(body)
    category = Select(driver.find_element(By.XPATH, '//*[@id="id_categories"]'))
    category.select_by_index(index)
    driver.find_element_by_name("_save").click()
    return True

#####TESTS#####
def test_create_valid_post():
    login("janinedesiree", "T!t@nia_")
    post_input("Test Post 1", "J'adore manger.", 1)
    assert "success" in driver.page_source

def test_invalid_title_exists():
    login("janinedesiree", "T!t@nia_")
    post_input("Test Post 1", "J'adore manger.", 1)
    assert "error" in driver.page_source

def test_invalid_blank_title():
    login("janinedesiree", "T!t@nia_")
    post_input("", "J'adore manger.", 1)
    assert "error" in driver.page_source

def test_invalid_blank_body():
    login("janinedesiree", "T!t@nia_")
    post_input("TestBlankBody", "", 1)
    assert "error" in driver.page_source

def test_all_blank():
    login("janinedesiree", "T!t@nia_")
    post_input("", "", 1)
    assert "error" in driver.page_source
