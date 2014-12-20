Feature: Authorize to Paychex
  Scenario: Authorize to Paychex
    Given I run the authorize command
    Then the config file should contain the encrypted credentials

  Scenario: Authorize to Paychex, answering 'y' to the security question
    Given I answer "y" to the security question during authorization
    Then the config file should contain the encrypted credentials

  Scenario: Authorize to Paychex, answering 'ye' to the security question
    Given I answer "ye" to the security question during authorization
    Then the config file should contain the encrypted credentials

  Scenario: Authorize to Paychex, answering '' to the security question
    Given I answer "" to the security question during authorization
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

  Scenario: Answer neither "yes" nor "no" to the security question
    Given I answer "I don't know" to the security question during authorization
    Then I should see a reminder to answer "yes" or "no"

  Scenario: Answer "no" to the security question
    Given I answer "no" to the security question during authorization
    Then I should see a notice that the security image didn't match

  Scenario: Answer "n" to the security question
    Given I answer "n" to the security question during authorization
    Then I should see a notice that the security image didn't match
