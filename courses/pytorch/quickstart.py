import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


# Download training data from open datasets
train_data = datasets.FashionMNIST(
                                root='data/',
                                train=True,
                                download=True,
                                transform=ToTensor()
                          )
# Download test data from open datasets
test_data = datasets.FashionMNIST(
                                root='data/',
                                train=False,
                                download=True,
                                transform=ToTensor()
                          )

# Dataloader wraps Dataset for us.
# It supports automatic batching,
# sampling, shuffling and other
BATCH_SIZE = 64
train_dataloader = DataLoader(dataset=train_data,
                              batch_size=BATCH_SIZE)
test_dataloader = DataLoader(dataset=test_data,
                             batch_size=BATCH_SIZE)

print(f'Number of batches in train_loader: {len(train_dataloader)}')
print(f'Number of batches in test_loader: {len(test_dataloader)}')

for X, y in test_dataloader:
    print(f'Shape of X (batch): {X.shape}')
    print(f'Shape of y (batch): {y.shape}')
    break

# set the available device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'We use {device} device')


# Create a model
# class inherits from nn.Module
# layers definitions in `__init__` functions
# specify how data will pass through the network in `forward` function
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_stack = nn.Sequential(
            nn.Linear(in_features=28*28, out_features=512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_stack(x)
        return logits


network_model = NeuralNetwork()
print(f'Our model is {network_model}')

# we need a loss function for evaluate error
# we need an optimizer to prune model's parameters
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(network_model.parameters(), lr=1e-3)


def train_loop(dataloader, model, loss, optim):
    size = len(dataloader.dataset)  # all elements in all batches
    model.train()

    for n_batch, (X_batch, y_batch) in enumerate(dataloader):
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        # error
        pred = model(X_batch)  # apply `forward` function
        # pred.shape = (64, 10) where 64 = len(batch), 10 = num of classes
        loss_value = loss(pred, y_batch)

        # parameters update
        optim.zero_grad()
        loss_value.backward()
        optim.step()

        if n_batch % 300 == 0:
            loss_value = loss_value.item()
            number_of_elements = n_batch * len(X_batch)

            print(f'Elements: {number_of_elements}/{size} || loss value is {loss_value}')


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_of_batches = len(dataloader)
    model.eval()
    test_error, correct = 0, 0
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            pred = model(X_batch)
            test_error += loss_fn(pred, y_batch).item()
            # calculate how many elements in batch
            # has been predicted correctly by our model
            correct += (pred.argmax(dim=1) == y_batch).type(torch.float32).sum().item()

    mean_test_error_per_batch = test_error / num_of_batches
    accuracy = (correct / size) * 100
    print(f' Test average loss: {mean_test_error_per_batch},\n Accuracy: {accuracy:>0.1f}%')


EPOCHS = 3
for epoch in range(EPOCHS):
    print(f'epoch number {epoch+1}')
    train_loop(dataloader=train_dataloader,
               model=network_model,
               loss=loss_function,
               optim=optimizer)
    test_loop(dataloader=test_dataloader,
              model=network_model,
              loss_fn=loss_function)

print('Done!')


# common way to save mode
torch.save(network_model.state_dict(),
           './models/quickstart_model.pth')
print('model is saved')

# common way to load model
new_model = NeuralNetwork()
new_model.load_state_dict(torch.load('./models/quickstart_model.pth'))
print('New model is\n', new_model)

# make predictions
classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

new_model.eval()
x, y = test_data[0][0], test_data[0][1]
print(f'shape of `x` is {x.shape} and `y` (original class) is {classes[y]}')
with torch.no_grad():
    prediction = new_model(x)
    print(f'shape of prediction is {prediction.shape}')
    prediction = prediction[0].argmax(dim=0)
    print(f'model predict this object as {classes[prediction]}')