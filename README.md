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
The chatbot will then be available from the public IP address on port 5000.  
To simplify access, you can use a domain that forwards to the IP on port 5000, such as:  
`(Public IP 184.105.5.79)`  
`www.botcssp.com` -> `http://184.105.5.79:5000/`  

## Modifying 
### Neural Net Data
The Neural Net uses a ".from" and ".to" file in order to train the data.  In order to train it, the ".from" is the response that it would receive from a user.  The ".to" is the response that will be used to train the chatbot based on the ".from" response.  
The ".from" and ".to" are essentially text files where each new line / return is a new entry.  Each new line / return has to be lined up with eachother in order to train correctly.  

### Bayes Layer Data
Modify Bayes Layer Data:

- All questions and answers that are fed into the layer are within the QuestionAnswer.txt file,  
	which needs to be in the same directory as the Main1.py file.  The file path to this file must correct  
	in trainAgent() within the Main1.py file.  
-The format is as follows:  
	Question::Answer (the :: delimites the end of the question and begginning of the answer. 
	
To train, do the following:  
    1. Fill the question answer file with data that you want to use.  
	2. Make sure the file is in the same directory as Main1.py.  
	3. Make sure the file paths in Main1.py are correct.  
	4. Run the trainAgent function.    
In order to re-train with new data, the same process is followed, but make sure to
	delete all .p files within the same directory as Main1.py first.  
	

