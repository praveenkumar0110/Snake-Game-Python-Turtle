import turtle
import time
import random

WIDTH, HEIGHT = 600, 600
BG_COLOR = "#1a1a1a"
BORDER_LIMIT = 290
COLLISION_LIMIT = 280

class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(width=WIDTH, height=HEIGHT)
        self.screen.tracer(0)
        self.screen.colormode(255)

        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.paused = False
        self.move_locked = False 
        self.delay = 0.09
        self.segments = []
        self.particles = []

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.color("white")

        self.head = self.create_turtle("circle", (0, 255, 150))
        self.head.direction = "stop"

        self.left_eye = self.create_eye(white=True)
        self.right_eye = self.create_eye(white=True)
        self.left_pupil = self.create_eye(white=False)
        self.right_pupil = self.create_eye(white=False)
        self.blink_timer = 0

        self.food = self.create_turtle("circle", (255, 50, 80))
        self.food.shapesize(0.8, 0.8)
        self.reset_food()

        self.draw_border()
        self.show_start_screen()

        self.screen.listen()
        self.screen.onkey(self.start_game, "Return")
        self.screen.onkey(self.toggle_pause, "space")
        self.screen.onkey(self.go_up, "Up")
        self.screen.onkey(self.go_down, "Down")
        self.screen.onkey(self.go_left, "Left")
        self.screen.onkey(self.go_right, "Right")
        self.screen.onkey(self.go_up, "w")
        self.screen.onkey(self.go_down, "s")
        self.screen.onkey(self.go_left, "a")
        self.screen.onkey(self.go_right, "d")

    def create_turtle(self, shape, color):
        t = turtle.Turtle()
        t.shape(shape)
        t.color(color)
        t.penup()
        t.speed(0)
        return t

    def create_eye(self, white=True):
        t = turtle.Turtle()
        t.shape("circle")
        t.color("white" if white else "black")
        t.penup()
        t.shapesize(0.4 if white else 0.15)
        t.hideturtle()
        return t

    def draw_border(self):
        border = turtle.Turtle()
        border.hideturtle()
        border.speed(0)
        border.color("red")
        border.pensize(3)
        border.penup()
        border.goto(-BORDER_LIMIT, -BORDER_LIMIT)
        border.pendown()
        for _ in range(4):
            border.forward(BORDER_LIMIT * 2)
            border.left(90)

    def show_start_screen(self):
        self.pen.clear()
        self.pen.goto(0, 50)
        self.pen.write("SNAKE GAME 🐍 ", align="center", font=("Verdana", 30, "bold"))
        self.pen.goto(0, 0)
        self.pen.write("Press ENTER to Start", align="center", font=("Arial", 14, "normal"))

    def update_scoreboard(self):
        self.pen.clear()
        self.pen.goto(0, HEIGHT // 2 - 40)
        self.pen.write(f"Score: {self.score}  High Score: {self.high_score}", 
                       align="center", font=("Courier New", 16, "bold"))

    def reset_food(self):
        safe_limit = BORDER_LIMIT - 20
        x = random.randint(-safe_limit, safe_limit)
        y = random.randint(-safe_limit, safe_limit)
        self.food.goto(x, y)

    def get_gradient_color(self, index):
        r = max(0, 0 - (index * 2))
        g = max(50, 255 - (index * 5))
        b = min(255, 150 + (index * 8))
        return (r, g, b)

    def create_particle_explosion(self, x, y):
        for _ in range(8):
            p = turtle.Turtle()
            p.shape("circle")
            p.shapesize(0.2)
            p.color("yellow")
            p.penup()
            p.goto(x, y)
            dx = random.uniform(-5, 5)
            dy = random.uniform(-5, 5)
            self.particles.append({"t": p, "dx": dx, "dy": dy, "life": 12})

    def handle_particles(self):
        for p in self.particles[:]:
            p["t"].goto(p["t"].xcor() + p["dx"], p["t"].ycor() + p["dy"])
            p["life"] -= 1
            if p["life"] <= 0:
                p["t"].hideturtle()
                p["t"].clear()
                self.particles.remove(p)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.head.direction = "up"
            self.score = 0
            self.delay = 0.09
            self.pen.clear()
            self.update_scoreboard()
            for eye in [self.left_eye, self.right_eye, self.left_pupil, self.right_pupil]:
                eye.showturtle()
            self.game_loop()

    def reset_game(self):
        time.sleep(0.5)
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.delay = 0.09
        
        for seg in self.segments:
            seg.goto(1000, 1000)
            seg.hideturtle()
        self.segments.clear()
        
        for eye in [self.left_eye, self.right_eye, self.left_pupil, self.right_pupil]:
            eye.hideturtle()

        self.game_running = False
        self.show_start_screen()
        self.screen.update()

    def move_head(self):
        step = 20
        if self.head.direction == "up": self.head.sety(self.head.ycor() + step)
        elif self.head.direction == "down": self.head.sety(self.head.ycor() - step)
        elif self.head.direction == "left": self.head.setx(self.head.xcor() - step)
        elif self.head.direction == "right": self.head.setx(self.head.xcor() + step)

    def update_eyes(self):
        x, y = self.head.xcor(), self.head.ycor()
        offset = 6
        pupil_offset = 2
        
        self.blink_timer += 1
        if self.blink_timer > 50 and self.blink_timer < 55:
            self.left_eye.shapesize(0.1, 0.4)
            self.right_eye.shapesize(0.1, 0.4)
        else:
            self.left_eye.shapesize(0.4, 0.4)
            self.right_eye.shapesize(0.4, 0.4)
            if self.blink_timer > 55: self.blink_timer = 0

        if self.head.direction == "up":
            self.left_eye.goto(x - offset, y + 5)
            self.right_eye.goto(x + offset, y + 5)
            self.left_pupil.goto(x - offset, y + 5 + pupil_offset)
            self.right_pupil.goto(x + offset, y + 5 + pupil_offset)
        elif self.head.direction == "down":
            self.left_eye.goto(x - offset, y - 5)
            self.right_eye.goto(x + offset, y - 5)
            self.left_pupil.goto(x - offset, y - 5 - pupil_offset)
            self.right_pupil.goto(x + offset, y - 5 - pupil_offset)
        elif self.head.direction == "left":
            self.left_eye.goto(x - 5, y + offset)
            self.right_eye.goto(x - 5, y - offset)
            self.left_pupil.goto(x - 5 - pupil_offset, y + offset)
            self.right_pupil.goto(x - 5 - pupil_offset, y - offset)
        elif self.head.direction == "right":
            self.left_eye.goto(x + 5, y + offset)
            self.right_eye.goto(x + 5, y - offset)
            self.left_pupil.goto(x + 5 + pupil_offset, y + offset)
            self.right_pupil.goto(x + 5 + pupil_offset, y - offset)

    def toggle_pause(self):
        if self.game_running:
            self.paused = not self.paused
            if self.paused:
                self.pen.goto(0, 0)
                self.pen.write("PAUSED", align="center", font=("Arial", 24, "bold"))
            else:
                self.update_scoreboard()

    def go_up(self):
        if self.head.direction != "down" and not self.move_locked:
            self.head.direction = "up"
            self.move_locked = True

    def go_down(self):
        if self.head.direction != "up" and not self.move_locked:
            self.head.direction = "down"
            self.move_locked = True

    def go_left(self):
        if self.head.direction != "right" and not self.move_locked:
            self.head.direction = "left"
            self.move_locked = True

    def go_right(self):
        if self.head.direction != "left" and not self.move_locked:
            self.head.direction = "right"
            self.move_locked = True

    def game_loop(self):
        while self.game_running:
            if self.paused:
                self.screen.update()
                time.sleep(0.1)
                continue

            for i in range(len(self.segments) - 1, 0, -1):
                x = self.segments[i - 1].xcor()
                y = self.segments[i - 1].ycor()
                self.segments[i].goto(x, y)
                self.segments[i].color(self.get_gradient_color(i))

            if len(self.segments) > 0:
                self.segments[0].goto(self.head.xcor(), self.head.ycor())

            self.move_head()
            self.move_locked = False

            if abs(self.head.xcor()) > COLLISION_LIMIT or abs(self.head.ycor()) > COLLISION_LIMIT:
                self.reset_game()
                return

            for seg in self.segments:
                if seg.distance(self.head) < 20:
                    self.reset_game()
                    return

            if self.head.distance(self.food) < 20:
                self.create_particle_explosion(self.food.xcor(), self.food.ycor())
                self.reset_food()
                
                new_seg = self.create_turtle("circle", self.get_gradient_color(len(self.segments)))
                self.segments.append(new_seg)
                
                self.score += 10
                if self.score > self.high_score: self.high_score = self.score
                self.update_scoreboard()

                if self.delay > 0.03:
                    self.delay -= 0.002

            self.update_eyes()
            self.handle_particles()
            
            self.screen.update()
            time.sleep(self.delay)

if __name__ == "__main__":
    game = SnakeGame()
    turtle.done()