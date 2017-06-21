Testing Strategies
==================

General Concepts
------------------

* security vs. reliability vs. performance tests
* black-box vs. white-box

Further Reading
* [CMU: Software Testing](https://users.ece.cmu.edu/~koopman/des_s99/sw_testing/)
* [OWASP: Security Testing Web Applications throughout Automated Software
Tests](https://www.owasp.org/images/9/99/AutomatedSecurityTestingofWebApplications-StephendeVries.pdf)

Validate Acceptance Criteria
----------------------------

The acceptance criteria formalize success or failure of user stories. To
prevent incorrect implementation, also consider negative user stories (also
called *evil user stories* or *abuser story*). The goal is to identify
behavior (of the user as well as of the application) that is not intended
initially. If not identified, it is unlikely, that any developer will
write tests that consider the corresponding behavior.

### Summary
* identify unintended application behavior

Further Reading
* [OWASP: Agile Software Development: Don't Forget EVIL User Stories](https://www.owasp.org/index.php/Agile_Software_Development:_Don%27t_Forget_EVIL_User_Stories)
* [DZone: Adding Appsec to Agile](https://dzone.com/articles/adding-appsec-agile-security)


Coverage
--------

The code coverage measures how many lines of code are executed during
testing. It's a good idea to maximize coverage. It's not a good idea
to rely on the coverage. The coverage does not give any advice about
logical issues or cases, that are not considered in your code. However,
there should be a good reason for a low coverage. Having no time is
not a good reason.

### Summary
* maximize coverage
* do not rely on a high coverage
* justify a low coverage


Negative vs. Positive Tests
---------------------------

Positive tests validate the application's behavior for valid input,
while negative tests do so for invalid input. Make sure, you do not test
your code solely the positive manner. For every positive case try
writing two negative cases.

Writing positive tests helps clarifying the meaning of a successful
execution. The intuition is that a method succeeds if the return code is
as expected. But this is a fairly narrow approach since it does not take
other main or side-effects into account. So define precisely what is
considered a successful execution.

The goal of negative tests is to trigger exceptions. This comprises
logical issues as well as technical exceptions like python's
`ValueError`.

### Summary
* precisely define the successful execution
* write more negative tests than positive tests
* try to trigger exceptions and logical errors


Scope
------

Define the scope of your tests. Usually you do not want to test third
party library unless you really need to.

Fail
----

See your test fail at least once. To do so, implement a bug in your
code or experiment with the assertions. The goal is to verify that the
test does not pass although the code is buggy.



* fuzzing
* property testing
* trust boundaries
* automated vs. manual testing
* if you need to mock a lot, question your code

python specific
* `pytest.mark.parametrize` if you want to execute the test w/ different
  input
* random data by using `import faker`

