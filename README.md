# ToDo App Backend 📝

<hr />

###### This app basically provides API to fetch data.

###### Developed using Django REST Framework.

###### Database used is Postgres.

###### Hosted on heroku.

**APIs are as follow:**

- User Related ::

  \* **Sign Up ( /api-users/ )** -

  1. POST request :- posts new user's data to the database and returns "201: Created".
  2. GET request :- on this endpoint returns "403: Forbidden".
  3. ERROR :- returns "400 - Bad Request".

  \* **Login ( /api-users/login/<username> )** -

  1. GET request :- this endpoint takes username and password from URL params. Validates these credentials against database.
     a. If success returns "200 - OK"
     b. If user not present returns "404 - Not Found"
     c. If fail returns "401 - UNAUTHORIZED"

  \* **User Details ( /api-users/<username> )** -

  1. GET request :- fetches the user details based on the username provided in URL params and returns "200 - OK"
  2. PUT request :- updates the user details and returns "200 - OK"
  3. DELETE request :- returns "403 - Forbidden"

**_ Users logged in to the app can make below requests _**

- Task Related ::

  \* **Todo List ( /user-tasks/<user> )** -

  1. GET :- fetch user's task list
     a. if valid user returns "200 - OK"
     b. if invalid user returns "403 - Forbidden"
  2. POST :- add new task to the user's task list
     a. if valid user and task added returns "201 - Created"
     b. if invalid user returns "403 - Forbidden"
     c. if task not added returns "400 - Bad Request"
  3. DELETE :- deletes all the tasks of that user
     a. if valid user and tasks deleted returns "204 - No Content"
     b. if invalid user returns "403 - Forbidden"
  4. Error returns "404 - Not Found"

  \* **ToDo Details ( /user-tasks/<user>/<pk> )** -

  1. GET :- fetch details of that task for logged in user. returns "200 -OK"
  2. PUT :- update task details returns "200 - OK"
  3. DELETE :- delete that particular task. returns "204 - No Content"
  4. Erros :- return "403 - Forbidden" or "400 - Bad Request" or "404 - Not Found"
