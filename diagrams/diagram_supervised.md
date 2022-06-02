```mermaid
sequenceDiagram
participant Unity
    participant FlaskAPI
    Note right of Unity: POST endpoint
    loop every frame
        Unity->>FlaskAPI: get input from kart
        FlaskAPI->>FlaskAPI: take a decision
        FlaskAPI->>Unity: send commands to kart
    end
```