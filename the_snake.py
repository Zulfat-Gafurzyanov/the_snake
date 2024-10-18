from random import choices, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс GameObject - родительский класс,
    от которого наследуются другие игровые объекты.
    """

    def __init__(self) -> None:
        """Инициализирует базовые атрибуты класса:
        position - позиция объекта на поле (по умолчанию: середина экрана).
        body_color - цвет объекта.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Предназначен для переопределения в дочерних классах."""
        pass


class Apple(GameObject):
    """Дочерний класс - яблоко, который наследуются от класса GameObject."""

    def __init__(self):
        """Задаёт цвет яблока (по умолчанию: красный (255, 0, 0))
        и вызывает метод randomize_position,
        чтобы установить начальную позицию яблока.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            (randrange(0, SCREEN_WIDTH, 20),
             randrange(0, SCREEN_HEIGHT, 20))
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс - змейка, который наследуются от класса GameObject."""

    def __init__(self):
        """Инициализирует атрибуты класса:
        length - длина змейки (по умолчанию: 1).
        positions - список, содержащий позиции всех сегментов тела змейки.
        direction - направление движения змейки (по умолчанию: вправо).
        next_direction - следующее направление движения (по умолчанию: None)
        body_color - цвет змейки (по умолчанию: зелёный (0, 255, 0))
        last - последний элемент в списке positions (по умолчанию: None,
        потому что изначально у змеи есть только голова).
        """
        super().__init__()
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Модифицирует список positions для обновления позиции змейки"""
        self.dx, self.dy = self.get_head_position()
        # Вычисляем новую позицию головы по координатам (dx, dy),
        # в зависимосты от направления.
        if self.direction == RIGHT:
            self.dx = self.dx + GRID_SIZE
        elif self.direction == LEFT:
            self.dx = self.dx - GRID_SIZE
        elif self.direction == UP:
            self.dy = self.dy - GRID_SIZE
        elif self.direction == DOWN:
            self.dy = self.dy + GRID_SIZE
        # Добавляем новую позицию в начало списка.
        self.positions.insert(0, (self.dx, self.dy))
        # Осуществляем обработку краев экрана: если змейка достигает
        # края экрана, то она появляется с противоположной стороны.
        if self.dx == SCREEN_WIDTH:
            self.positions[0] = 0, self.dy
        elif self.dy == SCREEN_HEIGHT:
            self.positions[0] = self.dx, 0
        elif self.dx == -20:
            self.positions[0] = SCREEN_WIDTH, self.dy
        elif self.dy == -20:
            self.positions[0] = self.dx, SCREEN_HEIGHT
        # Объявляем позицию последнего сегмента змейки.
        self.last = self.positions[-1]
        # Имитируем движение змеи: проверяем текущую длину змейки с её
        # максимальным значением. Если длина превышает, то последний элемент
        # списка удаляем.
        if len(self.positions) > self.length:
            self.positions.pop(-1)

    def draw(self):
        """Отрисовывает змейку на экране"""
        # Отрисовываем голову.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Отрисовываем смену позиций.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Стираем последний сегмент.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.nextdirection = choices([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает действия пользователя при нажатии на клавиши,
    для изменения направления движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описывает соновной цикл игры."""
    # Инициализируем PyGame:
    pygame.init()
    # Cоздаем экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        # Проверяем появления яблока на теле змейки.
        # При положительном исходе, перемещаем яблоко в другое место.
        if apple.position == snake.positions:
            apple.randomize_position()
        # Проверяем, съела ли змейка яблоко.
        # При положительном исходе увеличиваем длину змеи.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Проверяем факт столкновения змейки с собой.
        # При положительном исходе, сбросываем игру при помощи метода reset.
        if snake.get_head_position() in snake.positions[1:-1]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            snake.draw()
            apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
