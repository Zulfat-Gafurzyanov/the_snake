from random import randrange, choice

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
SPEED = 15

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

    def __init__(
        self,
        position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
        body_color=None
    ) -> None:
        """Инициализирует базовые атрибуты класса:
        position - позиция объекта на поле (по умолчанию: середина экрана).
        body_color - цвет объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Создали метод-шаблон."""
        # Возникнет, если в дочерних классах не переопределить метод-шаблон.
        raise NotImplementedError('Необходимо переопределить метод draw'
                                  'в классах Apple и Snake'
                                  )


class Apple(GameObject):
    """Дочерний класс - яблоко, который наследуются от класса GameObject."""

    def __init__(
            self,
            position=(
                randrange(0, (SCREEN_WIDTH - GRID_SIZE), GRID_SIZE),
                randrange(0, (SCREEN_HEIGHT - GRID_SIZE), GRID_SIZE)
            ),
            body_color=APPLE_COLOR
    ):
        """Инициализирует атрибуты класса:
        position - позиция яблока на поле (по умолчанию: в случайном месте)
        body_color - цвет яблока (по умолчанию: красный (255, 0, 0)).
        Вызывает метод randomize_position, чтобы установить начальную позицию
        яблока.
        """
        super().__init__(position, body_color)

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        # Проверяем появления яблока на теле змейки (аргумент: positions).
        # Eсли яблоко появилось на змейке, то размещаем яблоко
        # случайным образом на экране.
        if self.position in positions:
            self.position = (
                randrange(0, (SCREEN_WIDTH - GRID_SIZE), GRID_SIZE),
                randrange(0, (SCREEN_HEIGHT - GRID_SIZE), GRID_SIZE)
            )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс - змейка, который наследуются от класса GameObject."""

    def __init__(
        self,
        position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
        body_color=SNAKE_COLOR
    ):
        """Задаёт цвет змейки (по умолчанию: зеленый (0, 255, 0)),
        direction - начальное направление (по умолчанию: направо),
        next_direction - следующее направление движения,
        last - последний элемент списка (хвост змейки)
        и вызывает метод reset().
        """
        super().__init__(position, body_color)
        self.direction = RIGHT
        self.reset()

    def reset(self):
        """Устанавливает длину змейки = 1 и позицию головы в центр экрана.
        Устанавливает случайное направление движения в налале игры.
        """
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.next_direction = choice((UP, DOWN, LEFT, RIGHT))

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Модифицирует список positions для обновления позиции змейки"""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        # Вычисляем новую позицию головы по координатам (dx, dy),
        # в зависимости от направления.
        # Обработку краев экрана осуществляем с помощью остатка от деления: %)
        new_head_positions = ((head_x + direction_x
                               * GRID_SIZE) % SCREEN_WIDTH,
                              (head_y + direction_y
                               * GRID_SIZE) % SCREEN_HEIGHT
                              )
        # Добавляем новую позицию в начало списка.
        self.positions.insert(0, (new_head_positions))
        # Имитируем движение змеи: проверяем текущую длину змейки с её
        # максимальным значением. Если длина превышает, то последний элемент
        # списка удаляем. Если хвоста нет, атрибуту присваиваем: None.
        if len(self.positions) == self.length:
            self.last = None
        elif len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране"""
        # Стираем хвост.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        # Отрисовываем голову.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


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

    # Cоздаем экземпляры класса.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Проверяем, съела ли змейка яблоко. При положительном исходе
        # увеличиваем длину змеи.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Размещаем новое яблоко с учетом позиции змейки.
            apple.randomize_position(snake.positions)
        # Проверяем факт столкновения змейки с собой.
        # При положительном исходе, сбросываем игру при помощи метода reset.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
