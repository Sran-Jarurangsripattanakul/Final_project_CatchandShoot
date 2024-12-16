import ball
import paddle
import turtle
import random


class Level:
    def __init__(self, game):
        self.game = game

    def configure_target(self, target):
        raise NotImplementedError("Subclasses must implement this method")

    def update(self, dt):
        self.game.shooter.move(dt)  # Move the shooter (ball)
        self.game._redraw()  # Redraw everything
        self.game.target.move(dt)  # Move the target
        self.game._check_wall_collision()  # Check for collisions with walls
        self.game._check_collision()  # Check for collisions between shooter and target
        self.game._check_miss()  # Check if the ball missed
        self.game._paddle_collision()  # Check for collisions with paddle

        # Check for obstacle collisions with the shooter (ball)
        for obstacle in self.game.obstacles:
            if self.game.shooter.check_collision_with_obstacle(obstacle):
                print("Ball collided with obstacle!")


class Level1(Level):
    def configure_target(self, target):
        target.size = 0.05 * self.game.canvas_width  # Set a default size for the target
        target.x = random.randint(-self.game.canvas_width //
                                  2, self.game.canvas_width // 2)
        target.y = random.randint(0, self.game.canvas_height // 2)
        print(f"Level 1 target configured: size={target.size}, x={target.x}, y={target.y}")

    def update(self, dt):
        super().update(dt)


class Level2(Level):
    def configure_target(self, target):
        print("Configuring target for Level 2")
        target.vx = random.uniform(-50, 50)
        target.vy = random.uniform(-50, 50)
        target.size = 0.025 * self.game.canvas_width
        target.x = random.randint(-self.game.canvas_width //
                                  2, self.game.canvas_width // 2)
        target.y = random.randint(0, self.game.canvas_height // 2)
        print(f"Target size set to: {target.size}")

    def update(self, dt):
        super().update(dt)


class Level3(Level):
    def configure_target(self, target):
        target.vx = random.uniform(-100, 100)
        target.vy = random.uniform(-100, 100)
        target.size = 0.015 * self.game.canvas_width
        target.x = random.randint(-self.game.canvas_width //
                                  2, self.game.canvas_width // 2)
        target.y = random.randint(0, self.game.canvas_height // 2)

    def update(self, dt):
        if random.random() < 0.05:  # 5% chance per update cycle to change direction
            self.game.target.vx = random.uniform(-50, 50)
            self.game.target.vy = random.uniform(-50, 50)
        super().update(dt)


class Obstacle:
    def __init__(self, width, height, x, y, vx, vy, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        turtle.penup()
        turtle.goto(self.x - self.width / 2, self.y -
                    self.height / 2)  # Bottom-left corner
        turtle.pendown()
        turtle.color(self.color)
        turtle.begin_fill()
        for _ in range(2):
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height)
            turtle.left(90)
        turtle.end_fill()

    def check_collision(self, ball):
        # Check for collision with a ball
        return (
            abs(ball.x - self.x) <= (self.width / 2 + ball.size) and
            abs(ball.y - self.y) <= (self.height / 2 + ball.size)
        )


class CatchAndShootGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.HZ = 60
        self.lives = 3
        self.score = 0
        self.shooter_ready = True
        self.level_score = 0
        self.level_score_threshold = 5  # Initial score threshold for Level 1
        self.current_level = Level1(self)  # Set initial level

        # Define canvas dimensions
        self.canvas_width = self.screen.window_width()
        self.canvas_height = self.screen.window_height()

        self.obstacles = []  # List of obstacles
        self.initialize_obstacles()

        # Add a level timer
        self.level_timer = 30

        turtle.speed(0)
        turtle.tracer(0, 0)
        turtle.hideturtle()
        turtle.colormode(255)

        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]

        self.initialize_paddle()
        self.initialize_balls()

    def initialize_obstacles(self):
        if isinstance(self.current_level, Level2) or isinstance(self.current_level, Level3):
            # Add obstacles for Level 2 and Level 3
            for _ in range(3):  # Add three obstacles
                width = 50
                height = 20
                x = random.randint(-self.canvas_width // 2 +
                                   width, self.canvas_width // 2 - width)
                y = random.randint(-self.canvas_height // 2 +
                                   height, self.canvas_height // 2 - height)
                vx = random.choice([-50, 50])
                vy = random.choice([-30, 30])
                color = (0, 0, 255)
                self.obstacles.append(
                    Obstacle(width, height, x, y, vx, vy, color))

    def initialize_paddle(self):
        tom = turtle.Turtle()
        self.my_paddle = paddle.Paddle(100, 25, (255, 0, 0), tom)
        self.my_paddle.set_location([0, -self.canvas_height + 60])

    def initialize_balls(self):
        ball_radius = 0.025 * self.canvas_width
        self.shooter = ball.Ball(
            ball_radius, self.my_paddle.location[0], self.my_paddle.location[1] + self.my_paddle.height, 0, 0, (255, 0, 0), ball_type="shooter")
        self.target = ball.Ball(ball_radius, 0, 0, 0, 0,
                                (0, 255, 0), ball_type="target")

        # Ensure shooter is ready at game start
        self.shooter_ready = True

        # Configure target based on the current level
        if isinstance(self.current_level, Level1):
            self.current_level.configure_target(self.target)
        elif isinstance(self.current_level, Level2):
            self.current_level.configure_target(self.target)
        elif isinstance(self.current_level, Level3):
            self.current_level.configure_target(self.target)

    def _draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for _ in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)

    def _redraw(self):
        turtle.clear()
        self.my_paddle.clear()
        self._draw_border()
        self.my_paddle.draw()
        self.shooter.draw()
        self.target.draw()

        for obstacle in self.obstacles:
            obstacle.draw()

        # Display lives and score
        turtle.penup()
        # Position for score
        turtle.goto(-self.canvas_width + 45, self.canvas_height - 30)
        turtle.color("black")
        turtle.write(f"Lives: {self.lives}  Score: {self.level_score}", font=("Arial", 16, "bold"))

        # Display time remaining for the current level
        turtle.goto(-self.canvas_width + 45,
                    self.canvas_height - 60)  # Position for time
        turtle.color("black")
        turtle.write(f"Time: {int(self.level_timer)}s",
                     font=("Arial", 16, "bold"))

        # Display bonus time if level_timer > 30
        if self.level_timer > 30:
            # Position for bonus
            turtle.goto(-self.canvas_width + 45, self.canvas_height - 90)
            turtle.write(f"Bonus Time: {int(self.level_timer - 30)}s", font=("Arial", 16, "bold"))

        turtle.update()

    def _update_timer(self, dt):
        self.level_timer -= dt
        if self.level_timer <= 0:
            print("Time's up!")
            self.lives -= 1
            if self.lives <= 0:
                print("Game Over")
                turtle.bye()
            else:
                self.reset_level()

    def next_level(self):
        print(f"Transitioning from {type(self.current_level).__name__}")

        # Preserve remaining time and add to the next level
        remaining_time = self.level_timer

        if isinstance(self.current_level, Level1):
            self.current_level = Level2(self)
            self.level_score_threshold = 5  # Set new threshold for Level 2
        elif isinstance(self.current_level, Level2):
            self.current_level = Level3(self)
            self.level_score_threshold = 5  # Set new threshold for Level 3
        elif isinstance(self.current_level, Level3):
            print("Congratulations! You finished all levels!")
            turtle.bye()  # End the game
            return

        self.level_score = 0

        self.current_level.configure_target(self.target)
        print(f"Transitioned to {type(self.current_level).__name__}.")
        print(f"Target size: {self.target.size}, Next threshold: {self.level_score_threshold}")

        self.level_timer = remaining_time + 30

        self.initialize_obstacles()

    def reset_level(self):
        self.level_score = 0
        self.shooter_ready = True
        self.shooter.x = self.my_paddle.location[0]
        self.shooter.y = self.my_paddle.location[1] + self.my_paddle.height
        self.shooter.vx = 0
        self.shooter.vy = 0
        self.current_level.configure_target(self.target)

    def _check_miss(self):
        if self.shooter.y < -self.canvas_height:  # Check if the ball is below the screen
            self.lives -= 1  # Deduct a life

            if self.lives <= 0:
                print("Game Over")
                turtle.bye()  # End the game
            else:
                # Reset the shooter (ball) to the paddle position
                self.shooter_ready = True
                self.shooter.x = self.my_paddle.location[0]
                self.shooter.y = self.my_paddle.location[1] + \
                    self.my_paddle.height
                self.shooter.vx = 0
                self.shooter.vy = 0

    def _check_collision(self):
        if self.shooter.distance(self.target) <= self.shooter.size + self.target.size:
            self.level_score += 1  # Increase level score, not the global score

            # Respawn the target at a random position
            self.target.x = random.randint(-self.canvas_width //
                                           2, self.canvas_width // 2)
            self.target.y = random.randint(0, self.canvas_height // 2)

            # Update target velocity only for Level 2 and Level 3
            if isinstance(self.current_level, (Level2, Level3)):
                min_speed = 10  # Minimum speed for target
                previous_vx, previous_vy = self.target.vx, self.target.vy
                while True:
                    self.target.vx = random.uniform(-50, 50)
                    self.target.vy = random.uniform(-50, 50)

                    # Enforce minimum speed constraint
                    if abs(self.target.vx) < min_speed:
                        self.target.vx = min_speed if self.target.vx >= 0 else -min_speed
                    if abs(self.target.vy) < min_speed:
                        self.target.vy = min_speed if self.target.vy >= 0 else -min_speed

                    # Ensure the new velocity is not the same as the previous one
                    if (self.target.vx, self.target.vy) != (previous_vx, previous_vy):
                        break
                print(f"New target velocity: vx={self.target.vx}, vy={self.target.vy}")
            else:  # For Level 1, ensure the target is stationary
                self.target.vx = 0
                self.target.vy = 0

            # Reset shooter to paddle after successful hit
            self.shooter_ready = True
            self.shooter.x = self.my_paddle.location[0]
            self.shooter.y = self.my_paddle.location[1] + self.my_paddle.height
            self.shooter.vx = 0
            self.shooter.vy = 0

            # Check for level score threshold
            if self.level_score >= self.level_score_threshold:
                print(f"Level score reached {self.level_score}, moving to the next level!")
                self.next_level()

    def _paddle_collision(self):
        if (
            not self.shooter_ready and
            self.my_paddle.location[1] <= self.shooter.y <= self.my_paddle.location[1] +
                self.my_paddle.height
            and abs(self.shooter.x - self.my_paddle.location[0]) <= self.my_paddle.width / 2
        ):
            self.shooter_ready = True
            self.shooter.vx = 0
            self.shooter.vy = 0
            self.shooter.x = self.my_paddle.location[0]
            self.shooter.y = self.my_paddle.location[1] + self.my_paddle.height

    def _check_wall_collision(self):
        window_width = self.canvas_width // 2
        window_height = self.canvas_height // 2

        # Check if shooter hits left or right vertical walls
        if self.shooter.x - self.shooter.size <= -window_width or self.shooter.x + self.shooter.size >= window_width:
            self.shooter.vx = -self.shooter.vx

        # Check if shooter hits the top wall (bounces back)
        if self.shooter.y + self.shooter.size >= window_height:
            self.shooter.vy = -self.shooter.vy  # Bounces back on top wall

        # **Do NOT bounce off bottom**. Instead, we handle the miss in another method.
        if self.shooter.y - self.shooter.size <= -window_height:  # Shooter has fallen below the screen
            self._check_miss()

        # Check for target collisions with walls (for target object)
        if self.target.x - self.target.size <= -window_width or self.target.x + self.target.size >= window_width:
            self.target.vx = -self.target.vx

        if self.target.y - self.target.size <= -window_height or self.target.y + self.target.size >= window_height:
            self.target.vy = -self.target.vy

    def _check_obstacle_collision(self):
        for obstacle in self.obstacles:
            obstacle.move(1.0 / self.HZ)
            # Check for collision with the shooter
            if obstacle.check_collision(self.shooter):
                # Reverse shooter's direction if it hits an obstacle
                self.shooter.vx = -self.shooter.vx
                self.shooter.vy = -self.shooter.vy

            # Check for collision with the target
            if obstacle.check_collision(self.target):
                # Reverse target's direction if it hits an obstacle
                self.target.vx = -self.target.vx
                self.target.vy = -self.target.vy

            # Handle obstacle bouncing off walls
            if obstacle.x - obstacle.width / 2 <= -self.canvas_width or obstacle.x + obstacle.width / 2 >= self.canvas_width:
                obstacle.vx = -obstacle.vx

            # Handle obstacle bouncing off the top or bottom wall
            if obstacle.y - obstacle.height / 2 <= -self.canvas_height or obstacle.y + obstacle.height / 2 >= self.canvas_height:
                obstacle.vy = -obstacle.vy

    def move_left(self):
        if (self.my_paddle.location[0] - self.my_paddle.width / 2 - 20) >= -self.canvas_width:
            self.my_paddle.set_location(
                [self.my_paddle.location[0] - 20, self.my_paddle.location[1]])
            if self.shooter_ready:
                self.shooter.x = self.my_paddle.location[0]
                self.shooter.y = self.my_paddle.location[1] + \
                    self.my_paddle.height

    def move_right(self):
        if (self.my_paddle.location[0] + self.my_paddle.width / 2 + 20) <= self.canvas_width:
            self.my_paddle.set_location(
                [self.my_paddle.location[0] + 20, self.my_paddle.location[1]])
            if self.shooter_ready:
                self.shooter.x = self.my_paddle.location[0]
                self.shooter.y = self.my_paddle.location[1] + \
                    self.my_paddle.height

    def check_game_over(self):
        if self.lives <= 0:
            print("Game Over")
            turtle.bye()

    def shoot(self):
        if self.shooter_ready:

            self.shooter_ready = False

            # Position the ball slightly above the paddle before shooting
            self.shooter.y = self.my_paddle.location[
                1] + self.my_paddle.height + self.shooter.size  # Position it above the paddle

            # Set the velocity to move the ball upwards
            self.shooter.vy = 500
            self.shooter.vx = 0

    def run(self):
        self.screen.listen()
        self.screen.onkey(self.move_left, "Left")
        self.screen.onkey(self.move_right, "Right")
        self.screen.onkey(self.shoot, "space")

        try:
            while True:
                self._check_collision()  # Check ball collisions with other objects
                self._check_wall_collision()  # Check ball-wall collisions
                self._check_obstacle_collision()  # Check for ball-obstacle collisions

                # Loop through all obstacles to check if the ball hits them
                for obstacle in self.obstacles:
                    # Corrected here
                    if self.shooter.check_collision_with_obstacle(obstacle):
                        print("Ball collided with obstacle!")

                self._update_timer(1.0 / self.HZ)
                self.current_level.update(dt=1.0 / self.HZ)
                turtle.update()
                self.check_game_over()
        except turtle.Terminator:
            pass


# Run the game
game = CatchAndShootGame()
game.run()
