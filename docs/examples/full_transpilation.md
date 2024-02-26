# How To Transpile a Pytorch Model

In this tutorial we learn the following topics:

* How to create a Pytorch model from scratch
* How to train the model
* How to export this model to ONNX
* How to transpile the model to Cairo using Giza CLI!
* How to run inference on the transpiled model

## Creating a Pytorch Model

In this section we will create a simple Pytorch model using the MNIST dataset. The MNIST dataset is a dataset of handwritten digits. The dataset consists of 60,000 training images and 10,000 test images. The images are grayscale, 28x28 pixels, and centered to reduce preprocessing and get started quicker. You can read more about the dataset [here](https://en.wikipedia.org/wiki/MNIST_database).

The first step is to install the libraries that we are going to use:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install giza-cli==0.12.2 onnx==1.14.1 torch==2.1.0 torchvision==0.16.0
```

We will use the libraries for the following purposes:

* `giza-cli` is used to transpile the model to Cairo
* `torch` is used to create the model and train it
* `onnx` is used to export the model to ONNX
* `torchvision` is used to load the MNIST dataset

Now we can import our dependencies and configure basic settings:



```python
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import warnings
warnings.filterwarnings("ignore")

learning_rate = 0.01
momentum = 0.5
log_interval = 10000

random_seed = 1
torch.backends.cudnn.enabled = False
torch.manual_seed(random_seed)
```




    <torch._C.Generator at 0x10bbcded0>



To download the dataset we will use the `torchvision` library to download the dataset and create a `DataLoader` object that we can use to iterate over the dataset.

Some actions that we need to perform on the dataset are:

* Resize the images to 14x14 pixels, as we will be using `Linear` layers and we need to reduce the number of parameters
* Flatten the images to a vector of 196 elements


```python
train_loader = torch.utils.data.DataLoader(
  torchvision.datasets.MNIST('/tmp', train=True, download=True,
                             transform=torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Resize((14,14)),
                                torchvision.transforms.Lambda(lambda x: torch.flatten(x)),
                             ])), shuffle=True)

test_loader = torch.utils.data.DataLoader(
  torchvision.datasets.MNIST('/tmp', train=False, download=True,
                             transform=torchvision.transforms.Compose([
                               torchvision.transforms.ToTensor(),
                               torchvision.transforms.Resize((14,14)),
                                torchvision.transforms.Lambda(lambda x: torch.flatten(x)),
                             ])), shuffle=True)
```

Now let's see an example of the data that we have just downloaded:


```python
examples = enumerate(test_loader)
batch_idx, (example_data, example_targets) = next(examples)
print(f"example_data.shape: {example_data.shape}")
print(f"example_targets.shape: {example_targets.shape}")
```

    example_data.shape: torch.Size([1, 196])
    example_targets.shape: torch.Size([1])


## How To Train The Model

Now it's time to train the model, for this we are going to define a basic neural network with 2 hidden layers and 1 output layer.

We will follow the usual way of training a model in Pytorch by creating a `torch.nn.Module` class and defining the `forward` method. The `forward` method is the method that will be called when we pass an input to the model.


```python
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(196, 10)
        self.fc2 = nn.Linear(10, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
```

Now let's instantiate the model and define the optimizer:


```python
network = Net()
optimizer = optim.SGD(network.parameters(), lr=learning_rate,
                      momentum=momentum)
```

Now we are going to create a training loop that will train the model for the desired number of epochs. We will feed the data into the network and calculate the loss. Then we will use the loss to calculate the gradients and update the weights of the network.


```python
train_losses = []
train_counter = []

def train(epoch):
  network.train()
  for batch_idx, (data, target) in enumerate(train_loader):
    optimizer.zero_grad()
    output = network(data)
    loss = F.nll_loss(output, target)
    loss.backward()
    optimizer.step()
    if batch_idx % log_interval == 0:
      print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
        epoch, batch_idx * len(data), len(train_loader.dataset),
        100. * batch_idx / len(train_loader), loss.item()))
      train_losses.append(loss.item())
      train_counter.append(
        (batch_idx*64) + ((epoch-1)*len(train_loader.dataset)))
```

Time to start training the model! We have chosen 10 epochs, but you can increase/decrease the number as you wish.


```python
for i in range(10):
    train(i)
