# Online Judge (Online code evaluation system)

### All project files added in branch master. Project information shown here:


## Overview

This project is an Online Judge system built using Django. It allows users to register, login, browse programming problems, submit solutions, and receive automated feedback on their submissions. The project consists of three main applications:
1. `accounts` - Handles user authentication and profile management.
2. `home` - Manages problem statements, test cases, and submitted solutions.
3. `compiler` - Compiles the code and checks if the problem submitted is correct or incorrect using the testcases.

## Features

- **User Authentication**: Registration, login, logout management.
- **Problem Management**: View programming problems.
- **Submission Management**: Submit solutions, view submission status, and results.

## Technologies Used

- **Django**: Web framework for the backend.
- **SQLite**: Default database for development (can be switched to PostgreSQL/MySQL for production).
- **HTML/CSS**: Frontend technologies for creating responsive and interactive UIs.
- **Bootstrap**: Frontend framework for styling.

## Applications

### Accounts

- **URLs**:
  - `/auth/register/` - User registration.
  - `/auth/login/` - User login.
  - `/auth/logout/` - User logout.

- **Views**:
  - `Register_User` - Handles user registration.
  - `Login_User` - Handles user login.
  - `Logout_User` - Handles user logout.

- **Models**:
  - `User` - The default Django user model.

### Problems

- **URLs**:
  - `/home` - List all problems.
  - `/home/<id>/` - GET: View problem details. POST: Submit solution to problem.

- **Views**:
  - `ProblemDisplay` - Displays a list of all problems.
  
  - `ProblemDetail` - Displays the details of a specific problem.

- **Models**:
  - `Problem` - Stores problem details including title, description, and difficulty.
  - `TestCase` - Stores test cases for each problem, including input and expected output.
  - `Solution` - Stores submitted solutions, including the user who submitted it, the problem it is for, the solution code, and the result of the automated testing.

### Compiler

- **Views**:
  - `Post` - It takes the problem id of the problem, language and code. It then runs the submission submitted by the user and checks the resultant output with the reference output to check if the solution is correct or not.

- **Models**:
  - `Submission` - For submission of the code by the user.

  - `Result` - Output of the code submitted by the user. If it got Accepted or Wrong Answer or Compilation error. Time Limit Exceeded will be added soon.


### Upgradation

* Time Limit Exceeded part will be added.
* Admin dashboard for adding problems, testcases and output will be added via dashboard. For now it is done by django-admin.
* UI will improved.


## Demo

Video link of my project : (Link) : https://www.loom.com/share/b279231e09a8444b97db747b46ccc339?sid=9cbc2019-cdd1-47ed-ad97-b1cbd5a95601



