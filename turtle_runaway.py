
import turtle, random, time

def distance(x1, y1, x2, y2): #squared
    res = (x1 - x2)**2 + (y1 - y2)**2
    return (int)(res)

class RunawayGame:
    def __init__(self, canvas, runner, chaser, runner_mom, catch_radius=20, init_dist=600, mom_range=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.runner_mom = runner_mom
        self.catch_radius2 = catch_radius**2
        self.mom_range2 = mom_range**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()
        self.runner.setx(-init_dist / 2)

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        self.chaser.setx(+init_dist / 2)
        self.chaser.setheading(180)

        self.runner_mom.shape('turtle')
        self.runner_mom.color('yellow')
        self.runner_mom.penup()
        self.runner_mom.setx(0)

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_caught(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def mom_found(self):
        p = self.runner_mom.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.mom_range2 

    #----score calculation function--------
    def get_score(self):
        max_score = 100
        penalty = (int)(time.time() - self.start_time)
        return max_score - penalty

    def start(self, ai_timer_msec=50):
        self.ai_timer_msec = ai_timer_msec
        self.start_time = time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser)
        #the runner's mom always tries to get closer to her son
        self.runner_mom.mom_move(self.runner)
        self.chaser.auto_chase(self.runner, self.runner_mom)
        #self.chaser.run_ai()
        

        # TODO: You can do something here.
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        elapse = time.time() - self.start_time
        
        if self.mom_found():
            self.drawer.write("The runner's mom got you, 0 points!")
        #time up
        elif elapse > 100:
            self.drawer.write(f"Time is up, you get 0 point!")
        #when the chaser caught the runner!
        elif self.is_caught():
            self.drawer.write(f"The poor blue turtle is catched, you get {self.get_score()} points!")
        else:
            self.drawer.write(f'Is catched? {self.is_caught()} / Elapse: {elapse:.0f} / Current Score: {self.get_score()}')
            self.canvas.ontimer(self.step, self.ai_timer_msec)


class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self):
        pass

    def auto_chase(self, son, mom):
        self.son = son
        self.mom = mom
        x_best = self.pos()[0]
        y_best = self.pos()[1]
        best_dist = 10000000
        x_tmp = x_best
        y_tmp = y_best
        for i in [-10, 0, 10]:
            for j in [-10, 0, 10]:
                x = self.pos()[0] + i
                y = self.pos()[1] + j
                ok = True
                if distance(x, y, self.son.pos()[0], self.son.pos()[1]) > best_dist:
                    ok = False
                if distance(x, y, self.mom.pos()[0], self.mom.pos()[1]) <= 50**2:
                    ok = False
                elif abs(x) < 465 and abs(y) < 395:
                    x_tmp = x
                    y_tmp = y
                if abs(x) > 465 or abs(y) > 395:
                    ok = False
                if ok:
                    best_dist = distance(x, y, self.son.pos()[0], self.son.pos()[1])
                    x_best = x
                    y_best = y

        if x_best != self.pos()[0] or y_best != self.pos()[1]:
            self.goto(x_best, y_best)
        else:
            self.goto(x_tmp, y_tmp)


class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opponent):
        mode = random.randint(0, 1)
        if mode == 0:
            self.left(self.step_turn)
            self.forward(self.step_move)
        elif mode == 1:
            self.right(self.step_turn)
            self.forward(self.step_move)

        self.exceeded_margin_check()

    def mom_move(self, son):
        self.son = son
        x_mom = self.pos()[0]
        y_mom = self.pos()[1]
        x_runner = self.son.pos()[0]
        y_runner = self.son.pos()[1]
        if abs(x_mom - x_runner) < 50 and abs(y_mom - y_runner) < 50:
            mode = random.randint(0, 1)
            if mode == 0:
                self.left(self.step_turn)
                self.forward(self.step_move)
            elif mode == 1:
                self.right(self.step_turn)
                self.forward(self.step_move)

            self.exceeded_margin_check()
            return
        if x_mom < x_runner + 50:
            x_mom += 10
        else:
            x_mom -= 10
        if y_mom < y_runner + 50:
            y_mom += 10
        else:
            y_mom -= 10
        self.goto(x_mom, y_mom)
        self.exceeded_margin_check()


    def exceeded_margin_check(self):
        x = self.pos()[0]
        y = self.pos()[1]
        if abs(x) > 465:
            if x > 0:
                x = min(x, 465)
            else:
                x = max(x, -465)
        if abs(y) > 395:
            if y > 0:
                y = min(y, 395)
            else:
                y = max(y, -395)
        self.goto(x, y)


if __name__ == '__main__':
    canvas = turtle.Screen()
    canvas.bgcolor("SteelBlue3")
    canvas.title("Turtle Runaway")
    runner = RandomMover(canvas)
    chaser = ManualMover(canvas)
    runner_mom = RandomMover(canvas)

    game = RunawayGame(canvas, runner, chaser, runner_mom)
    game.start()
    canvas.mainloop()