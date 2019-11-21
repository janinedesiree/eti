import pytest
import os
import unittest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

#login to a superuser first
def test_create_new_valid_params():
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    username = driver.find_element_by_name("username")
    username.send_keys("janinedesiree")
    password = driver.find_element_by_name("password")
    password.send_keys("T!t@nia_")
    password.send_keys(Keys.RETURN)
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]/a').click()
    catName = driver.find_element_by_name("name")
    catName.send_keys("TestCat1")
    driver.find_element_by_name("_save").click()
    assert "Select category to change | Django site admin" in driver.title

@pytest.mark.parametrize("a", [
(""),
("4567890123456789012345345678901234567890123453456789012345678901234534567890123456789012345345678901234567890123453456789012345678901234534567890123456789012345345678901234567890123453"),
("CCAs"),
])
def test_create_new_invalid_params(a):
    driver.get("http://localhost:8000/admin/blog/category/add/")
    driver.find_element_by_name("name").send_keys(a)
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source
    # !!!!FAILED CASE!!!!
    # This test failed because of the 2nd and 3rd parameters. For the 2nd,
    # I entered a very long string but the input field only allows users to
    # enter up to a certain number of characters. For the 3rd, a category
    # that has the same name as en existing category was created as there's
    # no validation preventing categories of the same name to be created.

def test_delete_unused_category():
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[1]/td/input').click()
    driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/label/select').click() #click on dropdown
    driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/label/select/option[2]').click() #click on dropdown option
    driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[4]').click()
    assert "success" in driver.page_source

def test_delete_used_category():
    driver.get("http://localhost:8000/admin/blog/category/")
    driver.find_element_by_link_text('45678901234567890123').click()
    driver.find_element_by_link_text('Delete').click()
    # driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[10]/td/input').click()
    # driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/label/select').click() #click on dropdown
    # driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/label/select/option[2]').click() #click on dropdown option
    # driver.find_element(By.XPATH, '//*[@id="changelist-form"]/div[1]/button').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
    assert "error" in driver.page_source
    driver.close()
    # !!!!FAILED CASE!!!!
    # This failed because there's no validation to check whether it's currently
    # in use as categories can be deleted even if they are currently being used by
    # a post.
