Feature: Authorize to Paychex
  Scenario: Authorize to Paychex
    Given I run the authorize command
    Then the pychex-test.cfg file should contain the encrypted credentials

  Scenario: Print Paychex account summary
    Given I run the authorize command
    And I run the account_summary command
    Then I should see my account summary
