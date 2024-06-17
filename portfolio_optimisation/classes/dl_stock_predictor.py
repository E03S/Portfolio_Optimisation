import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm
import numpy as np
from typing import List
from sklearn.metrics import r2_score
import plotly 
from plotly.subplots import make_subplots
import plotly.graph_objects
from IPython.display import clear_output

class StockPredictor(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout_prob=0.5):
        super(StockPredictor, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc1 = nn.Linear(hidden_dim, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        self.dropout = nn.Dropout(dropout_prob)
        self.batch_norm1 = nn.BatchNorm1d(128)
        self.batch_norm2 = nn.BatchNorm1d(64)
        self.num_layers = num_layers
        self.hidden_dim = hidden_dim

    def forward(self, x):
        # Изменим форму входного тензора
        x = x.unsqueeze(1)  # Добавляем размерность для sequence_length, чтобы стало (batch_size, sequence_length, input_dim)
        
        # Инициализация скрытых состояний
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)
        
        # LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Получение только последнего выходного состояния
        out = out[:, -1, :]
        
        # Полносвязные слои с нормализацией и дроп-аутом
        out = self.fc1(out)
        out = self.batch_norm1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.batch_norm2(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc3(out)
        return out
