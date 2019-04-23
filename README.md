# Customer-Support-Chatbot
Customer Support Chatbot (Senior Project) - Neural Net and Bayes implementation

## Installation Requirements
### Opearting System Requirement 
- Ubuntu 16.04
- Nvidia GPU

### Software Requirements 
- NVIDIA - CUDA (9.0)  
- NVIDIA - CUDNN (7.0)  
    
### Package Requirements
- sudo add-apt-repository ppa:deadsnakes/ppa
- Tensorflow-gpu (1.4)
- Tensorflow (1.4)
- python3.6
- python3.6-dev
- regex
- python3
- python3-pip
- ipython3
- build-essential
- python-dev
- python3-dev

### Additional Instructions:  
- call all python applications as "python3.6"

## Running the Application  
In order to run the application, you can run the following command within the "ChatBot" Directory:  
`sudo python3.6 Main1.py`

## Modifying 
### Neural Net Data
The Neural Net uses a ".from" and ".to" file in order to train the data.  In order to train it, the ".from" is the response that it would receive from a user.  The ".to" is the response that will be used to train the chatbot based on the ".from" response.  
The ".from" and ".to" are essentially text files where each new line / return is a new entry.  Each new line / return has to be lined up with eachother in order to train correctly.  

### Bayes Layer Data


