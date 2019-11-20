import pytest
from selenium.webdriver.common.by import By
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

#login to a superuser first
def test_create_new_user():
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    username = driver.find_element_by_name("username")
    username.send_keys("janinedesiree")
    password = driver.find_element_by_name("password")
    password.send_keys("T!t@nia_")
    password.send_keys(Keys.RETURN)
    driver.get("http://localhost:8000/admin/auth/user/add/")
    newuser = driver.find_element(By.XPATH, '//*[@id="id_username"]')
    newuser.send_keys("newUser1")
    newpass1 = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
    newpass1.send_keys("n3wUs3r_")
    newpass2 = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
    newpass2.send_keys("n3wUs3r_")
    driver.find_element_by_name("_save").click()
    assert "The user \"newUser1\" was added successfully. You may edit it again below." in driver.page_source
    drive.close()
