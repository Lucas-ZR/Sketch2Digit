# Sketch2Num

A web application that recognizes handwritten digits using a CNN trained on MNIST data.

## Features
- Interactive 28x28 drawing canvas
- Real-time digit prediction with confidence scores
- Simple Flask API backend
- Rate limiting for API protection

## Tech Stack
- **Backend**: Flask, PyTorch
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Model**: Convolutional Neural Network trained on binarized MNIST

## How it works
The model was trained on binarized MNIST data (converting grayscale to binary) to match the drawing canvas output. Achieves ~75% accuracy on hand-drawn test data.

## Usage
1. Draw a digit on the grid
2. Click "Run Model" to get predictions
3. View confidence scores in the bar chart

## Running locally
```bash
git clone [repository-url]
cd sketch2num
pip install -r requirements.txt
flask run
```

## Architecture
Simple CNN: Conv2D → ReLU → MaxPool → Conv2D → ReLU → MaxPool → FC → ReLU → FC

## Live Demo
URL
