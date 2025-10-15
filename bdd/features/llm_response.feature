Feature: LLM Responses

  Scenario Outline: Factual answer
    Given the API is running
    When I send the prompt "<prompt>"
    Then the response should contain "<expected>"

  Examples:
    | prompt                         | expected |
    | What is the capital of France? | Paris    |
    | Largest planet in solar system?| Jupiter  |

