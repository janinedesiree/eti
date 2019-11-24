import pytest
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

def add_edit_user_info(name, passwrd, confirmpasswrd):
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(name)

    password = driver.find_element_by_name("password1")
    password.clear()
    password.send_keys(passwrd)

    password1 = driver.find_element_by_name("password2")
    password1.clear()
    password1.send_keys(confirmpasswrd)

    return True

def update(user, fname, lname, email):

    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(user)

    first = driver.find_element_by_name("first_name")
    first.clear()
    first.send_keys(fname)

    last = driver.find_element_by_name("last_name")
    last.clear()
    last.send_keys(lname)

    mail = driver.find_element_by_name("email")
    mail.clear()
    mail.send_keys(email)

    driver.find_element_by_name("_save").click()

    return True

def updatePassword(passwrd1, passwrd2):
    pass1 = driver.find_element_by_name("password1")
    # pass1.clear()
    pass1.send_keys(passwrd1)
    pass2 = driver.find_element_by_name("password2")
    # pass2.clear()
    pass2.send_keys(passwrd2)
    pass2.send_keys(Keys.RETURN)



#####TESTS#####

#####Creating new users
##2.0.1 - Test if user is able to create a new account with valid parameters
def test_create_new_user_new_username():
    login("janinedesiree", "T!t@nia_")
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("NewUser10", "T!t@nia_", "T!t@nia_")
    driver.find_element_by_name("_save").click()
    assert "was added successfully. You may edit it again below." in driver.page_source

##2.0.2 - Test that user is unable create new user with username that already exists
def test_create_new_user_existing_username():
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("janinedesiree", "T!t@nia_", "T!t@nia_")
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source

#2.0.3 - Test that user is unable to create a new user with passwords that do not match
def test_create_invalid_password_mismatched():
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("elysiaray", "oopsie1_", "oopsie1__")
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source

#2.0.4 - Test that user is unable to create a new user with a password that is less than 8 characters
def test_create_invalid_password_below_8():
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("elysiaray", "T!t@nia", "T!t@nia")
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source

#2.0.5 - Test that user is unable to create a new user with a password that is too common
def test_create_invalid_password_common():
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("elysiaray", "password", "password")
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source

#2.0.6 - Test that user is unable to create a new user with a password that is purely in numericals
def test_create_invalid_password_numerical():
    driver.get("http://localhost:8000/admin/auth/user/add/")
    add_edit_user_info("elysiaray", "12345678", "12345678")
    driver.find_element_by_name("_save").click()
    assert "Please correct the error below." in driver.page_source

#####Updating existing user
##2.1.0 - Test that user is able to update existing user with valid parameters
def test_valid_update():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('NewUser10').click()
    update("UpdatedUser01", "updated", "first and last", "new@email.com")
    assert "changed successfully" in driver.page_source

##2.1.1 - Test that user is unable to update existing user with blank username
def test_invalid_update_blank_username():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('UpdatedUser01').click()
    update("", "First", "Last", "new@email.com")
    assert "Please correct the error below." in driver.page_source

##2.1.2 - Test that user is unable to update existing user with blank first name
def test_valid_update_blank_first():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('UpdatedUser01').click()
    update("UpdatedUser02", "", "Last", "updated@email.com")
    assert "changed successfully" in driver.page_source

##2.1.3 - Test that user is unable to update existing user with blank last name
def test_valid_update_blank_last():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('UpdatedUser02').click()
    update("UpdatedUser03", "First", "", "updated@email.com")
    assert "changed successfully" in driver.page_source

##2.1.4 - Test that user is unable to update email with an incorrect email format
def test_invalid_update_email_format():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('UpdatedUser03').click()
    update("UpdatedUser04", "First", "Last", "janinedesiree")
    assert "Please correct the error below." in driver.page_source

###Updating Password
##2.1.5 - Test that user is unable to update password if they do not match
def test_invalid_change_password_mismatched():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword("00psie12_", "00psie12")
    assert "didn't match" in driver.page_source

##2.1.6 - Test that user is unable to update password if they are blank
def test_invalid_change_password_blank():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword(" ", " ")
    assert "error" in driver.page_source

##2.1.7 - Test that user is unable to update password if they are below 8 characters
def test_invalid_change_password_below_8():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword("w00ps_1", "w00ps_1")
    assert "error" in driver.page_source

##2.1.8 - Test that user is unable to update password if they are too common
def test_invalid_change_password_below_common():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword("password", "password")
    assert "error" in driver.page_source

##2.1.9 - Test that user is unable to update password if they are purely numerical
def test_invalid_change_password_below_numerical():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword("12345678", "12345678")
    assert "error" in driver.page_source

##2.1.10 - Test that user is able to update password with valid parameters
def test_valid_change_password():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('galeellamae').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/fieldset[1]/div[2]/div/div[2]/a').click()
    updatePassword("Time2log1n_", "Time2log1n_")
    assert "changed successfully" in driver.page_source


######Deleting existing user
##2.2.0 - Test that user is able to update delete an existing user
def test_delete_user():
    driver.get("http://localhost:8000/admin/auth/user/")
    driver.find_element_by_link_text('UpdatedUser03').click()
    driver.find_element(By.XPATH, '//*[@id="user_form"]/div/div/p/a').click()
    driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
    assert "deleted" in driver.page_source

######Check if user can log in after changing password
##2.3.0 - Test that user is unable to log in with old password
def test_old_login():
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    login("galeellamae", "T!t@nia_" )
    assert "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive." in driver.page_source

##2.3.1 - Test that user is able to log in with new password
def test_update_login():
    driver.get("http://localhost:8000/admin/login/?next=/admin/")
    login("galeellamae", "Time2log1n_" )
    assert driver.current_url == "http://localhost:8000/admin/"
    driver.close()
