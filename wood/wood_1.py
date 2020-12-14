import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# self_x = 0
# self_y = 0
# self_vx = 0
# self_vy = 0
# self_v_length = 0

# target_x = 0
# target_y = 0
# target_throttle = 0


class PlayerVars:
    rage = -1
    reaper_command = ""
    destroyer_command = ""
    doof_command = ""


p_vars = PlayerVars()


class Vector2:
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_length(self):
        return math.sqrt(math.pow(self.x, 2.0) + math.pow(self.y, 2.0))

    def distance_to_point(self, x, y):
        arg_0 = math.pow(x - self.x, 2.0)
        arg_1 = math.pow(y - self.y, 2.0)
        dist = math.sqrt(arg_0 + arg_1)

        return dist


class Entity:
    id = -1
    pos = Vector2()
    radius = -1

    def __init__(self, id, pos, radius):
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.radius = radius

    def distance_to(self, target_pos):
        arg_0 = math.pow(target_pos.x - self.pos.x, 2.0)
        arg_1 = math.pow(target_pos.y - self.pos.y, 2.0)
        dist = math.sqrt(arg_0 + arg_1)

        return dist

    def contains_point(self, p):
        if self.distance_to(p) < self.radius:
            return True
        else:
            return False


class Wreck(Entity):
    water_lvl = -1

    def __init__(self, id, pos, radius, water_lvl):
        self.id = id
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.radius = radius
        self.water_lvl = water_lvl


class Vehicle(Entity):
    vel = Vector2()
    player_id = None
    mass = None

    def __init__(self, id, pos, radius, vel, player_id, mass):
        self.id = id
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.radius = radius
        self.player_id = player_id
        self.mass = mass


class Reaper(Vehicle):
    throttle = -1
    target = None
    target_is_destroyer = False

    def update(self, wrecks, vehicles):
        if self.player_id != 0:
            return

        self.set_target(wrecks, vehicles)
        self.calc_throttle()
        self.set_command()

    def set_target(self, wrecks, vehicles):
        if self.target is not None:
            return

        if len(wrecks) == 0:
            # self.set_target_destroyer(vehicles)
            self.target = None
        else:
            self.set_target_closest_wreck(wrecks)

    def set_target_destroyer(self, vehicles):
        for i in range(len(vehicles)):
            curr_vehicle = vehicles[i]
            if isinstance(curr_vehicle, Destroyer) and curr_vehicle.player_id == 0:
                self.target = curr_vehicle
                self.target_is_destroyer = True
                return

    def set_target_closest_wreck(self, wrecks):
        min_dist = None
        closest_wreck = None

        for i in range(len(wrecks)):
            if i == 0:
                min_dist = wrecks[i].distance_to(self.pos)
                closest_wreck = wrecks[i]
            else:
                new_dist = wrecks[i].distance_to(self.pos)
                if new_dist < min_dist:
                    min_dist = new_dist
                    closest_wreck = wrecks[i]

        self.target = closest_wreck
        self.target_is_destroyer = False

    def set_target_fullest_wreck(self, wrecks):
        global p_vars

        max_water_lvl = None
        fullest_wreck = None

        for i in range(len(wrecks)):
            if i == 0:
                max_water_lvl = wrecks[i].water_lvl
                fullest_wreck = wrecks[i]
            else:
                new_water_lvl = wrecks[i].water_lvl
                if new_water_lvl > max_water_lvl:
                    max_water_lvl = new_water_lvl
                    fullest_wreck = wrecks[i]

        self.target_is_destroyer = False
        self.target = fullest_wreck

    def calc_throttle(self):
        if self.target is None:
            self.throttle = -1
            return

        dist = self.distance_to(self.target.pos)

        if dist < 600:
            if self.vel.get_length() > 100:
                self.throttle = 0
            else:
                self.throttle = 100
        else:
            self.throttle = 300

    def set_command(self):
        global p_vars
        if self.throttle == -1:
            p_vars.reaper_command = "WAIT"
        else:
            p_vars.reaper_command = str(self.target.pos.x) + " " + str(self.target.pos.y) + " " + str(self.throttle)


