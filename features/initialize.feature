Feature: Initialize a Paychex object
  Scenario: Initialize a Paychex object with username only
    Given I create a Paychex object
    Then the Paychex object contains the needed urls
    And the Paychex object contains content-type shortcuts
    And the Paychex object contains a session
    And the Paychex object contains a logged_in member variable set to False
    And the Paychex object contains a app_username member variable set to None
    And the Paychex object contains a security_image_path member variable set to None
    And the Paychex object contains a current_balance member variable set to None
    And the Paychex object contains a vested_balance member variable set to None
    And the Paychex object contains a personal_ror member variable set to None
    And the Paychex object contains a balance_tab_info member variable set to None
    And the Paychex object contains initialized common_data

  Scenario: Initialize a Paychex object with username and security image
    Given I create a Paychex object with username and security image
    Then the Paychex object contains the needed urls
    And the Paychex object contains content-type shortcuts
    And the Paychex object contains a session
    And the Paychex object contains a logged_in member variable set to False
    And the Paychex object contains a app_username member variable set to None
    And the Paychex object contains the correct security image path
    And the Paychex object contains a current_balance member variable set to None
    And the Paychex object contains a vested_balance member variable set to None
    And the Paychex object contains a personal_ror member variable set to None
    And the Paychex object contains a balance_tab_info member variable set to None
    And the Paychex object contains initialized common_data
    And the get_security_image method returns the full security image url
