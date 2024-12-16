import turtle
import math


class Ball:
    def __init__(self, size, x, y, vx, vy, color, ball_type=None, check_miss_callback=None):
        self.size = size
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.ball_type = ball_type
        self.mass = 100 * size**2
        self.count = 0
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        self.check_miss_callback = check_miss_callback

    def draw(self):
        # draw a circle of radius equals to size centered at (x, y) and paint it with color
        turtle.penup()
        turtle.color(self.color)
        turtle.fillcolor(self.color)
        turtle.goto(self.x, self.y-self.size)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(self.size)
        turtle.end_fill()

    def bounce_off_vertical_wall(self):
        self.vx = -self.vx
        self.count += 1

    def bounce_off_horizontal_wall(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off(self, that):
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy  # dv dot dr
        dist = self.size + that.size   # distance between particle centers at collison

        # magnitude of normal force
        magnitude = 2 * self.mass * that.mass * \
            dvdr / ((self.mass + that.mass) * dist)

        # normal force, and in x and y directions
        fx = magnitude * dx / dist
        fy = magnitude * dy / dist

        # update velocities according to normal force
        self.vx += fx / self.mass
        self.vy += fy / self.mass
        that.vx -= fx / that.mass
        that.vy -= fy / that.mass

        # update collision counts
        self.count += 1
        that.count += 1

    def distance(self, that):
        x1 = self.x
        y1 = self.y
        x2 = that.x
        y2 = that.y
        d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
        return d

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check for vertical wall collisions and bounce if needed
        if self.x - self.size <= -self.canvas_width or self.x + self.size >= self.canvas_width:
            self.bounce_off_vertical_wall()

        # Check for top wall collision and bounce if needed
        if self.y + self.size >= self.canvas_height:
            self.bounce_off_horizontal_wall()

        # Only bounce the target ball off the bottom, but not the shooter ball
        if self.ball_type == "target":  # Target ball behavior
            if self.y - self.size <= -self.canvas_height:
                self.bounce_off_horizontal_wall()  # Bounce off the bottom for target ball

        elif self.ball_type == "shooter":  # Shooter ball behavior
            if self.y - self.size <= -self.canvas_height:
                if self.check_miss_callback:  # Handle the miss callback for shooter ball
                    self.check_miss_callback()  # Call the miss handler

    def time_to_hit(self, that):
        if self is that:
            return math.inf
        dx = that.x - self.x
        dy = that.y - self.y
        dvx = that.vx - self.vx
        dvy = that.vy - self.vy
        dvdr = dx*dvx + dy*dvy
        if dvdr > 0:
            return math.inf
        dvdv = dvx*dvx + dvy*dvy
        if dvdv == 0:
            return math.inf
        drdr = dx*dx + dy*dy
        sigma = self.size + that.size
        d = (dvdr*dvdr) - dvdv * (drdr - sigma*sigma)
        # if drdr < sigma*sigma:
        # print("overlapping particles")
        if d < 0:
            return math.inf
        t = -(dvdr + math.sqrt(d)) / dvdv

        # should't happen, but seems to be needed for some extreme inputs
        # (floating-point precision when dvdv is close to 0, I think)
        if t <= 0:
            return math.inf

        return t

    def time_to_hit_vertical_wall(self):
        self.update_canvas_dimensions()
        if self.vx > 0:
            return (self.canvas_width - self.x - self.size) / self.vx
        elif self.vx < 0:
            return (-self.canvas_width - self.x + self.size) / abs(self.vx)
        else:
            return math.inf

    def time_to_hit_horizontal_wall(self):
        self.update_canvas_dimensions()
        if self.vy > 0:
            return (self.canvas_height - self.y - self.size) / self.vy
        elif self.vy < 0:
            return (-self.canvas_height - self.y + self.size) / abs(self.vy)
        else:
            return math.inf

    def time_to_hit_paddle(self, paddle):
        if self.vy == 0:  # Prevent division by zero
            return float('inf')

        # Calculate time for vertical alignment with the paddle
        dt = (paddle.location[1] - self.y - self.size -
              paddle.height / 2) / abs(self.vy)

        # Check if the ball's horizontal position will be within the paddle's width
        paddle_left_edge = paddle.location[0] - paddle.width / 2
        paddle_right_edge = paddle.location[0] + paddle.width / 2
        future_x = self.x + self.vx * dt

        if paddle_left_edge - self.size <= future_x <= paddle_right_edge + self.size and dt >= 0:
            return dt

        return float('inf')

    def bounce_off_paddle(self):
        self.vy = -self.vy
        self.count += 1

    def bounce_off_wall(self):
        self.vy = -self.vy
        self.count += 1

    def update_canvas_dimensions(self):
        screen = turtle.Screen()
        self.canvas_width = screen.window_width() // 2
        self.canvas_height = screen.window_height() // 2

    def check_collision_with_obstacle(self, obstacle):
        # Check if the ball's bounding box overlaps with the obstacle's bounding box
        ball_left = self.x - self.size
        ball_right = self.x + self.size
        ball_top = self.y + self.size
        ball_bottom = self.y - self.size

        obstacle_left = obstacle.x - obstacle.width / 2
        obstacle_right = obstacle.x + obstacle.width / 2
        obstacle_top = obstacle.y + obstacle.height / 2
        obstacle_bottom = obstacle.y - obstacle.height / 2

        # Check for collision
        if (ball_right > obstacle_left and
                ball_left < obstacle_right and
                ball_top > obstacle_bottom and
                ball_bottom < obstacle_top):
            # Handle the collision: reverse ball's velocity
            self.vx = -self.vx
            self.vy = -self.vy
            return True  # Collision occurred

        return False  # No collision

    def __str__(self):
        return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)
