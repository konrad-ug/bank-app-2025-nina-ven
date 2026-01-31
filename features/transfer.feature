Feature: Transfer

Scenario: User is able to make transfer in
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "200"

Scenario: User is able to make transfer out
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "89092909246"
    And I make a correct transfer of type: "outgoing" and amount: "100" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "100"

Scenario: User is unable to make transfer out with more money than owned
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "89092909246"
    And I make a transfer with too much money of type: "outgoing" and amount: "300" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "200"

Scenario: User is able to make express transfer out
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "89092909246"
    And I make a correct transfer of type: "express" and amount: "100" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "99"

Scenario: User is unable to make express transfer out with more money than owned
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make a correct transfer of type: "incoming" and amount: "200" for account with pesel: "89092909246"
    And I make a transfer with too much money of type: "express" and amount: "201" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "200"

Scenario: User is unable to make express transfer of nonexistent type
    Given Account registry is empty
    When I create an account using name: "Jane", last name: "Doe", pesel: "89092909246"
    And I make an incorrect transfer of type: "fun" and amount: "201" for account with pesel: "89092909246"
    Then Account with pesel: "89092909246" has balance equal to "0"

Scenario: User is unable to make a transfer for nonexistent account
    Given Account registry is empty
    And I make an incorrect transfer of type: "incoming" and amount: "201" for account which does not exist with pesel: "89092909246"
