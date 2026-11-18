Feature: Application Smoke Verification (UI & API)

  @ui @smoke @login
  Scenario: Verify successful login with standard user
    Given the user navigates to the login page
    When the user logs in with username "standard_user" and password "secret_sauce"
    Then the user should see the inventory page header

  @ui @login @negative
  Scenario: Verify error message for locked out user
    Given the user navigates to the login page
    When the user logs in with username "locked_out_user" and password "secret_sauce"
    Then the user should see the error message "Sorry, this user has been locked out."

  @api @smoke
  Scenario: Retrieve user details by ID via API
    When the user requests API details for user "1"
    Then the API response status code should be 200
    And the response body should contain username "emilys"

  @api @smoke
  Scenario: Create a new user resource via API
    When the user creates a new user with firstName "Alex" and lastName "Hunter"
    Then the API response status code should be 201
    And the response body should contain firstName "Alex"
