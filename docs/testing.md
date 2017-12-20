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

Randomize Data
-----------

In order to verify that tests are performed with varying input, use
random data. Otherwise, the test only covers static cases that might
fail to trigger errors.

### Example

```Python

from faker import Faker

...

def test_send_request(..):
    fake = Faker()
    ...

    # Create project
    request = {
        'phases-TOTAL_FORMS': '2',
        'phases-INITIAL_FORMS': '0',
        'phases-0-id': '',
        'phases-0-start_date': '2016-10-01 16:12',
        'phases-0-end_date': '2016-10-01 16:13',
        'phases-0-name': 'Name 0',
        'phases-0-description': fake.text(max_nb_chars=200),
        'phases-0-type': 'euth_offlinephases:000:offline',
        'phases-0-weight': '0',
        'phases-0-delete': '0',
        'phases-1-id': '',
        'phases-1-start_date': '2016-10-01 16:14',
        'phases-1-end_date': '2016-10-01 16:15',
        'phases-1-name': 'Name 1',
        'phases-1-description': 'Description 1',
        'phases-1-type': 'euth_ideas:020:collect',
        'phases-1-weight': '1',
        'phases-1-delete': '0',
        'project-description': 'Project description',
        'project-name': 'Project name',
        'project-information': 'Project info',
    }

    response = client.post(url, request)

    assert response.status_code == 302, str(request)
```

Note that the fake object provides random data. If the test fails, it
might be hard to reproduce the exact input. Hence, we print the
request in the `assert` statement in case of error.

This example only covers some fields. Feel free to randomize as many as
possible.

### Summary

* test with random data
* print the data triggering the error

-----

* fuzzing
* property testing
* trust boundaries
* automated vs. manual testing
* if you need to mock a lot, question your code
* `pytest.mark.parametrize` if you want to execute the test w/ different
  input

