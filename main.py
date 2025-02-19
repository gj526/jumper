import pygame
import random

# تهيئة pygame
pygame.init()

# إعداد الشاشة بملء الشاشة للهاتف
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("لعبة القفز")

# الألوان
BACKGROUND_COLOR = (34, 24, 89)  # #221859 لون الخلفية
WHITE = (255, 255, 255)  # لون اللاعب
COLUMN_COLOR = (255, 0, 85)  # #ff0055 لون الأعمدة
GRAY = (200, 200, 200)  # لون زر تغيير اللغة

# إعداد الخطوط
font = pygame.font.Font(None, WIDTH // 12)
small_font = pygame.font.Font(None, WIDTH // 20)
tiny_font = pygame.font.Font(None, WIDTH // 28)  # خط أصغر لأعلى سكور

# لغة اللعبة (افتراضيًا إنجليزية)
language = "EN"

# إعداد اللاعب
player_radius = WIDTH // 20  # نصف قطر الدائرة
player_x = WIDTH // 2
player_y = HEIGHT // 2  # يقف في منتصف الشاشة
player_velocity = 0
gravity = HEIGHT * 0.0015
jump_strength = -HEIGHT * 0.05  # القفز أقوى بمرتين
can_jump = True  # السماح بالقفز عند بداية اللعبة

# إعداد الأعمدة
column_width = player_radius * 2
column_speed = WIDTH * 0.02  # سرعة الأعمدة
move_columns = False  # التحكم في حركة الأعمدة باللمس

# قائمة الأعمدة (أول عمود لا يحتسب في النقاط)
columns = [
    {"x": WIDTH // 2 - column_width // 2, "y": HEIGHT // 2 + player_radius * 2, "height": HEIGHT // 2, "scored": True}
]

# الأرضية
ground_height = HEIGHT * 0.03

# النقاط
score = 0
high_score = 0  # أعلى معدل سكور

# زر تغيير اللغة
button_size = WIDTH // 10
button_rect = pygame.Rect(WIDTH - button_size - 10, 10, button_size, button_size)

# حالة البداية (قبل بدء اللعبة)
game_started = False
gravity_enabled = False  # الجاذبية تبدأ فقط بعد اللمس الأول

# حلقة اللعبة
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)  # تعيين لون الخلفية

    # الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if button_rect.collidepoint(mouse_x, mouse_y):  # تغيير اللغة
                language = "AR" if language == "EN" else "EN"
            else:
                game_started = True  # بدء اللعبة عند اللمس
                gravity_enabled = True  # تفعيل الجاذبية بعد اللمس الأول
                move_columns = True  # تشغيل حركة الأعمدة
        if event.type == pygame.MOUSEBUTTONUP:
            move_columns = False  # توقف الأعمدة عند رفع الإصبع

    # **عرض رسالة البداية قبل بدء اللعبة**
    if not game_started:
        start_text = "Click to start" if language == "EN" else "انقر للبدء"
        text_surface = font.render(start_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        # زر تغيير اللغة
        pygame.draw.rect(screen, GRAY, button_rect)
        lang_text = small_font.render("AR" if language == "EN" else "EN", True, WHITE)
        lang_rect = lang_text.get_rect(center=button_rect.center)
        screen.blit(lang_text, lang_rect)

        pygame.display.flip()
        continue  # انتظار اللمس لبدء اللعبة

    # **من هنا تبدأ اللعبة بعد لمس الشاشة**
    
    # تطبيق الجاذبية فقط إذا تم تفعيلها
    if gravity_enabled:
        player_velocity += gravity
        player_y += player_velocity

    # تحريك الأعمدة عند لمس الشاشة
    if move_columns:
        for column in columns:
            column["x"] -= column_speed

    # إضافة أعمدة جديدة
    if columns[-1]["x"] < WIDTH - random.randint(6, 8) * player_radius * 2:
        new_height = random.randint(HEIGHT // 4, HEIGHT // 2)
        columns.append({"x": WIDTH, "y": HEIGHT - new_height, "height": new_height, "scored": False})

    # إزالة الأعمدة القديمة
    columns = [column for column in columns if column["x"] > -column_width]

    # التحقق من التصادم مع الأعمدة
    on_column = False
    for column in columns:
        if (player_x + player_radius > column["x"] and player_x - player_radius < column["x"] + column_width and
                player_y + player_radius >= column["y"]):
            player_y = column["y"] - player_radius * 2
            player_velocity = 0
            on_column = True
            if not column["scored"]:
                score += 1
                column["scored"] = True
                if score > high_score:
                    high_score = score
            can_jump = True

    # تنفيذ القفز
    if can_jump and move_columns:
        player_velocity = jump_strength
        can_jump = False

    # إذا لم يكن هناك عمود تحته، يسقط
    if not on_column and player_y + player_radius < HEIGHT - ground_height:
        player_velocity += gravity

    # إذا لمس الأرض يخسر
    if player_y + player_radius >= HEIGHT - ground_height:
        score = 0
        player_y = HEIGHT // 2  # يعود إلى منتصف الشاشة
        columns = [{"x": WIDTH // 2 - column_width // 2, "y": HEIGHT // 2 + player_radius * 2, "height": HEIGHT // 2, "scored": True}]
        can_jump = True
        game_started = False  # إعادة اللعبة لحالة البداية
        gravity_enabled = False  # إيقاف الجاذبية حتى يلمس اللاعب الشاشة مرة أخرى

    # رسم الأعمدة
    for column in columns:
        pygame.draw.rect(screen, COLUMN_COLOR, (column["x"], column["y"], column_width, column["height"]))

    # رسم اللاعب (دائرة)
    pygame.draw.circle(screen, WHITE, (player_x, int(player_y)), player_radius)

    # عرض النقاط في أعلى منتصف الشاشة
    score_text = font.render(f"{score}", True, WHITE)
    score_rect = score_text.get_rect(midtop=(WIDTH // 2, 20))
    screen.blit(score_text, score_rect)

    # عرض أعلى سكور تحت النقاط
    high_score_text = tiny_font.render(f"Best: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(midtop=(WIDTH // 2, score_rect.bottom + 5))
    screen.blit(high_score_text, high_score_rect)

    # زر تغيير اللغة
    pygame.draw.rect(screen, GRAY, button_rect)
    lang_text = small_font.render("AR" if language == "EN" else "EN", True, WHITE)
    lang_rect = lang_text.get_rect(center=button_rect.center)
    screen.blit(lang_text, lang_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
