import pytest
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

#####TESTS#####
@pytest.mark.parametrize("adminpage", [
("http://localhost:8000/admin/"),
("http://localhost:8000/admin/auth/group/"),
("http://localhost:8000/admin/auth/group/add/"),
("http://localhost:8000/admin/auth/user/"),
("http://localhost:8000/admin/auth/user/add/"),
("http://localhost:8000/admin/blog/category/"),
("http://localhost:8000/admin/blog/category/add/"),
("http://localhost:8000/admin/blog/post/"),
("http://localhost:8000/admin/blog/post/add/"),
])
def test_admin_pages_access(adminpage):
    driver.get(adminpage)
    assert "Log in | Django site admin" in driver.title

@pytest.mark.parametrize("allpages", [
("http://localhost:8000/projects/"),
("http://localhost:8000/blog/"),
("http://localhost:8000/blog/3/"),
("http://localhost:8000/blog/Projects%20done/"),
])
def test_access_all_pages(allpages):
    driver.get(allpages)
    assert driver.current_url == allpages

def test_view_login_page():
    driver.delete_all_cookies()
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    assert "Log in | Django site admin" in driver.title

def test_wrong_password():
    login("wanninglim", "wrong")
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

def test_wrong_username():
    login("wrong", "T!t@nia_")
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

def test_username_doesnt_exist():
    login("FakeUser1", "T!t@nia_")
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

def test_username_case():
    login("janinedesiree", "t!t@nia_")
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

def test_password_case():
    login("janinedesiree", "T!t@nia_")
    assert driver.current_url == "http://localhost:8000/admin/"

@pytest.mark.parametrize("a, b", [
("janinedesiree", "T!t@nia_"),
("limwanning", "T!t@nia_"),
])
def test_correct_username_password(a,b):
    driver.get("http://localhost:8000/admin/logout/")
    login(a,b)
    assert driver.current_url == "http://localhost:8000/admin/"

def test_logout():
    driver.get("http://localhost:8000/admin/logout/")
    assert "Logged out | Django site admin" in driver.title
    driver.close()
