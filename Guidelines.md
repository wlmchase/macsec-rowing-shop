# CS6417 - Software Security
Term Project for UNB MACSec course

## Detailed Guidelines

Each graduate student will develop a client-server-based application of their choice using any preferable
programming language. The application developed must have the following functionality:
1. Login page ((i) must be able to log in/out, (ii) change password, (iii) be able to add new
users/customers with least privileges) 3 points
2. Input field (such as feedback forum, contact page) 2 points
3. Buy or sell products 3 points
4. Database to store data securely 2 points
Total (Functional testing) 10 points

From the security perspective, you will start your project using the following steps:
1. Read about Agile and DevOps. Choose either of these.
This will be the first part in your project report. You must justify why did you choose a particular
one.
2. The second component of your project will be to think like an attacker. Before you start
development process, design the attack surface for your whole application and attack tree for the
login page and input field. Explore diverse attack scenarios from the literature/standards (e.g,
NIST, ISO).
3. Follow the remaining steps outlined in the selected SDLC to complete your project.
4. Due to time constraint, focus on testing your application for:
(i) Authentication: Verify the strength of authentication mechanism. Test for weak or easily
guessable passwords.
(ii) Check for proper input validation to prevent injection attacks such as SQL injection,
cross-site scripting (XSS), and command injection. Ensure that user inputs are sanitized
and validated before processing.
(iii) You can use automated testing tools. You can also explore fuzzing (if interested).
Along with functionality of the application, you will be asked to test your application using
some undesired input during demo presentation and marks will be awarded accordingly.