class Destroyer(Vehicle):
    throttle = -1
    target = None
    throw_pos = None

    def update(self, wrecks, vehicles):
        if self.player_id != 0:
            return

        self.set_target_closest(vehicles)
        self.calc_throttle()
        self.throw_grenade(wrecks, vehicles)
        self.set_command()

    def set_target_fullest(self, vehicles):
        if self.target is not None:
            return

        first_tanker = True
        for i in range(len(vehicles)):
            curr_vehicle = vehicles[i]
            if isinstance(curr_vehicle, Tanker):
                if first_tanker:
                    self.target = curr_vehicle
                    first_tanker = False
                else:
                    if curr_vehicle.water_lvl > self.target.water_lvl:
                        self.target = curr_vehicle

    def set_target_closest(self, vehicles):
        if self.target is not None:
            return

        map_center = Vector2(0, 0)
        first_tanker = True
        for i in range(len(vehicles)):
            curr_vehicle = vehicles[i]
            if isinstance(curr_vehicle, Tanker):
                if map_center.distance_to_point(curr_vehicle.pos.x, curr_vehicle.pos.y) > 5500:
                    continue

                if first_tanker:
                    self.target = curr_vehicle
                    first_tanker = False
                else:
                    if curr_vehicle.distance_to(self.pos) < self.target.distance_to(self.pos):
                        self.target = curr_vehicle

    def calc_throttle(self):
        if self.target is None:
            self.throttle = -1
            return

        dist = self.distance_to(self.target.pos)
        self.throttle = 300

    def throw_grenade(self, wrecks, vehicles):
        global p_vars

        print(p_vars.rage, file=sys.stderr, flush=True)
        if p_vars.rage < 60:
            return

        for i in range(len(wrecks)):
            curr_wreck = wrecks[i]
            for j in range(len(vehicles)):
                curr_vehicle = vehicles[j]
                if curr_wreck.contains_point(curr_vehicle.pos) and self.distance_to(curr_wreck.pos) < 2000 and curr_vehicle.player_id != 0:
                    self.throw_pos = curr_wreck.pos
                    break

    def set_command(self):
        global p_vars
        if self.throw_pos is not None:
            p_vars.destroyer_command = "SKILL " + str(self.throw_pos.x) + " " + str(self.throw_pos.y)
            self.throw_pos = None
        elif self.throttle == -1:
            p_vars.destroyer_command = "WAIT"
        else:
            p_vars.destroyer_command = str(self.target.pos.x) + " " + str(self.target.pos.y) + " " + str(self.throttle)


class Doof(Vehicle):
    throttle = -1
    target_pos = None
    min_dist = 50
    range = 2000
    max_attemps = 20

    def update(self, wrecks, vehicles):
        if self.player_id != 0:
            return

        self.set_target(vehicles)
        self.calc_throttle()
        self.set_command()

    def set_target(self, vehicles):
        if self.target_pos is not None and self.distance_to(self.target_pos) > self.min_dist:
            return

        target_valid = False
        new_target_pos = None
        attemps_left = self.max_attemps
        while not target_valid and attemps_left > 0:
            new_target_pos = self.create_new_target()
            attemps_left -= 1
            target_valid = True
            for i in range(len(vehicles)):
                curr_vehicle = vehicles[i]
                if curr_vehicle.contains_point(new_target_pos):
                    target_valid = False
                    break

        if target_valid:
            self.target_pos = new_target_pos
        else:
            self.target_pos = None

    def create_new_target(self):
        angle = random.random() * math.pi * 2
        new_target_pos = Vector2(int(math.cos(angle) * self.range), int(math.sin(angle) * self.range))
        return new_target_pos

    def calc_throttle(self):
        if self.target_pos is None:
            self.throttle = -1
            return
        self.throttle = 300

    def set_command(self):
        global p_vars
        if self.throttle == -1:
            p_vars.doof_command = "WAIT"
        else:
            p_vars.doof_command = str(self.target_pos.x) + " " + str(self.target_pos.y) + " " + str(self.throttle)


