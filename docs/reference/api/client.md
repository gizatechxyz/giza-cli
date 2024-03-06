<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `client`




**Global Variables**
---------------
- **DEFAULT_API_VERSION**
- **GIZA_TOKEN_VARIABLE**
- **MODEL_URL_HEADER**
- **API_KEY_HEADER**


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ApiClient`
Implementation of the API client to interact with core-services 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UsersClient`
Client to interact with `users` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L296"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L320"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create_api_key`

```python
create_api_key()
```

Call the API to create a new API key 



**Returns:**
 
 - <b>`users.UserResponse`</b>:  the created user information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `me`

```python
me() → UserResponse
```

Retrieve information about the current user. Must have a valid token to perform the operation, enforced by `@auth` 



**Returns:**
 
 - <b>`users.UserResponse`</b>:  User information from the server 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `request_reset_password_token`

```python
request_reset_password_token(email: str) → Msg
```

Sends a request to the server to generate a password reset token. The token is sent to the user's email. 



**Args:**
 
 - <b>`email`</b> (str):  The email of the user who wants to reset their password. 



**Returns:**
 
 - <b>`Msg`</b>:  A message indicating the success or failure of the request. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `resend_email`

```python
resend_email(email: str) → Msg
```

Resend the verification email to the user. 



**Args:**
 
 - <b>`email`</b> (EmailStr):  The email of the user who wants to resend the verification email. 



**Returns:**
 
 - <b>`Msg`</b>:  A message indicating the success or failure of the request. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L413"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset_password`

```python
reset_password(token: str, new_password: str) → Msg
```

Resets the user's password using the provided token and new password. 



**Args:**
 
 - <b>`token`</b> (str):  The password reset token sent to the user's email. 
 - <b>`new_password`</b> (str):  The new password the user wants to set. 



**Returns:**
 
 - <b>`Msg`</b>:  A message indicating the success or failure of the password reset. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L438"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EndpointsClient`
Client to interact with `endpoints` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(
    model_id: int,
    version_id: int,
    endpoint_create: EndpointCreate,
    f: BufferedReader
) → Endpoint
```

Create a new deployment. 



**Args:**
 
 - <b>`endpoint_create`</b>:  Endpoint information to create 



**Returns:**
 The recently created deployment information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete`

```python
delete(endpoint_id: int) → None
```

Delete an endpoint. 



**Args:**
 
 - <b>`endpoint_id`</b>:  Endpoint identifier 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_proof`

```python
download_proof(endpoint_id: int, proof_id: int) → bytes
```

Download a proof. 



**Args:**
 
 - <b>`proof_id`</b>:  Proof identifier 



**Returns:**
 The proof binary file 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(endpoint_id: int) → Endpoint
```

Get a deployment. 



**Args:**
 
 - <b>`endpoint_id`</b>:  Endpoint identifier 



**Returns:**
 The deployment information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L569"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_proof`

```python
get_proof(endpoint_id: int, proof_id: int) → Proof
```

Return information about a specific proof. `proof_if` is the identifier of the proof that can be a integer or the request id. 



**Returns:**
  A proof created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L484"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(params: Optional[Dict[str, str]] = None) → EndpointsList
```

List endpoints. 



**Returns:**
  A list of endpoints created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L513"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_jobs`

```python
list_jobs(endpoint_id: int) → JobList
```

List proofs. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L541"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_proofs`

```python
list_proofs(endpoint_id: int) → ProofList
```

List proofs. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L438"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EndpointsClient`
Client to interact with `endpoints` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(
    model_id: int,
    version_id: int,
    endpoint_create: EndpointCreate,
    f: BufferedReader
) → Endpoint
```

Create a new deployment. 



**Args:**
 
 - <b>`endpoint_create`</b>:  Endpoint information to create 



**Returns:**
 The recently created deployment information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete`

```python
delete(endpoint_id: int) → None
```

Delete an endpoint. 



**Args:**
 
 - <b>`endpoint_id`</b>:  Endpoint identifier 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_proof`

```python
download_proof(endpoint_id: int, proof_id: int) → bytes
```

Download a proof. 



**Args:**
 
 - <b>`proof_id`</b>:  Proof identifier 



**Returns:**
 The proof binary file 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(endpoint_id: int) → Endpoint
```

