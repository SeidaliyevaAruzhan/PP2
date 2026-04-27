import pygame
import datetime
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

tool = "pencil"
drawing = False
start_pos = None
last_pos = None
brush_size = 2
color = (0, 0, 0)

typing = False
text_input = ""
text_pos = None
font = pygame.font.SysFont(None, 28)

palette = [
    (0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),
    (255,255,0),(255,165,0),(128,0,128),(0,255,255),(255,192,203)
]

palette_rects = []
size = 30
margin = 10
px = WIDTH - 80
py = 60

for i, col in enumerate(palette):
    x = px + (i % 2) * (size + margin)
    y = py + (i // 2) * (size + margin)
    palette_rects.append((pygame.Rect(x, y, size, size), col))

tools = ["pencil","line","rect","square","circle","triangle","rhombus","fill","text"]
tool_buttons = []
bx, by = 10, 10
bw, bh, gap = 44, 44, 8

for i, name in enumerate(tools):
    rect = pygame.Rect(bx + i*(bw+gap), by, bw, bh)
    tool_buttons.append((rect, name))

def draw_icon(surface, rect, name, col=(30,30,30)):
    x, y, w, h = rect
    cx, cy = x + w//2, y + h//2
    pad = 6

    if name == "pencil":
        pygame.draw.line(surface, col, (x+pad, y+h-pad), (x+w-pad, y+pad), 3)
        pygame.draw.circle(surface, col, (x+w-pad, y+pad), 3)

    elif name == "line":
        pygame.draw.line(surface, col, (x+pad, y+h-pad), (x+w-pad, y+pad), 3)

    elif name == "rect":
        pygame.draw.rect(surface, col, (x+pad, y+pad, w-2*pad, h-2*pad), 2)

    elif name == "square":
        s = min(w, h) - 2*pad
        pygame.draw.rect(surface, col, (cx - s//2, cy - s//2, s, s), 2)

    elif name == "circle":
        r = min(w, h)//2 - pad
        pygame.draw.circle(surface, col, (cx, cy), r, 2)

    elif name == "triangle":
        pts = [(cx, y+pad), (x+w-pad, y+h-pad), (x+pad, y+h-pad)]
        pygame.draw.polygon(surface, col, pts, 2)

    elif name == "rhombus":
        pts = [(cx, y+pad), (x+w-pad, cy), (cx, y+h-pad), (x+pad, cy)]
        pygame.draw.polygon(surface, col, pts, 2)

    elif name == "fill":
        pygame.draw.rect(surface, col, (x+pad, y+pad, w-2*pad, h//3), 2)
        pygame.draw.polygon(surface, col, [(x+pad, y+pad+h//3),
                                           (x+w-pad, y+pad+h//3),
                                           (x+w-pad-6, y+h-pad),
                                           (x+pad+6, y+h-pad)], 2)

    elif name == "text":
        pygame.draw.line(surface, col, (x+pad, y+pad), (x+w-pad, y+pad), 3)
        pygame.draw.line(surface, col, (cx, y+pad), (cx, y+h-pad), 3)

def flood_fill(surface, x, y, new_color):
    target = surface.get_at((x, y))
    if target == new_color:
        return
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if surface.get_at((x, y)) == target:
            surface.set_at((x, y), new_color)
            if x > 0: stack.append((x-1, y))
            if x < surface.get_width()-1: stack.append((x+1, y))
            if y > 0: stack.append((x, y-1))
            if y < surface.get_height()-1: stack.append((x, y+1))

running = True

while running:
    screen.fill((200,200,200))
    screen.blit(canvas, (0,0))
    temp = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: brush_size = 2
            if event.key == pygame.K_2: brush_size = 5
            if event.key == pygame.K_3: brush_size = 10

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                fname = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, fname)

            if typing:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input, True, color)
                    canvas.blit(txt, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, col in palette_rects:
                if rect.collidepoint(event.pos):
                    color = col

            for rect, name in tool_buttons:
                if rect.collidepoint(event.pos):
                    tool = name

            if tool == "pencil":
                drawing = True
                last_pos = event.pos

            elif tool in ["line","rect","circle","square","triangle","rhombus"]:
                drawing = True
                start_pos = event.pos

            elif tool == "fill":
                flood_fill(canvas, event.pos[0], event.pos[1], color)

            elif tool == "text":
                typing = True
                text_pos = event.pos
                text_input = ""

        if event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if tool == "pencil":
                drawing = False

            elif drawing:
                end = event.pos

                if tool == "line":
                    pygame.draw.line(canvas, color, start_pos, end, brush_size)

                elif tool == "rect":
                    r = pygame.Rect(start_pos, (end[0]-start_pos[0], end[1]-start_pos[1]))
                    pygame.draw.rect(canvas, color, r, brush_size)

                elif tool == "square":
                    s = min(abs(end[0]-start_pos[0]), abs(end[1]-start_pos[1]))
                    r = pygame.Rect(start_pos, (s, s))
                    pygame.draw.rect(canvas, color, r, brush_size)

                elif tool == "circle":
                    rad = int(math.hypot(end[0]-start_pos[0], end[1]-start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, rad, brush_size)

                elif tool == "triangle":
                    pygame.draw.polygon(canvas, color, [
                        start_pos, (end[0], start_pos[1]), end
                    ], brush_size)

                elif tool == "rhombus":
                    mx = (start_pos[0]+end[0])//2
                    my = (start_pos[1]+end[1])//2
                    pygame.draw.polygon(canvas, color, [
                        (mx, start_pos[1]), (end[0], my),
                        (mx, end[1]), (start_pos[0], my)
                    ], brush_size)

                drawing = False

    if drawing and tool in ["line","rect","circle","square","triangle","rhombus"]:
        mx, my = pygame.mouse.get_pos()

        if tool == "line":
            pygame.draw.line(temp, color, start_pos, (mx,my), brush_size)

        elif tool == "rect":
            r = pygame.Rect(start_pos, (mx-start_pos[0], my-start_pos[1]))
            pygame.draw.rect(temp, color, r, brush_size)

        elif tool == "square":
            s = min(abs(mx-start_pos[0]), abs(my-start_pos[1]))
            r = pygame.Rect(start_pos, (s, s))
            pygame.draw.rect(temp, color, r, brush_size)

        elif tool == "circle":
            rad = int(math.hypot(mx-start_pos[0], my-start_pos[1]))
            pygame.draw.circle(temp, color, start_pos, rad, brush_size)

        elif tool == "triangle":
            pygame.draw.polygon(temp, color, [
                start_pos, (mx, start_pos[1]), (mx, my)
            ], brush_size)

        elif tool == "rhombus":
            mx2 = (start_pos[0]+mx)//2
            my2 = (start_pos[1]+my)//2
            pygame.draw.polygon(temp, color, [
                (mx2, start_pos[1]), (mx, my2),
                (mx2, my), (start_pos[0], my2)
            ], brush_size)

        screen.blit(temp, (0,0))

    for rect, col in palette_rects:
        pygame.draw.rect(screen, col, rect)
        if col == color:
            pygame.draw.rect(screen, (0,0,0), rect, 3)

    for rect, name in tool_buttons:
        pygame.draw.rect(screen, (180,180,180), rect, border_radius=6)
        if tool == name:
            pygame.draw.rect(screen, (0,0,0), rect, 3, border_radius=6)
        draw_icon(screen, rect, name, (20,20,20))

    if typing:
        prev = font.render(text_input, True, color)
        screen.blit(prev, text_pos)

    pygame.display.flip()

pygame.quit()