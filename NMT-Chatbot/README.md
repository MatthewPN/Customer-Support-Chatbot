nmt-chatbot
===================

Major Contributions to David Kukiela who created the NMT chatbot implementation which we were able to use to come to our end results.  
Source: https://github.com/daniel-kukiela/nmt-chatbot

Table of Contents
-------------
2. [Setup](#setup)
3. [Custom summary values (evaluation)](#custom-summary-values-evaluation)
4. [Standard vs BPE/WPM-like (subword) tokenization, embedded detokenizer](#standard-vs-bpewpm-like-subword-tokenization-embedded-detokenizer)
5. [Rules files](#rules-files)
6. [Tests](#tests)
7. [More detailed information about training a model](#more-detailed-information-about-training-a-model)
8. [Utils](#utils)
9. [Inference](#inference)
10. [Importing nmt-chatbot](#importing-nmt-chatbot)
11. [Deploying chatbot/model](#deploying-chatbotmodel)
12. [Demo chatbot](#demo-chatbot)
13. [Changelog](#changelog)


Setup
-------------

Steps to setup project for your needs:
It is *highly* recommended that you use Python 3.6.

 1. ```$ git clone --recursive https://github.com/MatthewPN/Customer-Support-Chatbot.git```  
 2. ```$ cd Customer-nmt-chatbot```
 3. ```$ pip install -r requirements.txt``` TensorFlow-GPU is one of the requirements. You also need CUDA Toolkit 8.0 and cuDNN 6.1. (Windows tutorial: https://www.youtube.com/watch?v=r7-WPbx8VuY  Linux tutorial: https://pythonprogramming.net/how-to-cuda-gpu-tensorflow-deep-learning-tutorial/)
 4. ```$ cd setup```
 5. (optional) edit settings.py to your liking. These are a decent starting point for ~4GB of VRAM, you should first start by trying to raise vocab if you can. 
 6. (optional) Edit text files containing rules in the setup directory.
 7. Place training data inside "new_data" folder (train.(from|to), tst2013.(from|to), tst2013(from|to)). We have placed 160,000 interactions between customers and costomer support representatives at this location which is what generates our general customer support AI.
 8. ```$ python prepare_data.py``` ...Run setup/prepare_data.py - a new folder called "data" will be created with prepared training data
 9. ```$ cd ../```
 10. ```$ python train.py``` Begin training.  NOTE: This can take multiple days, and it will depend a lot on the hardware that is used.

Version 0.3 introduces epoch-based training including custom (epoch-based as well) decaying scheme - refer to `preprocessing['epochs']` in `setup/settings.py` for more detailed explanation and example (enabled by default).


Rules files
-------------

Setup folder contains multiple "rules" files (All of them are regex-based:

 - answers_detokenize.txt - detokenization rules (removes unnecessary spaces, legacy tokenizer only).
 - answers_replace - synonyms, replaces phrase or it's part with a replacement.
 - answers_subsentence_score.txt - rules for answer score (list of subsentences and score modifiers that can either lower or raise score when includes certain subsentences).
 - protected_phrases_standard.txt - ensures that matching phrases will remain untouched when building vocab file with standard tokenizer.
 - protected_phrases_bpe.txt - same as above but for BPE/WPM-like tokenizer.


Tests
-------------

Every rules file has related test script. Those test scripts might be treated as some kind of unit testing. Every modification of rules files might be checked against those tests but every modification should be also followed by new test cases in those scripts.

It's important to check everything before training new model. Even slight change might break something.

Test scripts will display check status, checked sentence and eventually check result (if different than assumed).


More detailed information about training a model
-------------

setup/settings.py consist of multiple settings:

 - untouched file/folder paths should fit for most cases
 - "preprocessing" dictionary should be easy to understand
 - "hparams" dictionary will be passed to NMT like command line options with standard usage
 - "score" dictionary with settings for answer scoring

setup/prepare_data.py:

 - walks thru files placed in "new_data" folder - train.(from|to), tst2012.(from|to)m tst2013(from|to)
 - tokenizes all sentences (based on settings and internal rules)
 - for "train" files - builds vocabulary files, makes them unique and saves up to the number of entities set in setup/settings.py file, unused vocab entities (if any - depends on settings) will be saved to separate files

train.py - starts training process



Inference
-------------

Whenever a model is trained, `inference.py`, when directly called, allows to "talk to" AI in interactive mode. It will start and setup everything needed to use trained model (using saved hparams file within the model folder and setup/settings.py for the rest of settings or lack of hparams file).

For every question will be printed up to a number of responses set in setup/settings.py. Every response will be marked with one of three colors:

 - green - first one with that color is a candidate to be returned. Answers to the color passed blacklist check (setup/response_blacklist.txt)
 - orange - still proper responses, but with lower than maximum score
 - red - improper response - below threshold

Steps from the question to the answers:

 1. Pass question
 2. Compute up to number of responses set in setup/settings.py
 3. Detokenize answers using either embedded detokenizer or rules from setup/answers_detokenized.txt (depending on settings)
 3. Replace responses or their parts using additional rules
 4. Score responses
 5. Return (show with interactive mode) responses

It is also possible to process a batch of the questions by simply using command redirection:

    python inference.py < input_file

or:

    python inference.py < input_file > output_file

It is possible to pass specified checkpoint as a parameter to use inference using that checkpoint, for example:

    python inference.py translate.ckpt-1000



Importing nmt-chatbot
-------------

The project allows being imported for the needs of inference. Simply embed folder within your project and import (notice: change folder name in a way it will not include dash (`-`) character - you can't import module with that character in it's name), then use:

    from nmt_chatbot.inference import inference

    print(inference("Hello!"))

(where `nmt_chatbot` is a directory name of chatbot module)

inference() takes one parameter:

 - `question` (required)

For a single question, function will return dictionary containing:

 - answers - list of all answers
 - scores - list of scores for answers
 - best_index - index of best answer
 - best_score - score of best answer

Score:

Every response starts with `score['starting_score']` value from `setup/settings.py` (10 by default) and is further modified by various checks. Please refer to `score` section of `setup/settings.py` for more details and settings. Final score is next used to pick "best" response.

With a list of questions, the function will return a list of dictionaries.

For every empty question, the function will return `None` instead of result dictionary.
