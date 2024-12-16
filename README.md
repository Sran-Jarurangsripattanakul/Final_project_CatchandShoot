# Project Title

## Project Description
This project is an interactive game built using Python's `turtle` module. It features dynamic gameplay where users control paddles to interact with bouncing balls and aim to shoot a target ball. The game combines physics simulation (e.g., collision detection) with user interactivity to provide an engaging experience.

### Features
- **Dynamic Ball Movement**: Balls move across the screen with adjustable velocity and respond to collisions.
- **Interactive Paddles**: Players can control paddles to redirect balls.
- **Target Shooting Mechanic**: Players can shoot a ball to hit a specific target.
- **Multiple Levels**: The game supports multiple levels with varying difficulty.

---

## How to Install and Run the Project

Follow these steps to set up and run the development environment:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Sran-Jarurangsripattanakul/Final_project_CatchandShoot.git
   cd Final_project_CatchandShoot
   ```

2. **Run the Application**: Run the game using the following command:

   ```bash
   python3 run_ball.py
   ```

---

## Usage

### Sample Interaction
1. The game begins with **Level 1**, where the ball is stationary. The player must initiate gameplay by interacting with the paddle.
2. Players can control paddles and shoot balls at obstacles or targets using predefined keys.
3. **Level Progression**: Players must successfully clear each level by hitting obstacles or targets. The game progresses through **three levels**.
4. **Game Over**: Occurs when the player either runs out of lives or time.

### Expected Outputs
- **Successful Obstacle Hits**: Players hit the designated obstacles or targets to progress through levels.
- **Successful Gameplay**: Players successfully complete all three levels.
- **Game Over**: A message displays if the player runs out of lives or time.

### Demo Video
Provide a link to a demo video of the project: [[Present Video](https://youtu.be/OMLJs1d4bCY?feature=shared)](#)

---

## Project Design and Implementation

### UML Class Diagram
<img width="797" alt="Screenshot 2024-12-16 at 11 30 31 AM" src="https://github.com/user-attachments/assets/c83d98a0-38c8-415b-a8ff-3e9cb07984e8" />


### Class Descriptions
- **Ball**:
  - Represents a ball with properties like size, position, velocity, and color.
  - Handles movement and boundary collision detection.

- **Paddle**:
  - Represents a paddle with adjustable position and dimensions.
  - Allows interaction with balls to influence their movement.

- **CatchAndShootGame**:
  - Manages the main game mechanics, including player controls, lives, and timing.
  - Integrates the paddle, ball, and obstacle interactions.

- **Obstacle**:
  - Represents obstacles that players must hit with the ball to progress through the levels.
  - Includes properties for position, size, and collision detection.

- **Level**:
  - A base class for game levels, including shared setup and gameplay logic.
  
- **Level1 (Level)**:
  - The first level of the game with basic gameplay.

- **Level2 (Level)**:
  - The second level with increased difficulty and more complex obstacle arrangements.

- **Level3 (Level)**:
  - The final level with challenging gameplay and advanced obstacles.

### Baseline Code Modifications
This project extends and integrates baseline code to:
- Simulate event-driven bouncing for balls.
- Enable user interactions like moving paddles and shooting.
- Handle dynamic collision detection with walls, paddles, and obstacles.

### Testing
The project was tested using unit tests and manual gameplay:
- **Unit Tests**: Verified ball movement, collision detection, paddle interactions, and shooting mechanics.
- **Manual Testing**: Ensured smooth gameplay and proper level transitions.

Known Issues:
- There's a bug when the ball hit the side of obstacle and stuck

---

## Sophistication Level
Rate your project on a scale of 80–100, based on the complexity and features.

**Rating**: 90

- **90**: A game involving multiple ball objects colliding with one another and with multiple surfaces oriented at an angle, including a target-shooting mechanic.

