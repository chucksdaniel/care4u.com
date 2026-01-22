# CARE4U.com



#### JWT Base Authentication
In this project, we are going to implement `jwt` based authentication

The package we will be using for this is `python-jose` Python-jose is commonly used with FastAPI for JWT handling, even though it’s not explicitly listed everywhere in the official FastAPI docs

- FastAPI Is Library-agnostic
  - FastAPI deliberately avoids tying authentication to a specific JWT library.
  - JWT is not part of FastAPI
  - JWT handling is an implementation detail
  - Multiple valid libraries exist (python-jose, PyJWT, Authlib)

- Avoiding Vendor Lock-in If FastAPI officially endorsed one JWT library:
  - It would limit flexibility
  - It would increase maintenance burden
  - It would break apps if that library changed
  - Instead, FastAPI documents:
    - OAuth2 flows
    - Dependency injection
    - Security schemes
    …and leaves token creation/verification to you.

- Where to Find Proper Documentation ✅
  1. Official python-jose Documentation
   This is the primary source.
    🔗 GitHub README - https://github.com/mpdavis/python-jose
    Key sections to read:
    - JWT encoding/decoding
    - Supported algorithms (HS256, RS256)
    - Error handling (JWTError, ExpiredSignatureError)


If you want to generate a password

```bash
openssl rand -hex 32
```


(class) OAuth2PasswordRequestForm
This is a dependency class to collect the username and password as form data for an OAuth2 password flow.
The OAuth2 specification dictates that for a password flow the data should be collected using form data (instead of JSON) and that it should have the specific fields username and password.
All the initialization parameters are extracted from the request. [Read more](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope) 

If you using this method, You no longer send credential through the body, but through the form data. My question is with schema we have the flexibility of ensuring the email is a validate email using `Emailstr` here how is this achieved.


### Database Migration Tool

The ORM has a limitation, one of the limitation is that once a table has been created doesn't allow for the table upgrade or deleting. so you will have to manually update or drop the table

The solution is [documentation](https://alembic.sqlalchemy.org/en/latest/)


#### Alembic Command

- **Initializing Alembic** `alembic init alembic`

- **To migrate** 
    - You run the command `alembic revision --autogenerate -m "create users table"` this command generate the table 
    - To push the table to the database `alembic upgrade head`

alembic revision --autogenerate -m "create request table"


git add backend/alembic backend/alembic.ini backend/app/api/ backend/app/core/ backend/app/main.py backend/app/models/ backend/app/schemas/user.py