```

    Train Epoch: 0 [0/60000 (0%)]	Loss: 2.143008
    Train Epoch: 0 [10000/60000 (17%)]	Loss: 0.013687
    Train Epoch: 0 [20000/60000 (33%)]	Loss: 0.142858
    Train Epoch: 0 [30000/60000 (50%)]	Loss: 0.171771
    Train Epoch: 0 [40000/60000 (67%)]	Loss: 4.330005
    Train Epoch: 0 [50000/60000 (83%)]	Loss: 0.002654
    Train Epoch: 1 [0/60000 (0%)]	Loss: 0.035651
    Train Epoch: 1 [10000/60000 (17%)]	Loss: 0.002056
    Train Epoch: 1 [20000/60000 (33%)]	Loss: 0.046558
    Train Epoch: 1 [30000/60000 (50%)]	Loss: 0.013240
    Train Epoch: 1 [40000/60000 (67%)]	Loss: 0.054755
    Train Epoch: 1 [50000/60000 (83%)]	Loss: 0.264868
    Train Epoch: 2 [0/60000 (0%)]	Loss: 0.116307
    Train Epoch: 2 [10000/60000 (17%)]	Loss: 0.006561
    Train Epoch: 2 [20000/60000 (33%)]	Loss: 2.750949
    Train Epoch: 2 [30000/60000 (50%)]	Loss: 0.000641
    Train Epoch: 2 [40000/60000 (67%)]	Loss: 0.001984
    Train Epoch: 2 [50000/60000 (83%)]	Loss: 0.000069
    Train Epoch: 3 [0/60000 (0%)]	Loss: 0.010279
    Train Epoch: 3 [10000/60000 (17%)]	Loss: 0.000068
    Train Epoch: 3 [20000/60000 (33%)]	Loss: 0.007274
    Train Epoch: 3 [30000/60000 (50%)]	Loss: 0.000202
    Train Epoch: 3 [40000/60000 (67%)]	Loss: 0.001901
    Train Epoch: 3 [50000/60000 (83%)]	Loss: 0.011818
    Train Epoch: 4 [0/60000 (0%)]	Loss: 0.026695
    Train Epoch: 4 [10000/60000 (17%)]	Loss: 0.000018
    Train Epoch: 4 [20000/60000 (33%)]	Loss: 0.087963
    Train Epoch: 4 [30000/60000 (50%)]	Loss: 0.017164
    Train Epoch: 4 [40000/60000 (67%)]	Loss: 0.010012
    Train Epoch: 4 [50000/60000 (83%)]	Loss: 0.000132
    Train Epoch: 5 [0/60000 (0%)]	Loss: 0.000029
    Train Epoch: 5 [10000/60000 (17%)]	Loss: 0.061885
    Train Epoch: 5 [20000/60000 (33%)]	Loss: 0.000262
    Train Epoch: 5 [30000/60000 (50%)]	Loss: 0.003394
    Train Epoch: 5 [40000/60000 (67%)]	Loss: 0.006318
    Train Epoch: 5 [50000/60000 (83%)]	Loss: 0.000012
    Train Epoch: 6 [0/60000 (0%)]	Loss: 0.000054
    Train Epoch: 6 [10000/60000 (17%)]	Loss: 0.000886
    Train Epoch: 6 [20000/60000 (33%)]	Loss: 0.000007
    Train Epoch: 6 [30000/60000 (50%)]	Loss: 0.000427
    Train Epoch: 6 [40000/60000 (67%)]	Loss: 0.339227
    Train Epoch: 6 [50000/60000 (83%)]	Loss: 0.000128
    Train Epoch: 7 [0/60000 (0%)]	Loss: 0.091982
    Train Epoch: 7 [10000/60000 (17%)]	Loss: 0.040187
    Train Epoch: 7 [20000/60000 (33%)]	Loss: 0.936580
    Train Epoch: 7 [30000/60000 (50%)]	Loss: 0.003259
    Train Epoch: 7 [40000/60000 (67%)]	Loss: 0.012328
    Train Epoch: 7 [50000/60000 (83%)]	Loss: 0.000088
    Train Epoch: 8 [0/60000 (0%)]	Loss: 0.001890
    Train Epoch: 8 [10000/60000 (17%)]	Loss: 0.018773
    Train Epoch: 8 [20000/60000 (33%)]	Loss: 0.000000
    Train Epoch: 8 [30000/60000 (50%)]	Loss: 0.000001
    Train Epoch: 8 [40000/60000 (67%)]	Loss: 0.103827
    Train Epoch: 8 [50000/60000 (83%)]	Loss: 0.016198
    Train Epoch: 9 [0/60000 (0%)]	Loss: 0.000028
    Train Epoch: 9 [10000/60000 (17%)]	Loss: 0.000041
    Train Epoch: 9 [20000/60000 (33%)]	Loss: 0.025466
    Train Epoch: 9 [30000/60000 (50%)]	Loss: 0.000639
    Train Epoch: 9 [40000/60000 (67%)]	Loss: 0.004122
    Train Epoch: 9 [50000/60000 (83%)]	Loss: 0.000008


Let's perform a simple prediction to see how the model performs:


```python
network.eval()

