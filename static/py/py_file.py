import torch
import torch.nn as nn



class Model_CNN (nn.Module):
    def __init__(self):
        super(Model_CNN, self).__init__()
        self.conv1 = nn.Conv2d(1,32,3)
        self.conv2 = nn.Conv2d(32,64,3)
        self.pool = nn.MaxPool2d(2)
        self.fc1 = nn.Linear(64 * 5 * 5, 128)
        self.fc2 = nn.Linear (128,10)

    def forward (self, x):
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.pool(x)
        x = x.view(-1, 64 * 5 *5)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)

        return x
    