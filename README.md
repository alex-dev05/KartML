KartML is a dissertation project that proposes to conduct two experiments aimed at teaching an agent how to learn using machine learning algorithms. 
The agent takes the form of a kart that is trained in a Nascar-like circuit, its goal being to pass through the three checkpoints.
![image](https://user-images.githubusercontent.com/37021205/174646885-17b5a966-8408-412d-9ff0-c4380608d2bd.png)

Generic Data Flow
![image](https://user-images.githubusercontent.com/37021205/174646845-9cc6cdb2-4afd-40af-b0e9-51d713d528d4.png)


Collecting Data

To begin with, the game was run in the normal way, the kart being controlled by a human user. The data collected from the Unity environment was saved in a csv file. For each game session such a file is created (see Exports folder). The exported files have been merged into a larger file.

![image](https://user-images.githubusercontent.com/37021205/174646862-58f18bb1-82ca-4aa8-8291-7555faef42de.png)


ML Classification algorithm

This file was cleaned in python and a classification algorithm was used on it, which returns a value from 0 to 15. This value represents the possible combinations that the kart can have as input: val = 0 -> up arrow = pressed, down arrow = pressed, left arrow = pressed, rigth arrow = pressed val = 1 -> up arrow = pressed, down arrow = pressed, left arrow = pressed, rigth arrow = not pressed .... val = 15 -> up arrow = not pressed, down arrow = not pressed, left arrow = not pressed, rigth arrow = not pressed

Data flow for machine learning supervised algorithm
![image](https://user-images.githubusercontent.com/37021205/174646976-24528417-3df7-4350-b59c-71e142752b8f.png)


Flask API + Modify Unity to be controlled by code

When the game starts in supervised ML mode, at each frame when the update function is executed, a call is made to the Python function via the FLask API via a post request, which contains the data collected from the unity environment, and returns as response the value pa the agent will take. That value is interpreted and a command is given to unity via Vertical and Horizontal.

Vertical takes values between -1 and 1. -1 -> down arrow pressed 0 -> down arrow/up arrow not pressed 1 - up arrow pressed

Horizontal takes values between -1 and 1. -1 -> left arrow pressed 0 -> left arrow/right arrow unpressed 1 - right arrrow pressed

Reinforcement Learning


Reinforcement Learning Flow
![image](https://user-images.githubusercontent.com/37021205/174646797-97ff953e-a721-4d10-908d-4ffbe87fba50.png)


For the reinforcement learning part we used the OpenAI Gym toolkit. 
It requires a directory structure as below:
![image](https://user-images.githubusercontent.com/37021205/174646992-eff65824-097a-4c0a-9bbc-70b6d7307542.png)

For learning, at each frame the agent makes a decision, which is then evaluated by a gain function that penalizes or rewards the agent. This concept is based on a cycle of several consecutive episodes in which the agent learns.

Data flow for reinforcement learnig