Get a deployment. 



**Args:**
 
 - <b>`endpoint_id`</b>:  Endpoint identifier 



**Returns:**
 The deployment information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L569"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_proof`

```python
get_proof(endpoint_id: int, proof_id: int) → Proof
```

Return information about a specific proof. `proof_if` is the identifier of the proof that can be a integer or the request id. 



**Returns:**
  A proof created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L484"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(params: Optional[Dict[str, str]] = None) → EndpointsList
```

List endpoints. 



**Returns:**
  A list of endpoints created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L513"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_jobs`

```python
list_jobs(endpoint_id: int) → JobList
```

List proofs. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L541"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list_proofs`

```python
list_proofs(endpoint_id: int) → ProofList
```

List proofs. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L698"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TranspileClient`
Client to interact with `users` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L707"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `transpile`

```python
transpile(f: <class 'BinaryIO'>) → Response
```

Make a call to the API transpile endpoint with the model as a file. 



**Args:**
 
 - <b>`f`</b> (BinaryIO):  model to send for transpilation 



**Returns:**
 
 - <b>`Response`</b>:  raw response from the server with the transpiled model as a zip 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L730"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_transpilation`

```python
update_transpilation(
    model_id: int,
    version_id: int,
    f: <class 'BinaryIO'>
) → None
```

Make a call to the API transpile endpoint with the model as a file. 



**Args:**
 
 - <b>`f`</b> (BinaryIO):  model to send for transpilation 



**Returns:**
 
 - <b>`Response`</b>:  raw response from the server with the transpiled model as a zip 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L765"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ModelsClient`
Client to interact with `models` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L837"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(model_create: ModelCreate) → Model
```

Create a new model. 



**Args:**
 
 - <b>`model_create`</b>:  Model information to create 



**Raises:**
 
 - <b>`Exception`</b>:  if there is no upload Url 



**Returns:**
 
 - <b>`Tuple[Model, str]`</b>:  the recently created model and a url, used to upload the model. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L772"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(model_id: int, **kwargs) → Model
```

Make a call to the API to retrieve model information. 



**Args:**
 
 - <b>`model_id`</b>:  Model identfier to retrieve information 



**Returns:**
 
 - <b>`Model`</b>:  model entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L819"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_name`

```python
get_by_name(model_name: str, **kwargs) → Optional[Model]
```

Make a call to the API to retrieve model information by its name. 



**Args:**
 
 - <b>`model_name`</b>:  Model name to retrieve information 



**Returns:**
 
 - <b>`Model`</b>:  model entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L797"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(**kwargs) → ModelList
```

List all the models related to the user. 



**Returns:**
  A list of models created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L865"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update`

```python
update(model_id: int, model_update: ModelUpdate) → Model
```

Update a model. 



**Args:**
 
 - <b>`model_id`</b>:  Model identfier to retrieve information 
 - <b>`model_update`</b>:  body to partially update the model 



**Returns:**
 
 - <b>`Model`</b>:  the updated model 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L892"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobsClient`
Client to interact with `jobs` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L924"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(
    job_create: JobCreate,
    trace: BufferedReader,
    memory: Optional[BufferedReader] = None
) → Job
```

Create a new job. 



**Args:**
 
 - <b>`job_create`</b>:  Job information to create 
 - <b>`f`</b>:  filed to upload, a CASM json 



**Raises:**
 
 - <b>`Exception`</b>:  if there is no upload Url 



**Returns:**
 
 - <b>`Tuple[Model, str]`</b>:  the recently created model and a url, used to upload the model. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L899"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(job_id: int, params: Optional[dict[str, str]] = None) → Job
```

Make a call to the API to retrieve job information. 



**Args:**
 
 - <b>`job_id`</b>:  Job identfier to retrieve information 



**Returns:**
 
 - <b>`Job`</b>:  job entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L962"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list() → List[Job]
```

List jobs. 



**Returns:**
  A list of jobs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L984"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `VersionJobsClient`
Client to interact with `jobs` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1027"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(
    model_id: int,
    version_id: int,
    job_create: JobCreate,
    f: BufferedReader
) → Job
```

Create a new job. 