class Tanker(Vehicle):
    water_lvl = -1
    capacity = -1

    def __init__(self, id, pos, radius, vel, player_id, mass, water_lvl, capacity):
        self.id = id
        self.pos.x = pos.x
        self.pos.y = pos.y
        self.radius = radius
        self.player_id = player_id
        self.mass = mass
        self.water_lvl = water_lvl
        self.capacity = capacity

    def update(self, wrecks, vehicles):
        return


def clean_Nones_list(list_to_clean):
    for i in range(len(list_to_clean) - 1, 0, -1):
        if list_to_clean[i] is None:
            del list_to_clean[i]


def update_list_entity(vehicles, wrecks, unit_id, unit_type, mass, pos, vel, extra, extra_2):
    if unit_type == 4:
        for i in range(len(wrecks)):
            curr_entity = wrecks[i]
            if curr_entity.id == unit_id:
                curr_entity.water_lvl = extra
    else:
        for i in range(len(vehicles)):
            curr_entity = vehicles[i]
            if curr_entity.id == unit_id:
                curr_entity.mass = mass
                curr_entity.pos = pos
                curr_entity.vel = vel
                if unit_type == 3:
                    curr_entity.water_lvl = extra


def add_entity_to_lists(vehicles, wrecks, unit_id, unit_type, player_id, mass, radius, pos, vel, extra, extra_2):
    if unit_type == 0:
        new_unit_pos = Vector2(x, y)
        new_unit_vel = Vector2(vx, vy)
        new_reaper = Reaper(unit_id, new_unit_pos, radius, new_unit_vel, player_id, mass)
        vehicles.append(new_reaper)
    elif unit_type == 1:
        new_unit_pos = Vector2(x, y)
        new_unit_vel = Vector2(vx, vy)
        new_destroyer = Destroyer(unit_id, new_unit_pos, radius, new_unit_vel, player_id, mass)
        vehicles.append(new_destroyer)
    elif unit_type == 2:
        new_unit_pos = Vector2(x, y)
        new_unit_vel = Vector2(vx, vy)
        new_doof = Doof(unit_id, new_unit_pos, radius, new_unit_vel, player_id, mass)
        vehicles.append(new_doof)
    elif unit_type == 3:
        new_unit_pos = Vector2(x, y)
        new_unit_vel = Vector2(vx, vy)
        new_tanker = Tanker(unit_id, new_unit_pos, radius, new_unit_vel, player_id, mass, extra, extra_2)
        vehicles.append(new_tanker)
    elif unit_type == 4:
        new_unit_pos = Vector2(x, y)
        new_wreck = Wreck(unit_id, new_unit_pos, radius, extra)
        wrecks.append(new_wreck)


wrecks = []
vehicles = []

# game loop
while True:
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())

    p_vars.rage = my_rage
    for i in range(unit_count):
        inputs = input().split()
        unit_id = int(inputs[0])
        unit_type = int(inputs[1])
        player_id = int(inputs[2])
        mass = float(inputs[3])
        radius = int(inputs[4])
        x = int(inputs[5])
        y = int(inputs[6])
        vx = int(inputs[7])
        vy = int(inputs[8])
        extra = int(inputs[9])
        extra_2 = int(inputs[10])

        pos = Vector2(x, y)
        vel = Vector2(vx, vy)

        unit_exists = False
        for i in range(len(vehicles)):
            if vehicles[i].id == unit_id:
                unit_exists = True
                break

        if not unit_exists:
            for i in range(len(wrecks)):
                if wrecks[i].id == unit_id:
                    unit_exists = True
                    break

        if unit_exists:
            update_list_entity(vehicles, wrecks, unit_id, unit_type, mass, pos, vel, extra, extra_2)
        else:
            add_entity_to_lists(vehicles, wrecks, unit_id, unit_type, player_id, mass, radius, pos, vel, extra, extra_2)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    for i in range(len(vehicles)):
        vehicles[i].update(wrecks, vehicles)

    print(p_vars.reaper_command)
    print(p_vars.destroyer_command)
    print(p_vars.doof_command)
