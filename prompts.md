# Prompts log

This file logs the tool/prompts you used and the results.  A small note on whether it was successful, choices you made and what was used.


## Team-Member1-Joy


|AI tool name|prompt | result | alterations |
|------------|-------|--------|-------------|
|ChatGPT|I'm having an issue with validation code. my debugger keeps saying that Validation Report - invalid_noc: 1 issues found. what would I add code to prevent this|Fix: Skip empty NOC values in validation|No alterations|


## Team-Member2-Batu


|AI tool name|prompt | result | alterations |
|------------|-------|--------|-------------|
|Chatgpt|what is the Python date format code for a 3-letter month abbreviation like "Jul"?|gave me  ```%b```.|No alterations|
|Chatgpt|I have a string that looks like a list, ['a', 'b'] . how do I turn this into an actual python list without writing a manual parser?|suggested to use ast.literal_eval from the standard library.|No alterations|
|Chatgpt|Im looping through a dictionary. if a key is missing, my code crashes. is there a method to return none or a default value instead of raising a KeyError?|suggested to use the ```.get(key, default)``` method.|No alterations|
|Chatpgt|my data has some strings with extra spaces and symbols. what is the standard string function to check if a string contains only digits?|gave me documentation on the ```.isdigit()``` string method.|No alterations|
|Chatgpt|I have strings like "75 kg" and "180 cm" in my data. what is the cleanest and fastest way to use regex to strip the letters and keep only the numeric value?|simple regex pattern ```r"[\d\.]+"```|No alterations|

## Team-Member3-Henry


|AI tool name|prompt | result | alterations |
|------------|-------|--------|-------------|
|ChatGPT|Generate a map of special "accented" characters to normal characters. Include all of the characters that you would think would appear in names. Use the format: characters = {"é": "e"}|The result is included in the file special_character_map.py|No alterations|
|ChatGPT|I'm working in python and I'm trying to get all the permutations of a list without itertools and without repetition. I want to see smaller versions of the permutations too. So I should see [1, 2, 3] and [1, 2]|The result is in utils.py and is commented on for clarity|No alterations|
|ChatGPT|Help me create a format map in Python between two olympic datasets with differing event names. Here are the names of my legacy olympic event names: "names..." Here are the names of my new Paris dataset: "names..." Do a deep review of all the names to ensure that you are correctly assigning each name. DO NOT CHANGE ANY OF THE NAMES WHATSOEVER|The results are in event_map.py|No alterations|

## Team-Member4-Yigit


|AI tool name|prompt | result | alterations |
|------------|-------|--------|-------------|
|ChatGPT|Grammer check and formalize MS1 problem identification|Polished ms1_prob_id.md succesfully|Structured text with correct grammer, detailed explanation of data inconsistencies, and prototype outputs|