**Args:**
 
 - <b>`job_create`</b>:  Job information to create 
 - <b>`f`</b>:  filed to upload, a CASM json 



**Raises:**
 
 - <b>`Exception`</b>:  if there is no upload Url 



**Returns:**
 
 - <b>`Tuple[Model, str]`</b>:  the recently created model and a url, used to upload the model. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L993"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(model_id: int, version_id: int, job_id: int) → Job
```

Make a call to the API to retrieve job information. 



**Args:**
 
 - <b>`job_id`</b>:  Job identfier to retrieve information 



**Returns:**
 
 - <b>`Job`</b>:  job entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1067"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(model_id: int, version_id: int) → List[Job]
```

List jobs. 



**Returns:**
  A list of jobs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L1098"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProofsClient`
Client to interact with `proofs` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download`

```python
download(proof_id: int) → bytes
```

Download a proof. 



**Args:**
 
 - <b>`proof_id`</b>:  Proof identifier 



**Returns:**
 The proof binary file 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(proof_id: int) → Proof
```

Make a call to the API to retrieve proof information. 



**Args:**
 
 - <b>`proof_id`</b>:  Proof identfier to retrieve information 



**Returns:**
 
 - <b>`Proof`</b>:  proof entity with the desired information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_job_id`

```python
get_by_job_id(job_id: int) → Proof
```

Make a call to the API to retrieve proof information based on the job id. 



**Args:**
 
 - <b>`job_id`</b>:  Job identifier to query by. 



**Returns:**
 
 - <b>`Proof`</b>:  proof entity with the desired information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1185"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list() → List[Proof]
```

List all the proofs related to the user. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L1207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `VersionsClient`
Client to interact with `versions` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1287"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(
    model_id: int,
    version_create: VersionCreate,
    filename: Optional[str] = None
) → Tuple[Version, str]
```

Create a new version. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_create`</b>:  Version information to create 



**Returns:**
 The recently created version information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download`

```python
download(model_id: int, version_id: int, params: Dict) → Dict[str, bytes]
```

Download a version. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_id`</b>:  Version identifier 
 - <b>`params`</b>:  Additional parameters to pass to the request 



**Returns:**
 The version binary file 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1374"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download_original`

```python
download_original(model_id: int, version_id: int) → bytes
```

Download the original version. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_id`</b>:  Version identifier 



**Returns:**
 The version binary file 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(model_id: int, version_id: int) → Version
```

Get a version. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_id`</b>:  Version identifier 



**Returns:**
 The version information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1428"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list(model_id: int) → VersionList
```

List all the versions related to a model. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 



**Returns:**
 A list of versions related to the model 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1452"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update`

```python
update(model_id: int, version_id: int, version_update: VersionUpdate) → Version
```

Update a specific version. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_id`</b>:  Version identifier 
 - <b>`version_update`</b>:  Version information to update 



**Returns:**
 The updated version information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `upload_cairo`

```python
upload_cairo(model_id: int, version_id: int, file_path: str) → str
```

Get the Cairo model URL. 



**Args:**
 
 - <b>`model_id`</b>:  Model identifier 
 - <b>`version_id`</b>:  Version identifier 



**Returns:**
 The Cairo model URL 


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L1482"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WorkspaceClient`
Client to interact with `workspaces` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    host: str,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: str = 'v1',
    verify: bool = True,
    debug: Optional[bool] = False
) → None
```








---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1510"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create() → Workspace
```

Call the API to create a new workspace. If the workspace already exists it will return a 400. 



**Returns:**
 
 - <b>`Workspace`</b>:  the created workspace information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1533"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete`

```python
delete() → None
```

Call the API to delete the workspace. If the workspace does not exist it will return a 404. 



**Returns:**
  None 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L1489"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get() → Workspace
```

Make a call to the API to retrieve workspace information. Only one should exist. 



**Returns:**
 
 - <b>`Workspace`</b>:  workspace information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `retrieve_api_key`

```python
retrieve_api_key() → None
```

Retrieve the API key from the `~/.giza/.api_key.json` file. 



**Raises:**
 
 - <b>`Exception`</b>:  if the file does not exist 



**Returns:**
 
 - <b>`str`</b>:  the API key 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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


