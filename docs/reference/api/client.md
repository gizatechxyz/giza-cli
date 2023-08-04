<!-- markdownlint-disable -->

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `client`




**Global Variables**
---------------
- **DEFAULT_API_VERSION**
- **GIZA_TOKEN_VARIABLE**
- **MODEL_URL_HEADER**


---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ApiClient`
Implementation of the API client to interact with core-services 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UsersClient`
Client to interact with `users` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `me`

```python
me() → UserResponse
```

Retrieve information about the current user. Must have a valid token to perform the operation, enforced by `@auth` 



**Returns:**
 
 - <b>`users.UserResponse`</b>:  User information from the server 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L275"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TranspileClient`
Client to interact with `users` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L282"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ModelsClient`
Client to interact with `models` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(model_create: ModelCreate) → Tuple[Model, str]
```

Create a new model. 



**Args:**
 
 - <b>`model_create`</b>:  Model information to create 



**Raises:**
 
 - <b>`Exception`</b>:  if there is no upload Url 



**Returns:**
 
 - <b>`Tuple[Model, str]`</b>:  the recently created model and a url, used to upload the model. 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L422"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `download`

```python
download(model_id: int) → bytes
```

Download a Transpiled model from the API. 



**Args:**
 
 - <b>`model_id`</b>:  Model identfier to download 



**Returns:**
 The model content of the request 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L315"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(model_id: int) → Model
```

Make a call to the API to retrieve model information. 



**Args:**
 
 - <b>`model_id`</b>:  Model identfier to retrieve information 



**Returns:**
 
 - <b>`Model`</b>:  model entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L394"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L457"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobsClient`
Client to interact with `jobs` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L489"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(job_create: JobCreate, f: BufferedReader) → Job
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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L464"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(job_id: int) → Job
```

Make a call to the API to retrieve job information. 



**Args:**
 
 - <b>`job_id`</b>:  Job identfier to retrieve information 



**Returns:**
 
 - <b>`Job`</b>:  job entity with the retrieved information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L521"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list() → List[Job]
```

List jobs. 



**Returns:**
  A list of jobs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L545"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProofsClient`
Client to interact with `proofs` endpoint. 

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L603"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L552"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L577"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_job_id`

```python
get_by_job_id(job_id: int) → Proof
```

Make a call to the API to retrieve proof information. 



**Args:**
 
 - <b>`proof_id`</b>:  Proof identfier to retrieve information 



**Returns:**
 
 - <b>`Proof`</b>:  proof entity with the desired information 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/utils/decorators.py#L636"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `list`

```python
list() → List[Proof]
```

List Proofs. 



**Returns:**
  A list of proofs created by the user 

---

<a href="https://github.com/gizatechxyz/giza-cli/blob/main/giza/client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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


