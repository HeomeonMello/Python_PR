import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        print("Bubble areas:", area)
        print("Bubble radii:", r)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 6))  # shape (6,)
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.bubbles[:, 4:6] = self.bubbles[:, :2]  # 원래 위치를 저장
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]
        self.bubbles[:, 4:6] = self.bubbles[:, :2]  # 원래 위치 저장

        self.com = self.center_of_mass()
        self.fig = None
        self.ax = None
        self.hover_bubble = None
        self.mouse_x = None
        self.mouse_y = None

    def center_of_mass(self):
        return np.average(self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3])

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0], bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return np.argmin(distance, keepdims=True)

    def collapse(self, n_iterations=50):
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                dir_vec = self.com - self.bubbles[i, :2]

                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:])

                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        new_point1 = (self.bubbles[i, :2] + orth * self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth * self.step_dist)
                        dist1 = self.center_distance(self.com, np.array([new_point1]))
                        dist2 = self.center_distance(self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            new_bubble = np.append(new_point, self.bubbles[i, 2:])
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def wrap_text(self, text, max_width):
        from textwrap import wrap
        wrapped_text = "\n".join(wrap(text, width=max_width))
        return wrapped_text

    def plot(self, fig, ax, labels, colors, font_properties):
        self.fig = fig
        self.ax = ax

        max_font_size = 20
        min_font_size = 8
        font_size_range = max_font_size - min_font_size

        self.circles = []
        self.texts = []
        for i in range(len(self.bubbles)):
            circ = Circle(self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            self.circles.append(circ)

            # 글씨 크기를 키워드 순위에 따라 조정
            font_size = max_font_size - (i * font_size_range / (len(self.bubbles) - 1))

            # 텍스트 줄 바꿈 적용
            max_width = 6  # 글씨의 최대 너비를 지정
            wrapped_text = self.wrap_text(labels[i], max_width)

            text = ax.text(*self.bubbles[i, :2], wrapped_text,
                           horizontalalignment='center', verticalalignment='center',
                           fontproperties=font_properties, fontsize=font_size)
            self.texts.append(text)

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        self.fig.canvas.mpl_connect("draw_event", self.update)

    def on_hover(self, event):
        if self.ax is None:
            return
        if event.xdata is None or event.ydata is None:
            self.hover_bubble = None
            return
        self.mouse_x = event.xdata
        self.mouse_y = event.ydata

    def update(self, event=None):
        if self.mouse_x is not None and self.mouse_y is not None:
            for i, bubble in enumerate(self.bubbles):
                dist = np.hypot(bubble[0] - self.mouse_x, bubble[1] - self.mouse_y)
                if dist < bubble[2] * 2:  # 마우스 근처에 있는 버블만 이동
                    direction = np.array([bubble[0] - self.mouse_x, bubble[1] - self.mouse_y])
                    direction = direction / np.linalg.norm(direction)  # 방향 벡터를 단위 벡터로 만듦
                    bubble[:2] += direction * 2  # 이동 거리 조정
        else:
            for bubble in self.bubbles:
                direction = np.array([bubble[4] - bubble[0], bubble[5] - bubble[1]])
                if np.linalg.norm(direction) > 0.1:
                    direction = direction / np.linalg.norm(direction)
                    bubble[:2] += direction * 0.5  # 원래 위치로 돌아가는 힘 추가

        for i, bubble in enumerate(self.bubbles):
            circ = self.circles[i]
            text = self.texts[i]
            circ.center = (bubble[0], bubble[1])
            text.set_position((bubble[0], bubble[1]))
        self.fig.canvas.draw_idle()