with torch.no_grad():
    pred = network(example_data)
print(f"Prediction: {pred.argmax()}")
print(f"Real Value: {example_targets.item()}")

```

    Prediction: 3
    Real Value: 3


Now we have our trained model and we can export it to ONNX. ONNX is an open format built to represent machine learning models. ONNX defines a common set of operators - the building blocks of machine learning and deep learning models - and a common file format to enable AI developers to use models with a variety of frameworks, tools, runtimes, and compilers. If you want to know more about it you can read the [documentation](https://onnx.ai/).

## How To Export The ONNX Model Using PyTorch

1. Ensure that your model is in evaluation mode. This can be done by calling `model.eval()`.
2. Generate a dummy input that matches the input size that your model expects. This can be done using `torch.randn()`. In this case we just use the example data.
3. Call `torch.onnx.export()`, passing in your model, the dummy input, and the desired output file name.

The reason we export our PyTorch model to ONNX is to increase interoperability. ONNX is a platform-agnostic format for machine learning models, meaning it can be used with various machine learning and deep learning frameworks. This allows developers to train a model in one framework (in this case, PyTorch) and then use the model in another framework for inference, in our case we will use the model in **Cairo**.


```python
torch.onnx.export(network, example_data, "mnist_pytorch.onnx")
```

Now our model is in the ONNX format, we can visually check the output using [Netron](https://github.com/lutzroeder/netron), it will allow us to check the final architecture and the operators used by the network.

![neural_network](img/mnist_pytorch_onnx.png)

## Transpile The Model Using Giza CLI!

We are now ready to transpile the model to Cairo using Giza CLI. Giza CLI is a command line tool that allows you to transpile ONNX models to Cairo. You can read more about in the [docs](https://cli.gizatech.xyz/).

The first step to start using Giza CLI is to create a user in the platform. You can do this by running the following command:

```console
❯ giza users create
Enter your username 😎: # YOUR USERNAME GOES HERE
Enter your password 🥷 : # YOUR PASSWORD GOES HERE
Confirm your password 👉🏻 : 
Enter your email 📧: # YOUR EMAIL GOES HERE
[giza][2023-10-12 12:04:06.072] Creating user in Giza ✅ 
[giza][2023-10-12 12:04:13.875] User created ✅. Check for a verification email 📧
```

You will be prompted to add your username, password and email. Finally you will need to verify your email address by clicking on the link that you will receive in your inbox.

![email](img/email.png)

Once we click the link we will be redirected to a verification endpoint and we will see a message saying that our email has been verified. Now we are ready to start using Giza CLI!

Let's start by login into the platform:

```console
❯ giza users login 
Enter your username 😎: # YOUR USERNAME GOES HERE
Enter your password 🥷 : # YOUR PASSWORD GOES HERE
[giza][2023-10-12 12:09:51.843] Log into Giza
[giza][2023-10-12 12:09:52.622] Credentials written to: {HOME DIRECTORY}/.giza/.credentials.json
[giza][2023-10-12 12:09:52.624] Successfully logged into Giza ✅
```

We should be ready to start using Giza's capabilities, we can easily check by running the following command:

```console
❯ giza users me
[giza][2023-10-12 12:11:37.153] Retrieving information about me!
{
  "username": "YOUR USERNAME GOES HERE",
  "email": "YOUR EMAIL GOES HERE",
  "is_active": true
}
```

Now we are ready to transpile our model to Cairo! We want to help you jumpstart your journey into ZKML by helping you to create this amazing models, we abstract you from the tedious process of introspecting the model and getting the information needed to use it in Cairo, that's why we build the transpilation process, to ease this and improve the iteration time from creating a model to using it in Cairo! 

Let's check how we can do it:

```console
❯ giza transpile mnist_pytorch.onnx --output-path mnist_cairo
[giza][2023-10-12 12:15:30.624] No model id provided, checking if model exists ✅ 
[giza][2023-10-12 12:15:30.625] Model name is: mnist_pytorch
[giza][2023-10-12 12:15:30.956] Model Created with id -> 1! ✅
[giza][2023-10-12 12:15:31.520] Sending model for transpilation ✅ 
[giza][2023-10-12 12:15:42.592] Transpilation recieved! ✅
[giza][2023-10-12 12:15:42.601] Transpilation saved at: mnist_cairo
```

To explain a bit what is happening here, we are calling the `giza transpile` command and passing the path to the ONNX model that we want to transpile. We are also passing the `--output-path` flag to specify the path where we want to save the transpiled model. If we don't pass this flag the model will be saved in the current directory under `cairo_model`.

We can see that we make reference to a `model` this is because in Giza we organize the transpilations under models and versions:

* A `model` is a collection of versions of the same model, we are iterating over the model and improving it we can create different versions of the same model and keep track of the changes.
* A `version` is a reference to the transpiled model, each new transpilation will be referenced as a new version of the model.

We handle the creation for you, and if the model has the same name we will re-use the model and create a new version under it. If you want to know more about the model and version concept you can read the [docs](https://cli.gizatech.xyz/).

Also, if you ever have a question about the commands that you can run you can always run `giza --help` or `giza COMMAND --help` to get more information about the command and the flags that you can use.

```console
❯ giza --help
```

Back to the transpilation!

So we have received a file that we have saved in the `mnist_cairo` directory, let's check the contents of the directory:

```console
❯ tree mnist_cairo
mnist_cairo
├── Scarb.toml
├── crates
│   ├── layer1
│   │   ├── Scarb.toml
│   │   └── src
│   │       ├── bias.cairo
│   │       ├── lib.cairo
│   │       └── weights.cairo
│   └── layer3
│       ├── Scarb.toml
│       └── src
│           ├── bias.cairo
│           ├── lib.cairo
│           └── weights.cairo
└── src
    ├── functions.cairo
    ├── inference.cairo
    └── lib.cairo

