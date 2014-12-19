Feature: Authorize to Paychex
  Scenario: Authorize to Paychex
    Given I run the authorize command
    Then the config file should contain the encrypted credentials

  Scenario: Print Paychex account summary
    Given I run the authorize command
    And I run the account_summary command
    Then I should see my account summary

  Scenario: Try to print account summary before authorizing
    Given I have not authorized the CLI
    And I run the account_summary command
    Then we remind the user to authorize

  Scenario: Try to print account summary with a mangled config (missing section)
    Given my config is missing the pychex section
    And I run the account_summary command
    Then we remind the user to authorize

  Scenario: Try to print account summary with a mangled config (missing option)
    Given my config is missing an option
    And I run the account_summary command
    Then we remind the user to authorize
