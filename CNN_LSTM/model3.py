import torch
from torch.nn import Linear, ReLU, LSTM, CrossEntropyLoss, Sequential, Conv1d, MaxPool1d, Module, BatchNorm2d, Dropout, Sigmoid, Flatten
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class LSTM1(Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super().__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state
        self.seq_length = seq_length #sequence length

        self.lstm = LSTM(input_size=input_size, hidden_size=hidden_size,
                          num_layers=num_layers, batch_first=True) #lstm
        self.fc_1 =  Linear(hidden_size, 100) #fully connected 1
        self.fc = Linear(100, num_classes) #fully connected last layer

        self.relu = ReLU()
    
    def forward(self,x):
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device) #hidden state
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out
