import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import kagglehub

# Download latest version
# path = kagglehub.dataset_download("austinreese/craigslist-carstrucks-data")

# print("Path to dataset files:", path)
# Load your dataset
used_car_sales = pd.read_csv('data/raw/autoscout24-germany-dataset.csv')
text_columns = ['make', 'model', 'fuel']  # Update this list with all the columns that have text
for col in text_columns:
    used_car_sales[col] = used_car_sales[col].str.lower()

used_car_sales = used_car_sales.dropna()

# Split data into features and target
X = used_car_sales.drop(columns=['price', 'offerType'])  # Features
y = used_car_sales['price']  # Target variable

# Split data into training and validation sets (train first, then preprocess)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess Training Data
scaler = StandardScaler()
numerical_features = ['mileage', 'hp', 'year']  # Example numerical columns
X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])

# One-hot encoding for categorical variables (e.g., 'make', 'model', 'fuel', 'gear')
X_train = pd.get_dummies(X_train, columns=['make', 'model', 'fuel', 'gear'], drop_first=True)

# Preprocess Validation Data
X_val[numerical_features] = scaler.transform(X_val[numerical_features])
X_val = pd.get_dummies(X_val, columns=['make', 'model', 'fuel', 'gear'], drop_first=True)

# Ensure both train and validation sets have the same columns after one-hot encoding
X_train, X_val = X_train.align(X_val, join='left', axis=1, fill_value=0)
X_train = X_train.astype('int32')
X_val = X_val.astype('int32')
# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
X_val_tensor = torch.tensor(X_val.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)  # Make it a column vector
y_val_tensor = torch.tensor(y_val.values, dtype=torch.float32).view(-1, 1)

# Define the model
class CarPricePredictor(nn.Module):
    def __init__(self, input_dim):
        super(CarPricePredictor, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)  # First fully connected layer
        self.fc2 = nn.Linear(128, 64)         # Second fully connected layer
        self.fc3 = nn.Linear(64, 32)          # Third fully connected layer
        self.fc4 = nn.Linear(32, 1)           # Output layer (price)

        self.relu = nn.ReLU()  # ReLU activation function

    def forward(self, x):
        x = self.relu(self.fc1(x))  # Apply ReLU to first hidden layer
        x = self.relu(self.fc2(x))  # Apply ReLU to second hidden layer
        x = self.relu(self.fc3(x))  # Apply ReLU to third hidden layer
        x = self.fc4(x)             # No activation for the output layer (regression)
        return x

# Instantiate the model
input_dim = X_train.shape[1]  # The number of input features
model = CarPricePredictor(input_dim)

# Loss function and optimizer
criterion = nn.MSELoss()  # Mean Squared Error loss for regression
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Train the model
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    
    # Forward pass
    predictions = model(X_train_tensor)
    loss = criterion(predictions, y_train_tensor)
    
    # Backward pass
    optimizer.zero_grad()  # Zero the gradients
    loss.backward()  # Backpropagate
    optimizer.step()  # Update model parameters

    if (epoch + 1) % 10 == 0:  # Print every 10 epochs
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

# Evaluate the model
model.eval()
with torch.no_grad():
    predictions_val = model(X_val_tensor)
    val_loss = criterion(predictions_val, y_val_tensor)
    print(f"Validation Loss: {val_loss.item():.4f}")
