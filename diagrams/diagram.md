```mermaid
sequenceDiagram
    participant Unity
    participant Python Script
    Note right of Unity: Start Game
    loop Every frame
    Note right of Unity: Collect data
    Unity ->> Python Script: Send collected data
    Note right of Python Script: Get Action
    Python Script ->> Unity: Send Action
    Note right of Unity: the kart takes the action 
    end
    Note right of Unity: Game Over
```