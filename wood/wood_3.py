import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

self_x = 0
self_y = 0
self_vx = 0
self_vy = 0
self_v_length = 0

target_x = 0
target_y = 0
target_throttle = 0

best_wreck = -1
best_wreck_players_at = -1


def calcThrotlle(self_x, self_y, target_x, target_y):
    arg_0 = math.pow(target_x - self_x, 2.0)
    arg_1 = math.pow(target_y - self_y, 2.0)
    dist = math.sqrt(arg_0 + arg_1)

    if dist < 200:
        if self_v_length > 100:
            return 0
        else:
            return 100
    else:
        return 300


# game loop
while True:
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())

    for i in range(unit_count):
        inputs = input().split()
        unit_id = int(inputs[0])
        unit_type = int(inputs[1])
        player = int(inputs[2])
        mass = float(inputs[3])
        radius = int(inputs[4])
        x = int(inputs[5])
        y = int(inputs[6])
        vx = int(inputs[7])
        vy = int(inputs[8])
        extra = int(inputs[9])
        extra_2 = int(inputs[10])

        if unit_type == 4:
            target_x = x
            target_y = y

        if unit_id == 0:
            self_x = x
            self_y = y
            self_vx = vx
            self_vy = vy
            self_v_length = math.sqrt(math.pow(self_vx, 2.0) + math.pow(self_vy, 2.0))

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    target_throttle = calcThrotlle(self_x, self_y, target_x, target_y)

    print(str(target_x) + " " + str(target_y) + " " + str(target_throttle))
    print("WAIT")
    print("WAIT")

