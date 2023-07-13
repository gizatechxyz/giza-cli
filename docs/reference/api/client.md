<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `client`




**Global Variables**
---------------
- **DEFAULT_API_VERSION**
- **GIZA_TOKEN_VARIABLE**


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ApiClient`
Implementation of the API client to interact with core-services

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_token`

```python
retrieve_token(
    user: Optional[str] = None,
    password: Optional[str] = None,
    renew: bool = False
) → None
```

Get the JWT token.

First,  it will try to get it from GIZA_TOKEN. Second, from ~/.giza/.credentials.json. And finally it will try to retrieve it from the API login the user in.



**Args:**

 - <b>`user`</b>:  if provided it will be used to check against current credentials  and if provided with `password` used to retrieve a new token.
 - <b>`password`</b>:  if provided with `user` it will be used to retrieve a new token.
 - <b>`renew`</b>:  for renewal of the JWT token by user login.



**Raises:**

 - <b>`Exception`</b>:  if token could not be retrieved in any way


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UsersClient`
Client to interact with `users` endpoint.

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(user: UserCreate) → UserResponse
```

Call the API to create a new user



**Args:**

 - <b>`user`</b> (users.UserCreate):  information used to create a new user



**Returns:**

 - <b>`users.UserResponse`</b>:  the created user information

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `me`

```python
me() → UserResponse
```

Retrieve information about the current user. Must have a valid token to perform the operation, enforced by `@auth`



**Returns:**

 - <b>`users.UserResponse`</b>:  User information from the server

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_token`

```python
retrieve_token(
    user: Optional[str] = None,
    password: Optional[str] = None,
    renew: bool = False
) → None
```

Get the JWT token.

First,  it will try to get it from GIZA_TOKEN. Second, from ~/.giza/.credentials.json. And finally it will try to retrieve it from the API login the user in.



**Args:**

 - <b>`user`</b>:  if provided it will be used to check against current credentials  and if provided with `password` used to retrieve a new token.
 - <b>`password`</b>:  if provided with `user` it will be used to retrieve a new token.
 - <b>`renew`</b>:  for renewal of the JWT token by user login.



**Raises:**

 - <b>`Exception`</b>:  if token could not be retrieved in any way


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TranspileClient`
Client to interact with `users` endpoint.

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_token`

```python
retrieve_token(
    user: Optional[str] = None,
    password: Optional[str] = None,
    renew: bool = False
) → None
```

Get the JWT token.

First,  it will try to get it from GIZA_TOKEN. Second, from ~/.giza/.credentials.json. And finally it will try to retrieve it from the API login the user in.



**Args:**

 - <b>`user`</b>:  if provided it will be used to check against current credentials  and if provided with `password` used to retrieve a new token.
 - <b>`password`</b>:  if provided with `user` it will be used to retrieve a new token.
 - <b>`renew`</b>:  for renewal of the JWT token by user login.



**Raises:**

 - <b>`Exception`</b>:  if token could not be retrieved in any way

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `transpile`

```python
transpile(f: <class 'BinaryIO'>) → Response
```

Make a call to the API transpile endpoint with the model as a file.



**Args:**

 - <b>`f`</b> (BinaryIO):  model to send for transpilation



**Returns:**

 - <b>`Response`</b>:  raw response from the server with the transpiled model as a zip
