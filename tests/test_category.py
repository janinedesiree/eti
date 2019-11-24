import pytest
import os
import unittest
from selenium.webdriver.common.by import By
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

def category_input(title):
    cat = driver.find_element_by_name("name")
    cat.clear()
    cat.send_keys(title)
    driver.find_element_by_name("_save").click()
    return True

def invalid_input_blank():
    category_input("")

def invalid_input_long():
    category_input("4567890123456789012345345678901234567890123453456789012345678901234534567890123456789012345345678901234567890123453456789012345678901234534567890123456789012345345678901234567890123453")

def invalid_input_existing():
    category_input("CCAs")

def update(existingName):
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element_by_link_text(existingName).click()
    return True

#####TESTS#####

#####CREATING A NEW CATEGORY
##3.0.0 - Test that user is able create a new category with valid parameters
def test_create_new_valid_params():
    login("janinedesiree","T!t@nia_")
    driver.get("http://localhost:8000/admin/blog/category/add/")
    category_input("TestCat1")
    assert "Select category to change | Django site admin" in driver.title

##3.0.1 - Test that user is unable create a new category with blank input
def test_create_invalid_blank():
    driver.get("http://localhost:8000/admin/blog/category/add/")
    invalid_input_blank()
    assert "error" in driver.page_source

##3.0.2 - Test that user is unable create a new category with long input
def test_create_invalid_long():
    driver.get("http://localhost:8000/admin/blog/category/add/")
    invalid_input_blank()
    assert "error" in driver.page_source

##3.0.3 - Test that user is unable create a new category with existing name input
def test_create_invalid_existing():
    driver.get("http://localhost:8000/admin/blog/category/add/")
    invalid_input_blank()
    assert "error" in driver.page_source


#####UPDATE A CATEGORY
##3.1.0 - Test that user is able update existing categories with valid parameters
def test_valid_update():
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element_by_link_text('TestCat1').click()
    category_input("UpdatedNew1")
    assert "Select category to change | Django site admin" in driver.title

##3.1.1 - Test that user is unable to update category with blank input
def test_blank_input():
    update("1")
    invalid_input_blank()
    assert "error" in driver.page_source

##3.1.2 - Test that user is unable to update category with existing category name input
def test_existing_input():
    update("2")
    invalid_input_existing()
    assert "error" in driver.page_source

##3.1.3 - Test that user is unable to update category with long input
def test_long_input():
    update("3")
    invalid_input_long()
    assert "error" in driver.page_source


#####DELETING A CATEGORY
##3.2.0 - Test that user is unable to delete existing categories in use
def test_delete_used_category():
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element_by_link_text('CCAs').click()
    driver.find_element_by_link_text('Delete').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
    assert "error" in driver.page_source

##3.2.1 - Test that user is able to delete existing categories not in use
def test_delete_unused_category():
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element_by_link_text('4').click()
    driver.find_element_by_link_text('Delete').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
    assert "success" in driver.page_source
    driver.close()
