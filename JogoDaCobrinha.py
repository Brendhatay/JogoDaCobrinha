from tkinter import *
from tkinter.font import Font
import random
from tkinter.messagebox import showinfo

width = 800
heigh = 600
grid_size = 20
obstacle_size = 40  # Tamanho dos obstáculos
speed = 30  # Velocidade da cobra

class Square:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velx = 0
        self.vely = 0
    
    def setVel(self, newx, newy):
        self.velx = newx
        self.vely = newy
            
    def pos(self):
        return (self.x, self.y, self.x + grid_size, self.y + grid_size)
    
    def update(self):
        self.x = (self.x + self.velx) % width
        self.y = (self.y + self.vely) % heigh

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'gray'
    
    def pos(self):
        return (self.x, self.y, self.x + obstacle_size, self.y + obstacle_size)
    
    def get_bounds(self):
        return (self.x, self.y, self.x + obstacle_size, self.y + obstacle_size)

class Game:
    def __init__(self, snake_color):
        self.window = Tk()
        self.window.title("Jogo da Cobra")
        self.canvas = Canvas(self.window, bg='black', width=width, height=heigh)
        self.canvas.pack()
        
        # Inicializa a cobra
        self.snake_color = snake_color
        self.snake_colors = [snake_color, 'white']  # Alterna entre a cor selecionada e branco
        self.snake = [
            Square(20, 20, self.snake_colors[0]),
            Square(20 - grid_size, 20, self.snake_colors[1]),
            Square(20 - 2 * grid_size, 20, self.snake_colors[0]),
            Square(20 - 3 * grid_size, 20, self.snake_colors[1])
        ]
        self.food = Square(random.randint(0, (width - grid_size) // grid_size) * grid_size, 
                           random.randint(0, (heigh - grid_size) // grid_size) * grid_size, 'red')
        self.vel = [20, 0]
        self.obstacles = self.create_obstacles(10)
        self.score = 0  # Inicializa a pontuação
        
        self.window.bind("<Up>", self.moveUp)
        self.window.bind("<Down>", self.moveDown)
        self.window.bind("<Right>", self.moveRight)
        self.window.bind("<Left>", self.moveLeft)
        
    def create_obstacles(self, num_obstacles):
        obstacles = []
        for _ in range(num_obstacles):
            x = random.randint(0, (width - obstacle_size) // grid_size) * grid_size
            y = random.randint(0, (heigh - obstacle_size) // grid_size) * grid_size
            # Certifique-se de que os obstáculos não aparecem no início do jogo na frente da cobra
            while any(self.intersect((x, y, x + obstacle_size, y + obstacle_size), s.pos()) for s in self.snake):
                x = random.randint(0, (width - obstacle_size) // grid_size) * grid_size
                y = random.randint(0, (heigh - obstacle_size) // grid_size) * grid_size
            obstacles.append(Obstacle(x, y))
        return obstacles

    def moveUp(self, event):
        if self.vel != [0, 20]:
            self.vel = [0, -20]
    def moveDown(self, event):
        if self.vel != [0, -20]:
            self.vel = [0, 20]
    def moveRight(self, event):
        if self.vel != [-20, 0]:
            self.vel = [20, 0]
    def moveLeft(self, event):
        if self.vel != [20, 0]:
            self.vel = [-20, 0]
    
    def checkCollisionWithObstacles(self):
        snake_head_bounds = self.snake[0].pos()
        for obstacle in self.obstacles:
            if self.intersect(snake_head_bounds, obstacle.pos()):
                return True
        return False

    def intersect(self, rect1, rect2):
        x1_min, y1_min, x1_max, y1_max = rect1
        x2_min, y2_min, x2_max, y2_max = rect2
        return not (x1_max <= x2_min or x1_min >= x2_max or y1_max <= y2_min or y1_min >= y2_max)

    def get_snake_segment_color(self, index):
        return self.snake_colors[index % len(self.snake_colors)]

    def run(self):
        while True:
            self.canvas.delete('all')
            
            # Redesenha o fundo com um padrão de gradiente
            for i in range(0, width, grid_size):
                for j in range(0, heigh, grid_size):
                    self.canvas.create_rectangle(i, j, i + grid_size, j + grid_size, fill='darkgreen', outline='darkgreen')

            # Atualiza a posição da cobra
            head_velx, head_vely = self.vel
            new_head_x = (self.snake[0].x + head_velx) % width
            new_head_y = (self.snake[0].y + head_vely) % heigh

            # Move a cobra
            for i in range(len(self.snake) - 1, 0, -1):
                self.snake[i].x = self.snake[i-1].x
                self.snake[i].y = self.snake[i-1].y
            self.snake[0].x = new_head_x
            self.snake[0].y = new_head_y

            # Verifica se a cobra comeu a comida
            if self.snake[0].pos() == self.food.pos():
                self.food.x = random.randint(0, (width - grid_size) // grid_size) * grid_size
                self.food.y = random.randint(0, (heigh - grid_size) // grid_size) * grid_size
                last_segment = self.snake[-1]
                new_color = self.snake_colors[0] if last_segment.color == self.snake_colors[1] else self.snake_colors[1]
                self.snake.append(Square(last_segment.x, last_segment.y, new_color))
                # Atualiza a lista de cores para garantir alternância correta
                self.snake_colors = [new_color, 'white'] if new_color == self.snake_color else [self.snake_color, 'white']
                # Atualiza a pontuação
                self.score += 10
                # Move obstáculos para novas posições, evitando proximidade com a cobra
                self.obstacles = self.create_obstacles(len(self.obstacles))
                while self.checkCollisionWithObstacles():
                    self.obstacles = self.create_obstacles(len(self.obstacles))
                
            for i, s in enumerate(self.snake):
                s.color = self.get_snake_segment_color(i)
                self.canvas.create_rectangle(s.pos(), fill=s.color, outline='black')
                
            self.canvas.create_rectangle(self.food.pos(), fill=self.food.color, outline='black')
            
            for obstacle in self.obstacles:
                self.canvas.create_rectangle(obstacle.pos(), fill=obstacle.color, outline='black')

            # Desenha a pontuação com uma fonte estilizada
            self.canvas.create_text(width - 100, 20, text=f"Score: {self.score}", fill="white", font=("Press Start 2P", 24))

            # Verifica colisão com a própria cobra
            for i in range(2, len(self.snake)):
                if self.intersect(self.snake[0].pos(), self.snake[i].pos()):
                    showinfo(title="Game Over", message="GAME OVER!!!")
                    self.window.destroy()
                    return

            if self.checkCollisionWithObstacles():
                showinfo(title="Game Over", message="GAME OVER!!!")
                self.window.destroy()
                return

            self.canvas.after(speed)
            self.window.update_idletasks()
            self.window.update()

class MainMenu:
    def __init__(self):
        self.window = Tk()
        self.window.title("Menu Inicial")
        
        # Define o tamanho da janela
        self.window.geometry("800x600")
        self.window.configure(bg='black')

        # Fonte para o título e texto
        title_font = Font(family="Press Start 2P", size=48)
        button_font = Font(family="Press Start 2P", size=20)

        # Criação de um frame para centralizar o conteúdo
        frame = Frame(self.window, bg='green')
        frame.pack(expand=True, fill=BOTH)

        # Título com borda
        title_label = Label(frame, text="NAJA", font=title_font, fg='white', bg='green')
        title_label.pack(pady=20)

        # Texto de instrução
        instruction_label = Label(frame, text="Escolha a cor da cobrinha", font=("Press Start 2P", 24), fg='white', bg='green')
        instruction_label.pack(pady=10)

        # Botões de seleção de cor
        self.create_color_button(frame, "Pink", 'pink', self.start_game)
        self.create_color_button(frame, "Green", 'green', self.start_game)
        self.create_color_button(frame, "Red", 'red', self.start_game)
        self.create_color_button(frame, "Black", 'black', self.start_game)
        self.create_color_button(frame, "Purple", 'purple', self.start_game)
        self.create_color_button(frame, "Yellow", 'yellow', self.start_game)
        
        self.window.mainloop()

    def create_color_button(self, parent, color_name, color, command):
        button = Button(parent, text=color_name, font=("Press Start 2P", 20), fg='white', bg=color, command=lambda: command(color))
        button.pack(pady=5, padx=10)

    def start_game(self, snake_color):
        self.window.destroy()
        game = Game(snake_color)
        game.run()

if __name__ == "__main__":
    menu = MainMenu()