7 directories, 12 files
```

We have the basic structure of a Cairo project, we have a `src` directory that contains the `lib.cairo` file that contains the main logic of the model. We also have a `functions.cairo` file that contains the functions that we will use in the `lib.cairo` file. Finally we have a `inference.cairo` file that contains the code that we will use to run inference on the model.

The `crates` folder contains the weights and biases of the layers, it is done this way so when working on the main inference project the developer experience is better as the IDE will not try to parse the weights and biases with each change and just for the compilation.

## How To Perform an Inference Using Cairo

We have the Cairo code with our model, now we need to feed the data to the model and run inference. As currently `scarb cairo-run` does not support passing arguments to the program we will need to create a small input file `input.cairo` that will contain the input data that we want to feed to the model.

Also, we need to make some changes to the transpilation.

First, we need to change the `inference.cairo` file to use an input file, instead of an argument:

```diff
#inference.cairo
use orion::operators::tensor::{TensorTrait, FP16x16Tensor, Tensor};
use orion::operators::nn::{NNTrait, FP16x16NN};
use orion::numbers::FP16x16;
use layer1::weights::tensor1 as w1;
use layer1::bias::tensor1 as b1;
use layer3::weights::tensor3 as w3;
use layer3::bias::tensor3 as b3;
use mnist_pytorch::functions as f;
+ use mnist_pytorch::input::input;

    
+fn main() -> Tensor<FP16x16>{
-fn main(input: Tensor<FP16x16>) -> Tensor<FP16x16>{
-	let _0 = f::lin1(input);
+	let _0 = input();
	let _1 = f::lin2(_0, w1(), b1());
	let _2 = f::relu3(_1);
	let _3 = f::lin4(_2, w3(), b3());
	let _4 = f::logsoftmax5(_3);
	_4
}
```

Then add it to `lib.cairo`:

```diff
mod functions;
mod inference;
+mod input;
```

Now let's create the `input.cairo` file. For this we are going to take the example data that we used to train the model and we are going to convert it to Cairo tensors. In cairo the tensors that contains `floats` are represented as `FP16x16` numbers, so we need to convert the data to this format.


```python
def to_fixed_point(val, bits):
    return round(val * (2**bits))

def mnist_image_to_fixed_point(data):
    return [to_fixed_point(val.item(), 16) for val in data]


def generate_input_cairo(data):
    values = mnist_image_to_fixed_point(data)
    values = [f"FixedTrait::<FP16x16>::new({val}, {'true' if val < 0 else 'false'})" for val in values]
    return ",\n ".join(values)

input_cairo = generate_input_cairo(example_data[0])

with open("mnist_cairo/src/input.cairo", "w") as f:
    f.write("""
use array::{SpanTrait, ArrayTrait};
use orion::operators::tensor::{TensorTrait, FP16x16Tensor, Tensor};
use orion::numbers::{FixedTrait, FP16x16};
fn input() -> Tensor<FP16x16> {
    TensorTrait::<FP16x16>::new(
        array![196].span(),
        array![
    """)
    f.write(input_cairo)
    f.write("""
        ].span()
    )
}
    """)
```

Now we have the base to start working in our model!

Happy coding!
