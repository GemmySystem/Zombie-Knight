init python:

    import math
    import random
    import pygame

    class Vector:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        # Vector operator overloads
        def __add__(self, other):
            if isinstance(other, self.__class__):
                return Vector(self.x + other.x, self.y + other.y)
            return Vector(self.x + other, self.y + other)

        def __mul__(self, other):
            if isinstance(other, self.__class__):
                return Vector(self.x * other.x, self.y * other.y)
            return Vector(self.x * other, self.y * other)

        def __rmul__(self, other):
            return self.__mul__(other)

        def set(self, vec):
            self.x = vec.x
            self.y = vec.y


    class ZKSprite():
        """
        The base class for all sprites or tiles for Zombie Knight.

        Provides rendering and collision detection methods.
        """

        def __init__(self, width, height, x, y):
            """
            Arguments:

            width (int): How wide the sprite or tile is in pixels.

            height (int): How tall the sprite or tile is in pixels.

            x (int): X-axis coordinate of the top-left of this sprite or tile.

            y (int): Y-axis coordinate of the top-left of this sprite or tile.

            ...

            Attributes:
            -----------
            position : Vector
                The x and y Vector location of the sprite or tile.

            """
            self.width = width
            self.height = height
            self.position = Vector(x, y)

        def render(self, render, st, at):
            """
            Renders the sprite's image on the given displayable using Ren'Py's
            render methods.

            Arguments:

            render (renpy.Render): Ren'Py render object onto which this sprite
            will be rendered.

            st (float): Shown timebase in seconds.

            at (float): Animation timebase in seconds.
            """
            r = renpy.render(self.image, self.width, self.height, st, at)
            render.blit(r, (int(self.position.x), int(self.position.y)))
        
        def update(self):
            pass

        def is_colliding(self, other):
            """
            Tests whether this sprite is colliding with another.

            Arguments:

            other (ZKSprite): Other sprite to test for collision with.
            """
            return (
                self.position.x <= other.position.x + other.width and
                self.position.x + self.width >= other.position.x and
                self.position.y <= other.position.y + other.height and
                self.position.y + self.height >= other.position.y
            )


    class Tile(ZKSprite):
        """
        A static, collidable ZKSprite.
        """
        def __init__(self, x, y, image_int, main_tile_group, sub_tile_group=[]):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this tile.

            y (int): Y-axis coordinate of the top-left of this tile.

            image_int (int): An integer that defines the sprite used by this
            tile, e.g. 1: dirt and 2-5: platforms.

            main_tile_group (list): List of all the Tiles to be rendered.
            
            sub_tile_group (list): List of all the Tiles of this subtype, e.g.
            Platforms.
            """
            ZKSprite.__init__(self, 30, 30, x, y)

            # Load in the correct image and append it to the correct 
            # sub_tile_group

            # Dirt tiles
            if image_int == 1:
                self.image = Image("images/tiles/Tile (1).png")
            # Platform tiles
            elif image_int == 2:
                self.image = Image("images/tiles/Tile (2).png")
                sub_tile_group.append(self)
            elif image_int == 3:
                self.image = Image("images/tiles/Tile (3).png")
                sub_tile_group.append(self)
            elif image_int == 4:
                self.image = Image("images/tiles/Tile (4).png")
                sub_tile_group.append(self)
            elif image_int == 5:
                self.image = Image("images/tiles/Tile (5).png")
                sub_tile_group.append(self)

            # Add every tile to the main group
            main_tile_group.append(self)


    class ZKAnimated(ZKSprite):
        """
        An animated ZKSprite.
        """
        def __init__(self, width, height, x, y):
            ZKSprite.__init__(self, width, height, x, y)
    
        def generate_mirrored_animation(self, fname_pattern, start, end, step = 1):
            """
            Generates two mirrored lists of sprites based on files matching the
            given `fname_pattern` interpolated with numbers from `start` to
            `end` (inclusive) stepping by `step` at a time.

            For example, given the inputs `("hello_{}.png", 1, 5, 1)`, this
            method would attempt to load sprites for the following source image
            files:
            ```
            hello_1.png
            hello_2.png
            hello_3.png
            hello_4.png
            hello_5.png
            ```

            This function returns two lists, a righthand side and a lefthand
            side. The righthand list is the sprites loaded as-is, where the
            lefthand side is the x-axis inversion of the loaded sprites.

            Arguments:

            fname_pattern (str): Filename string pattern to be used with
            Python's string `format` function. This will be given a single int
            value from the range of numbers defined by `start`, `end`, and
            `step`.

            start (int): Starting index for the number series that will be
            generated from this value to `end`.

            end (int): Ending index for the number series that will be generated
            from `start` to this value.

            step (int): Step by which the number series from `start` to `end`
            will be generated.

            Returns:

            right_sprites (Displayable[]): Righthand side sprite list.

            left_sprites (Displayable[]): Lefthand side sprite list.
            """
            right_sprites = []
            left_sprites = []
            for i in range(start, end + 1 if step > 0 else end - 1, step):
                img = Image(fname_pattern.format(i))
                right_sprites.append(img)
                left_sprites.append(Transform(img, xzoom=-1.0))
            
            return (right_sprites, left_sprites)

        def generate_animation(self, fname_pattern, start, end, step = 1):
            """
            Generates a list of sprites based on files matching the
            given `fname_pattern` interpolated with numbers from `start` to
            `end` (inclusive) stepping by `step` at a time.

            For example, given the inputs `("hello_{}.png", 1, 5, 1)`, this
            method would attempt to load sprites for the following source image
            files:
            ```
            hello_1.png
            hello_2.png
            hello_3.png
            hello_4.png
            hello_5.png
            ```

            Arguments:

            fname_pattern (str): Filename string pattern to be used with
            Python's string `format` function. This will be given a single int
            value from the range of numbers defined by `start`, `end`, and
            `step`.

            start (int): Starting index for the number series that will be
            generated from this value to `end`.

            end (int): Ending index for the number series that will be generated
            from `start` to this value.

            step (int): Step by which the number series from `start` to `end`
            will be generated.

            Returns:

            sprites (Displayable[]): Sprite list.
            """
            sprites = []
            for i in range(start, end + 1 if step > 0 else end - 1, step):
                sprites.append(Image(fname_pattern.format(i)))
            return sprites
                

    class ZKPlayer(ZKAnimated):
        """
        It's the player!

        ...

        Attributes:
        -----------
        move_right_sprites : list
            List of sprites for the ZKPlayer's right movement animation.

        move_left_sprites : list
            List of sprites for the ZKPlayer's left movement animation.

        idle_right_sprites : list
            List of sprites for the ZKPlayer's idle animation while facing right.

        idle_left_sprites : list
            List of sprites for the ZKPlayer's idle animation while facing left.

        jump_right_sprites : list
            List of sprites for the ZKPlayer's animation while jumping right.

        jump_left_sprites : list
            List of sprites for the ZKPlayer's animation while jumping left.

        attack_right_sprites : list
            List of sprites for the ZKPlayer's animation while attacking right.

        attack_left_sprites : list
            List of sprites for the ZKPlayer's animation while attacking left.
        
        current_sprite_index : float
            Current frame index represented as a float, which is floored to get
            the frame to be rendered.

        image : Image
            Current frame to be rendered.
        
        platform_tiles : Tile[]
            List of platform Tiles used for collision detection.

        portal_group : Portal[]
            List of Portals used for collision detection.

        beam_group : Beam[]
            List of Beams into which "slash" sprites will be inserted.

        animate_jump : bool
            Whether jumping is being animated.

        animate_fire : bool
            Whether slashing is being animated.

        velocity : Vector
            Current player movement speed.

        acceleration : Vector
            Current change in player velocity.
        
        health : int
            ZKPlayer's health.

        starting_x : int
            ZKPlayer's starting x position. This value is used for resetting 
            the player sprite to the start location when necessary.

        starting_y : int
            ZKPlayer's starting y position. This value is used for resetting 
            the player sprite to the start location when necessary.
            
        """

        # Constant variables
        HORIZONTAL_ACCELERATION = 2  # Speed at which the player can move horizontally.
        HORIZONTAL_FRICTION = 0.15  # Amount the player is slowed down by friction.
        VERTICAL_ACCELERATION = 0.8  # Amount of gravity applied to the player.
        VERTICAL_JUMP_SPEED = 23  # Determines how high the player can jump.
        STARTING_HEALTH = 100  # Beginning amount of player health.

        def __init__(self, x, y, platform_tiles, portal_group, beam_group):
            ZKAnimated.__init__(self, 80, 118, x, y)

            # Generate pairs of sprite lists.
            self.move_right_sprites, self.move_left_sprites = self.generate_mirrored_animation("images/player/run/Run ({}).png", 1, 10)
            self.idle_right_sprites, self.idle_left_sprites = self.generate_mirrored_animation("images/player/idle/Idle ({}).png", 1, 10)
            self.jump_right_sprites, self.jump_left_sprites = self.generate_mirrored_animation("images/player/jump/Jump ({}).png", 1, 10)
            self.attack_right_sprites, self.attack_left_sprites = self.generate_mirrored_animation("images/player/attack/Attack ({}).png", 1, 10)

            # Reset current_sprite_index.
            self.current_sprite_index = 0

            # Render initial sprite, determined by referencing the idle right
            # sprite list using the current_sprite_index.
            self.image = self.idle_right_sprites[self.current_sprite_index]

            # Attach sprite groups.
            self.platform_tiles = platform_tiles
            self.portal_group = portal_group
            self.beam_group = beam_group

            # Set animation booleans.
            self.animate_jump = False
            self.animate_fire = False

            # Initialize kinematics vectors.
            self.velocity = Vector(0, 0)
            self.acceleration = Vector(0, self.VERTICAL_ACCELERATION)

            # Initialize player values.
            self.health = self.STARTING_HEALTH
            self.starting_x = x
            self.starting_y = y

        def update(self, keyboard, max_width, max_height, can_trigger_space_action, can_trigger_shift_action):
            """
            Updates the player by calling the move, check_collisions, and
            check_animations methods.

            Arguments:

            keyboard (dict): Boolean flags for the keyboard controls indicating
            whether they are currently pressed.

            max_width (int): Viewport width used for detecting when player
            has reached the right side of the screen.

            max_height (int): Viewport height used for detecting when player
            has entered portal on top or bottom of screen.

            can_trigger_space_action (bool): Boolean flag for whether player is
            able to trigger space action, e.g. jump.

            can_trigger_shift_action (bool): Boolean flag for whether player is
            able to trigger shift action, e.g. fire.
            """

            self.move(keyboard, max_width, can_trigger_space_action, can_trigger_shift_action)
            self.check_collisions(max_width, max_height)
            self.check_animations()

        def move(self, keyboard, max_width, can_trigger_space_action, can_trigger_shift_action):
            """
            Moves the player.

            ...

            Attributes:
            -----------
            velocity : Vector
                Current player movement speed.
                
            acceleration : Vector
                Current change in player velocity.

            position : Vector
                Current x and y location of player.
            """

            # Set the acceleration vector
            self.acceleration = Vector(0, self.VERTICAL_ACCELERATION)

            # If the user is pressing the left arrow key, set the x component of
            # the acceleration to be the value of the horizontal acceleration
            # constant variable inversed. Also animate the player to move left.
            if keyboard["left"]:
                self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
                self.animate(self.move_left_sprites, 0.5)

            # If the user is pressing the right arrow key, set the x component
            # of the acceleration to be the value of the horizontal acceleration
            # constant variable. Also animate the player to move right.
            elif keyboard["right"]:
                self.acceleration.x = self.HORIZONTAL_ACCELERATION
                self.animate(self.move_right_sprites, 0.5)

            # If the user is not pressing either the left or right arrow keys,
            # animate the player in their idle state facing either left or right
            # based on the player's x velocity.
            else:
                if self.velocity.x > 0:
                    self.animate(self.idle_right_sprites, 0.5)
                else:
                    self.animate(self.idle_left_sprites, 0.5)
            
            # If the user is pressing the spacebar and is allowed to trigger the
            # space action, this triggers the jump method.
            if keyboard["space"] and can_trigger_space_action:
                self.jump()

            # If the user is pressing the shift key and is allowed to trigger
            # the shift action, this triggers the fire method.
            if keyboard["shift"] and can_trigger_shift_action:
                self.fire()

            # Calculate new kinematics values based on displacement formulas.
            self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
            self.velocity += self.acceleration
            self.position += self.velocity + (0.5 * self.acceleration)

            # If the player's x position is off the screen to the left,
            # wrap-around movement to the right.
            if self.position.x < 0:
                self.position.x = max_width

            # If the player's x position is off the screen to the right,
            # wrap-around movement to the left.
            elif self.position.x > max_width:
                self.position.x = 0

        def check_collisions(self, max_width, max_height):
            """
            Check for collisions between the player and platforms and portals.
            """

            # Collision check between player and platforms when falling. If
            # player has collided, set y position to the position of the
            # platform's y position minus the player's height plus a small
            # buffer. Then reset the y velocity.
            if self.velocity.y > 0:
                for platform in self.platform_tiles:
                    if platform.is_colliding(self):
                        self.position.y = platform.position.y - self.height + 5
                        self.velocity.y = 0

            # Collision check between player and platform when jumping up. If
            # player has collided, reset the y velocity. Then while the player
            # is still colliding with the platform, increment the y position of
            # the player by one.
            if self.velocity.y < 0:
                for platform in self.platform_tiles:
                    if platform.is_colliding(self):
                        self.velocity.y = 0
                        while platform.is_colliding(self):
                            self.position.y += 1

            # Collision check between player and portals. If player has
            # collided, use renpy.sound.play to play a portal sound effect. Then
            # teleport the player to the top-left, top-right, bottom-left, or
            # bottom-right depending on the current position of the player on
            # the screen.
            for portal in self.portal_group:
                if portal.is_colliding(self):
                    renpy.sound.play("audio/zk_portal_sound.wav")
                    # Determine which portal you are moving to
                    # Left and right
                    if self.position.x > max_width // 2:
                        self.position.x = 150
                    else:
                        self.position.x = max_width - 150 - self.width
                    # Top and bottom
                    if self.position.y > max_height // 2:
                        self.position.y = 50
                    else:
                        self.position.y = max_height - 150 - self.height

        def check_animations(self):
            """
            Check to see if the jump or fire animations should run.
            """

            # If the player jump animation should be triggered, check the
            # x velocity of the player to determine whether to render the right-
            # or left-facing version of the jumping sprites.
            
            if self.animate_jump:
                if self.velocity.x > 0:
                    self.animate(self.jump_right_sprites, 0.1)
                else:
                    self.animate(self.jump_left_sprites, 0.1)

            # If the player fire animation should be triggered, check the
            # x velocity of the player to determine whether to render the right-
            # or left-facing version of the attacking sprites.
            if self.animate_fire:
                if self.velocity.x > 0:
                    self.animate(self.attack_right_sprites, 0.25)
                else:
                    self.animate(self.attack_left_sprites, 0.25)

        def jump(self):
            """
            Player jump upwards if on a platform.
            """

            # Collision check between player and platforms. If player has
            # collided, use renpy.sound.play to play a jumping sound effect.
            # Then set y velocity to the inverse of the vertical jump speed
            # constant variable. Finally, set the animate_jump bool to True.
            for platform in self.platform_tiles:
                if platform.is_colliding(self):
                    renpy.sound.play("audio/zk_jump_sound.wav")
                    self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
                    self.animate_jump = True

        def fire(self):
            """
            Player fires a beam from their sword.
            """

            # Use renpy.sound.play to play a slashing sound effect. Then create
            # a Beam object originating from the player, adding it to the beam
            # group for the purposes of later removal. Finally, set the
            # animate_fire bool to True.
            renpy.sound.play("audio/zk_slash_sound.wav")
            Beam(self.position.x + self.width / 2, self.position.y + self.height / 2, self.beam_group, self)
            self.animate_fire = True

        def reset(self):
            """
            Reset the player's velocity and position.
            """

            self.velocity = Vector(0, 0)
            self.position = Vector(self.starting_x, self.starting_y)

        def animate(self, sprite_list, speed):
            """
            Animate the player's actions.

            Arguments:

            sprite_list (Displayable[]): List of sprites to be rendered.

            speed (float): Speed at which the frames of the sprites should be
            animated.
            ...

            Attributes:
            -----------
            image : Image
                Current frame to be rendered, determined by referencing the
                sprite list using the current_sprite_index.
            """

            # If the current_sprite_index is less than the total length of the
            # current list of sprite frames minus one (because the index starts
            # at zero), increment the current_sprite_index by the speed of the
            # animation. Else, reset the current_sprite_index to zero.
            if self.current_sprite_index < len(sprite_list) - 1:
                self.current_sprite_index += speed
            else:
                self.current_sprite_index = 0

                # Once the current_sprite_index has been reset, if the jump
                # animation boolean has been triggered, make it False.
                if self.animate_jump:
                    self.animate_jump = False

                # Once the current_sprite_index has been reset, if the fire
                # animation boolean has been triggered, make it False.
                if self.animate_fire:
                    self.animate_fire = False

            self.image = sprite_list[int(self.current_sprite_index)]


    class Beam(ZKSprite):
        """
        A slash-type beam attack summoned by the player's fire action.
        """

        # Constant variables
        VELOCITY = 20  # Horizontal speed of Beams.
        RANGE = 500  # Horizontal area where Beams are allowed to exist.

        def __init__(self, x, y, beam_group, player):
            """
            Arguments:
            x (int): X-axis coordinate of the top-left of this Beam.

            y (int): Y-axis coordinate of the top-left of this Beam.

            beam_group (Beam[]): List of Beams into which "slash" sprites will
            be inserted.

            player (ZKPlayer): The player to which the Beam is attached and from
            whom the Beam is fired.

            """
            ZKSprite.__init__(self, 60, 60, x, y)

            # If player's x velocity is greater than zero, e.g. the player is
            # facing the right, render the right-facing Beam sprite. Else,
            # render the left-facing sprite and inverse the Beam velocity.
            if player.velocity.x > 0:
                self.image = Image("images/player/slash.png")
            else:
                self.image = Transform(Image("images/player/slash.png"), xzoom=-1.0)
                self.VELOCITY = -1 * self.VELOCITY

            # Store starting x position of the Beam. 
            self.starting_x = x

            # Attach sprite group.
            self.beam_group = beam_group

            # Add Beam to beam_group.
            beam_group.append(self)

        def update(self):
            """
            Updates the Beam by incrementing the x position by the velocity
            constant variable. Also removes the Beam from the beam_group if the
            x position of the Beam minus its starting x position is greater
            than the range constant variable.
            """

            # Move the Beam.
            self.position.x += self.VELOCITY

            # If the beam has passed the range, kill it.
            if abs(self.position.x - self.starting_x) > self.RANGE:
                self.beam_group.remove(self)


    class Zombie(ZKAnimated):
        """
        It's a zombie! This is the enemy of Zombie Knight.
        """

        # Constant variables
        VERTICAL_ACCELERATION = 3  # Amount of gravity applied to the Zombies.
        RISE_TIME = 2 # Seconds it takes for the Zombies to reanimate.

        def __init__(self, x, y, platform_tiles, portal_group, min_speed, max_speed):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this Zombie.

            y (int): Y-axis coordinate of the top-left of this Zombie.

            platform_tiles (Tile[]): List of platform Tiles used for collision
            detection.

            portal_group (Portal[]): List of Portals used for collision
            detection.

            min_speed (int): The minimum speed at which the Zombies can move.

            max_speed (int): The maximum speed at which the Zombies can move.

            ...

            Attributes:
            -----------
            gender : int
                A random integer, between 0 and 1, used to determine whether the
                Zombie sprite rendered is a boy or a girl.
            
            direction : int
                A random choice, either 1 or -1, used to determine whether the
                Zombie moves left or right.
            
            animate_death : bool
                Whether Zombie death is being animated.

            animate_rise : bool
                Whether Zombie reanimation is being animated.

            velocity : Vector
                Current Zombie movement speed, determined by direction times a
                random integer, between min_speed and max_speed.
                
            acceleration : Vector
                Current change in Zombie velocity.

            is_dead : bool
                Whether the Zombie is considered dead, the state in which it has
                been hit by a Beam but has not been jumped on to make it
                disappear.
            
            frame_count : int
                The number of frames that has passed 

            round_time : int

            """
            ZKAnimated.__init__(self, 120, 120, x, y)

            # Choose gender.
            gender = random.randint(0, 1)

            # Boy Zombie
            if gender == 0:
                self.walk_right_sprites, self.walk_left_sprites = self.generate_mirrored_animation("images/zombie/boy/walk/Walk ({}).png", 1, 10)
                self.die_right_sprites, self.die_left_sprites = self.generate_mirrored_animation("images/zombie/boy/dead/Dead ({}).png", 1, 10)
                self.rise_right_sprites, self.rise_left_sprites = self.generate_mirrored_animation("images/zombie/boy/dead/Dead ({}).png", 10, 1, -1)

            # Girl Zombie
            else:
                self.walk_right_sprites, self.walk_left_sprites = self.generate_mirrored_animation("images/zombie/girl/walk/Walk ({}).png", 1, 10)
                self.die_right_sprites, self.die_left_sprites = self.generate_mirrored_animation("images/zombie/girl/dead/Dead ({}).png", 1, 10)
                self.rise_right_sprites, self.rise_left_sprites = self.generate_mirrored_animation("images/zombie/girl/dead/Dead ({}).png", 10, 1, -1)

            # Choose direction.
            self.direction = random.choice([-1, 1])

            # Reset current_sprite_index.
            self.current_sprite_index = 0

            # If direction is equal to -1, the zombie is rendered walking left.
            # Else, the zombie is rendered walking right.
            if self.direction == -1:
                self.image = self.walk_left_sprites[self.current_sprite_index]
            else:
                self.image = self.walk_right_sprites[self.current_sprite_index]

            # Attach sprite groups.
            self.platform_tiles = platform_tiles
            self.portal_group = portal_group

            # Set animation booleans.
            self.animate_death = False
            self.animate_rise = False

            # Initialize kinematics vectors.
            self.velocity = Vector(self.direction * random.randint(min_speed, max_speed), 0)
            self.acceleration = Vector(0, self.VERTICAL_ACCELERATION)

            # Initialize zombie values.
            self.is_dead = False
            self.frame_count = 0
            self.round_time = 0

        def update(self, max_width, max_height):
            """
            Updates the zombie by calling the move, check_collisions, and
            check_animations methods. Also determines whether the zombie is
            considered to be in a dead state and when they should reanimate.
            """

            self.move(max_width)
            self.check_collisions(max_width, max_height)
            self.check_animations()

            # Determine when the zombie should rise from the dead by checking
            # the is_dead boolean flag and if it is set, incrementing
            # frame_count by one every update loop until sixty frames have
            # passed. This adds one to the round_time and when round_time equals
            # the same as the zombie's rise_time constant variable, the
            # animate_rise boolean flag is triggered and the
            # current_sprite_index is reset so the animation occurs properly.
            if self.is_dead:
                self.frame_count += 1
                if self.frame_count % 60 == 0:
                    self.round_time += 1
                    if self.round_time == self.RISE_TIME:
                        self.animate_rise = True
                        # When the zombie died, the image was kept as the last image.
                        # When it rises, we want to start at index 0 of our rise_sprite lists.
                        self.current_sprite_index = 0

        def move(self, max_width):
            """
            If the zombie is not dead, move it. If direction is -1, animate the
            zombie walking left. Else, animate the zombie walking right.
            """

            if not self.is_dead:
                if self.direction == -1:
                    self.animate(self.walk_left_sprites, 0.5)
                else:
                    self.animate(self.walk_right_sprites, 0.5)

                # Calculate new kinematics values based on displacement
                # formulas. We don't need to update the acceleration vector
                # because it never changes here.
                self.velocity += self.acceleration
                self.position += self.velocity + (0.5 * self.acceleration)

                # If the zombie's x position is off the screen to the left,
                # wrap-around movement to the right.
                if self.position.x < 0:
                    self.position.x = max_width

                # If the zombie's x position is off the screen to the right,
                # wrap-around movement to the left.
                elif self.position.x > max_width:
                    self.position.x = 0

        def check_collisions(self, max_width, max_height):
            """
            Check for collisions between the zombie and platforms and portals.
            """

            # Collision check between zombie and platforms when falling. If
            # zombie has collided, set y position to the position of the
            # platform's y position minus the zombie's height plus a small
            # buffer. Then reset the y velocity.
            for platform in self.platform_tiles:
                if platform.is_colliding(self):
                    self.position.y = platform.position.y - self.height + 5
                    self.velocity.y = 0

            # Collision check between zombie and portals. If zombie has
            # collided, use renpy.sound.play to play a portal sound effect. Then
            # teleport the zombie to the top-left, top-right, bottom-left, or
            # bottom-right depending on the current position of the zombie on
            # the screen.
            for portal in self.portal_group:
                if portal.is_colliding(self):
                    renpy.sound.play("audio/zk_portal_sound.wav")
                    # Determine which portal you are moving to
                    # Left and right
                    if self.position.x > max_width // 2:
                        self.position.x = 150
                    else:
                        self.position.x = max_width - 150 - self.width
                    # Top and bottom
                    if self.position.y > max_height // 2:
                        self.position.y = 50
                    else:
                        self.position.y = max_height - 150 - self.height

        def check_animations(self):
            """
            Check to see if the death or rise animations should run.
            """

            # If the zombie death animation should be triggered, check the
            # direction of the zombie to determine whether to render the right-
            # or left-facing version of the dying sprites.
            if self.animate_death:
                if self.direction == 1:
                    self.animate(self.die_right_sprites, 0.095)
                else:
                    self.animate(self.die_left_sprites,0.095)

            # If the zombie rise animation should be triggered, check the
            # direction of the zombie to determine whether to render the right-
            # or left-facing version of the reanimating sprites.
            if self.animate_rise:
                if self.direction == 1:
                    self.animate(self.rise_right_sprites, 0.095)
                else:
                    self.animate(self.rise_left_sprites, 0.095)

        def animate(self, sprite_list, speed):
            """
            Animate the zombie's actions.

            Arguments:

            sprite_list (Displayable[]): List of sprites to be rendered.

            speed (float): Speed at which the frames of the sprites should be
            animated.
            ...

            Attributes:
            -----------
            image : Image
                Current frame to be rendered, determined by referencing the
                sprite list using the current_sprite_index.
            """

            # If the current_sprite_index is less than the total length of the
            # current list of sprite frames minus one (because the index starts
            # at zero), increment the current_sprite_index by the speed of the
            # animation. Else, reset the current_sprite_index to zero.
            if self.current_sprite_index < len(sprite_list) - 1:
                self.current_sprite_index += speed
            else:
                self.current_sprite_index = 0

                # Once the current_sprite_index has been reset, if the death
                # animation boolean has been triggered, make it False and set
                # the current_sprite_index to the last frame of the death
                # animation.
                if self.animate_death:
                    self.current_sprite_index = len(sprite_list) - 1
                    self.animate_death = False

                # Once the current_sprite_index has been reset, if the
                # reanimation boolean has been triggered, make it False, as well
                # as setting the is_dead boolean to False and resetting the
                # frame_count and round_time to zero.
                if self.animate_rise:
                    self.animate_rise = False
                    self.is_dead = False
                    self.frame_count = 0
                    self.round_time = 0

            self.image = sprite_list[int(self.current_sprite_index)]


    class RubyMaker(ZKAnimated):
        """
        The transparent RubyMaker from which all Rubies are generated.
        """

        def __init__(self, x, y, main_tile_group):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this RubyMaker.

            y (int): Y-axis coordinate of the top-left of this RubyMaker.

            main_tile_group (list): List of all the Tiles and RubyMaker to be
            rendered.
            
            ...

            Attributes:
            -----------
            image : Image
                Current frame to be rendered, determined by referencing the
                sprite list using the current_sprite_index.
            """

            ZKAnimated.__init__(self, 60, 60, x, y)

            # Generate sprite list.
            self.ruby_sprites = self.generate_animation("images/ruby_maker/tile00{}.png", 0, 6)

            # Reset current_sprite_index.
            self.current_sprite_index = 0

            self.image = self.ruby_sprites[self.current_sprite_index]

            # Add RubyMaker to main tile group.
            main_tile_group.append(self)

        def update(self):
            """
            Updates the RubyMaker by calling the animate method.
            """

            self.animate(self.ruby_sprites, 0.25)

        def animate(self, sprite_list, speed):
            """
            Animate the RubyMaker.

            Arguments:

            sprite_list (Displayable[]): List of sprites to be rendered.

            speed (float): Speed at which the frames of the sprites should be
            animated.
            ...

            Attributes:
            -----------
            image : Image
                Current frame to be rendered, determined by referencing the
                sprite list using the current_sprite_index.
            """

            # If the current_sprite_index is less than the total length of the
            # current list of sprite frames minus one (because the index starts
            # at zero), increment the current_sprite_index by the speed of the
            # animation. Else, reset the current_sprite_index to zero.
            if self.current_sprite_index < len(sprite_list) - 1:
                self.current_sprite_index += speed
            else:
                self.current_sprite_index = 0

            self.image = sprite_list[int(self.current_sprite_index)]


    class Ruby(ZKAnimated):
        """
        The method of gaining points and health in the game.
        """

        # Constant variables
        VERTICAL_ACCELERATION = 3  # Amount of gravity applied to the Rubies.
        HORIZONTAL_VELOCITY = 5  # Horizontal speed of Rubies.

        def __init__(self, max_width, platform_tiles, portal_group):
            """
            Arguments:
            max_width (int): Viewport width used for detecting when the Ruby has
            reached the right side of the screen.

            platform_tiles (Tile[]): List of platform Tiles used for collision
            detection.

            portal_group (Portal[]): List of Portals used for collision
            detection.
            """
            ZKAnimated.__init__(self, 60, 60, max_width // 2, 100)

            # Generate sprite list.
            self.ruby_sprites = self.generate_animation("images/ruby/tile00{}.png", 0, 6)

            # Reset current_sprite_index.
            self.current_sprite_index = 0

            self.image = self.ruby_sprites[self.current_sprite_index]

            # Attach sprite groups.
            self.platform_tiles = platform_tiles
            self.portal_group = portal_group

            # Initialize kinematics vectors.
            self.velocity = Vector(random.choice([-1 * self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
            self.acceleration = Vector(0, self.VERTICAL_ACCELERATION)

        def update(self, max_width, max_height):
            """
            Updates the Ruby by calling the animate, move, and check_collisions
            methods.
            """

            self.animate(self.ruby_sprites, 0.25)
            self.move(max_width)
            self.check_collisions(max_width, max_height)

        def move(self, max_width):
            """
            Moves the ruby.
            """

            # Calculate new kinematics values based on displacement
            # formulas. We don't need to update the acceleration vector
            # because it never changes here.
            self.velocity += self.acceleration
            self.position += self.velocity + (0.5 * self.acceleration)

            # If the zombie's x position is off the screen to the left,
            # wrap-around movement to the right. Decrement y position to deal
            # with some positional wonkiness.
            if self.position.x < 0:
                self.position.x = max_width
                self.position.y -= 120

            # If the zombie's x position is off the screen to the right,
            # wrap-around movement to the left. Decrement y position to deal
            # with some positional wonkiness.
            elif self.position.x > max_width:
                self.position.x = 0
                self.position.y -= 120

        def check_collisions(self, max_width, max_height):
            """
            Check for collisions between the rubies and platforms and portals.
            """

            # Collision check between rubies and platforms when falling. If
            # the ruby has collided, set y position to the position of the
            # platform's y position minus the rubies's height plus a small
            # buffer. Then reset the y velocity.
            for platform in self.platform_tiles:
                if platform.is_colliding(self):
                    self.position.y = platform.position.y - self.height + 5
                    self.velocity.y = 0

            # Collision check between rubies and portals. If the ruby has
            # collided, use renpy.sound.play to play a portal sound effect. Then
            # teleport the rubies to the top-left, top-right, bottom-left, or
            # bottom-right depending on the current position of the rubies on
            # the screen.
            for portal in self.portal_group:
                if portal.is_colliding(self):
                    renpy.sound.play("audio/zk_portal_sound.wav")
                    # Determine which portal you are moving to
                    # Left and right
                    if self.position.x > max_width // 2:
                        self.position.x = 150
                    else:
                        self.position.x = max_width - 150 - self.width
                    # Top and bottom
                    if self.position.y > max_height // 2:
                        self.position.y = 50
                    else:
                        self.position.y = max_height - 150 - self.height

        def animate(self, sprite_list, speed):
            """
            Animate the Ruby.

            Arguments:

            sprite_list (Displayable[]): List of sprites to be rendered.

            speed (float): Speed at which the frames of the sprites should be
            animated.
            ...

            Attributes:
            -----------
            image : Image
                Current frame to be rendered, determined by referencing the
                sprite list using the current_sprite_index.
            """

            # If the current_sprite_index is less than the total length of the
            # current list of sprite frames minus one (because the index starts
            # at zero), increment the current_sprite_index by the speed of the
            # animation. Else, reset the current_sprite_index to zero.
            if self.current_sprite_index < len(sprite_list) - 1:
                self.current_sprite_index += speed
            else:
                self.current_sprite_index = 0

            self.image = sprite_list[int(self.current_sprite_index)]


    class Portal(ZKAnimated):
        """
        
        """
        def __init__(self, x, y, color, portal_group):
            ZKAnimated.__init__(self, 120, 120, x, y)

            # Animation frames
            self.portal_sprites = []

            # Portal animation
            if color == "green":
                # Green portal
                self.portal_sprites.append(Image("images/portals/green/tile000.png"))
                self.portal_sprites.append(Image("images/portals/green/tile001.png"))
                self.portal_sprites.append(Image("images/portals/green/tile002.png"))
                self.portal_sprites.append(Image("images/portals/green/tile003.png"))
                self.portal_sprites.append(Image("images/portals/green/tile004.png"))
                self.portal_sprites.append(Image("images/portals/green/tile005.png"))
                self.portal_sprites.append(Image("images/portals/green/tile006.png"))
                self.portal_sprites.append(Image("images/portals/green/tile007.png"))
                self.portal_sprites.append(Image("images/portals/green/tile008.png"))
                self.portal_sprites.append(Image("images/portals/green/tile009.png"))
                self.portal_sprites.append(Image("images/portals/green/tile010.png"))
                self.portal_sprites.append(Image("images/portals/green/tile011.png"))
                self.portal_sprites.append(Image("images/portals/green/tile012.png"))
                self.portal_sprites.append(Image("images/portals/green/tile013.png"))
                self.portal_sprites.append(Image("images/portals/green/tile014.png"))
                self.portal_sprites.append(Image("images/portals/green/tile015.png"))
                self.portal_sprites.append(Image("images/portals/green/tile016.png"))
                self.portal_sprites.append(Image("images/portals/green/tile017.png"))
                self.portal_sprites.append(Image("images/portals/green/tile018.png"))
                self.portal_sprites.append(Image("images/portals/green/tile019.png"))
                self.portal_sprites.append(Image("images/portals/green/tile020.png"))
                self.portal_sprites.append(Image("images/portals/green/tile021.png"))
            else:
                # Purple portal
                self.portal_sprites.append(Image("images/portals/purple/tile000.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile001.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile002.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile003.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile004.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile005.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile006.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile007.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile008.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile009.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile010.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile011.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile012.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile013.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile014.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile015.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile016.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile017.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile018.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile019.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile020.png"))
                self.portal_sprites.append(Image("images/portals/purple/tile021.png"))

            # Load an image
            self.current_sprite_index = random.randint(0, len(self.portal_sprites) - 1)
            self.image = self.portal_sprites[self.current_sprite_index]

            # Add to the portal group
            portal_group.append(self)

        def update(self):
            # Update the portal

            self.animate(self.portal_sprites, 0.2)

        def animate(self, sprite_list, speed):
            # Animate the portal
            if self.current_sprite_index < len(sprite_list) - 1:
                self.current_sprite_index += speed
            else:
                self.current_sprite_index = 0

            self.image = sprite_list[int(self.current_sprite_index)]


    class ZombieKnightDisplayable(renpy.Displayable):

        def __init__(self, player, zombie_group, platform_tiles, portal_group, beam_group, ruby_group, main_tile_group):

            renpy.Displayable.__init__(self)
            # Initialize the game

            # Set constant variables
            self.STARTING_ROUND_TIME = 30
            self.STARTING_ZOMBIE_CREATION_TIME = 5
            self.WINDOW_WIDTH = 1920
            self.WINDOW_HEIGHT = 1080

            # Set game values
            self.score = 0
            self.round_number = 1
            self.frame_count = 0
            self.round_time = self.STARTING_ROUND_TIME
            self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

            # Set displayables
            self.player = player
            self.zombie_group = zombie_group
            self.platform_tiles = platform_tiles
            self.portal_group = portal_group
            self.beam_group = beam_group
            self.ruby_group = ruby_group
            self.main_tile_group = main_tile_group

            self.pause_background = Solid("#000000", xsize=self.WINDOW_WIDTH, ysize=self.WINDOW_HEIGHT)
            self.pbx = 0
            self.pby = 0

            self.main_text = _("Zombie Knight")
            self.mtx = 0
            self.mty = self.WINDOW_HEIGHT / 2 - 100

            self.sub_text = _("Press Enter or Start to begin")
            self.stx = 0
            self.sty = self.WINDOW_HEIGHT / 2 + 100

            # The time of the past render-frame
            self.oldst = None

            self.keyboard = {"up": False, "down": False, "left": False, "right": False, "space": False, "shift": False, "enter": False}
            self.can_trigger_space_action = True
            self.can_trigger_shift_action = True
            self.is_paused = False
            
            self.lose = False

            return

        def render(self, width, height, st, at):
            # Draws the screen

            # The Render object we'll be drawing into
            r = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame
            if self.oldst is None:
                self.oldst = st

            dtime = st - self.oldst
            self.oldst = st
            
            # This draws the pause background
            def pause_background(pbx, pby):

                # Render the pause background
                pause_background = renpy.render(self.pause_background, width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                r.blit(pause_background, (int(pbx), int(pby)))
            
            # This draws the main text
            def main_text(mtx, mty):

                # Render the main text
                main_text = renpy.render(Fixed(Text(self.main_text, size=60, color="#00bf00", outlines=[ (4, "#007300", 0, 0) ], font="gui/font/Poultrygeist.ttf", xalign=0.5)), width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                r.blit(main_text, (int(mtx), int(mty)))
            
            # This draws the sub text
            def sub_text(stx, sty):

                # Render the sub text
                sub_text = renpy.render(Fixed(Text(self.sub_text, size=60, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Poultrygeist.ttf", xalign=0.5)), width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                r.blit(sub_text, (int(stx), int(sty)))

            if not self.is_paused:

                # Render the player
                self.player.update(self.keyboard, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.can_trigger_space_action, self.can_trigger_shift_action)
                self.player.render(r, st, at)

                self.can_trigger_space_action = False
                self.can_trigger_shift_action = False

                # Render the zombies
                for zombie in self.zombie_group:
                    zombie.update(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                    zombie.render(r, st, at)

                # Render the beams
                for beam in self.beam_group:
                    beam.update()
                    beam.render(r, st, at)

                # Render the rubies
                for ruby in self.ruby_group:
                    ruby.update(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                    ruby.render(r, st, at)

                # Render the portals
                for portal in self.portal_group:
                    portal.update()
                    portal.render(r, st, at)

                # Render the tiles
                for tile in self.main_tile_group:
                    tile.update()
                    tile.render(r, st, at)

                self.update()
            else:
                renpy.music.set_pause(True, channel="music")
                pause_background(self.pbx, self.pby)
                main_text(self.mtx, self.mty)
                sub_text(self.stx, self.sty)

                if self.keyboard["enter"]:
                    self.is_paused = False
                    renpy.music.set_pause(False, channel="music")

            renpy.redraw(self, 0)

            return r

        def event(self, ev, x, y, st):
            # Handles events

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    self.keyboard["up"] = True
                elif ev.key == pygame.K_DOWN:
                    self.keyboard["down"] = True
                elif ev.key == pygame.K_LEFT:
                    self.keyboard["left"] = True
                elif ev.key == pygame.K_RIGHT:
                    self.keyboard["right"] = True
                elif ev.key == pygame.K_SPACE:
                    self.keyboard["space"] = True
                    self.can_trigger_space_action = True
                elif ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                    self.keyboard["shift"] = True
                    self.can_trigger_shift_action = True
                elif ev.key == pygame.K_RETURN:
                    self.keyboard["enter"] = True
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_UP:
                    self.keyboard["up"] = False
                elif ev.key == pygame.K_DOWN:
                    self.keyboard["down"] = False
                elif ev.key == pygame.K_LEFT:
                    self.keyboard["left"] = False
                elif ev.key == pygame.K_RIGHT:
                    self.keyboard["right"] = False
                elif ev.key == pygame.K_SPACE:
                    self.keyboard["space"] = False
                elif ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                    self.keyboard["shift"] = False
                elif ev.key == pygame.K_RETURN:
                    self.keyboard["enter"] = False
            else:
                if renpy.map_event(ev, "pad_a_press"):
                    self.keyboard["space"] = True
                    self.can_trigger_space_action = True
                elif renpy.map_event(ev, "pad_a_release"):
                    self.keyboard["space"] = False

                if renpy.map_event(ev, "pad_b_press"):
                    self.keyboard["shift"] = True
                    self.can_trigger_shift_action = True
                elif renpy.map_event(ev, "pad_b_release"):
                    self.keyboard["shift"] = False

                if renpy.map_event(ev, "pad_start_press"):
                    self.keyboard["enter"] = True
                elif renpy.map_event(ev, "pad_start_release"):
                    self.keyboard["enter"] = False

                if renpy.map_event(ev, "pad_lefty_neg") or renpy.map_event(ev, "pad_righty_neg") or renpy.map_event(ev, "pad_dpup_press"):
                    self.keyboard["up"] = True
                elif ((renpy.map_event(ev, "pad_lefty_zero") or renpy.map_event(ev, "pad_righty_zero")) and self.keyboard["up"]) or renpy.map_event(ev, "pad_dpup_release"):
                    self.keyboard["up"] = False

                if renpy.map_event(ev, "pad_lefty_pos") or renpy.map_event(ev, "pad_righty_pos") or renpy.map_event(ev, "pad_dpdown_press"):
                    self.keyboard["down"] = True
                elif ((renpy.map_event(ev, "pad_lefty_zero") or renpy.map_event(ev, "pad_righty_zero")) and self.keyboard["down"]) or renpy.map_event(ev, "pad_dpdown_release"):
                    self.keyboard["down"] = False
            
                if renpy.map_event(ev, "pad_leftx_neg") or renpy.map_event(ev, "pad_rightx_neg") or renpy.map_event(ev, "pad_dpleft_press"):
                    self.keyboard["left"] = True
                elif ((renpy.map_event(ev, "pad_leftx_zero") or renpy.map_event(ev, "pad_rightx_zero")) and self.keyboard["left"]) or renpy.map_event(ev, "pad_dpleft_release"):
                    self.keyboard["left"] = False

                if renpy.map_event(ev, "pad_leftx_pos") or renpy.map_event(ev, "pad_rightx_pos") or renpy.map_event(ev, "pad_dpright_press"):
                    self.keyboard["right"] = True
                elif ((renpy.map_event(ev, "pad_leftx_zero") or renpy.map_event(ev, "pad_rightx_zero")) and self.keyboard["right"]) or renpy.map_event(ev, "pad_dpright_release"):
                    self.keyboard["right"] = False

            # Ensure the screen updates
            renpy.restart_interaction()

            # If the player loses, return it
            if self.lose:
                return self.lose
            else:
                raise renpy.IgnoreEvent()

        def update(self):
            # Update the game

            # Update the round time every second
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.round_time -= 1
                self.frame_count = 0

            self.check_collisions()
            self.add_zombie()
            self.check_round_completion()
            self.check_game_over()

        def add_zombie(self):
            #Add a zombie to the game
            
            # Check to add a zombie every second
            if self.frame_count % 60 == 0:
                # Only add a zombie if zombie creation time has passed
                if self.round_time % self.zombie_creation_time == 0:
                    zombie = Zombie(random.randint(100, self.WINDOW_WIDTH - 100), -100, self.platform_tiles, self.portal_group, self.round_number, 5 + self.round_number)
                    self.zombie_group.append(zombie)

        def check_collisions(self):
            #Check collisions that affect gameplay
            
            # See if any beam in the beam group hit a zombie in the zombie group
            for zombie in self.zombie_group:
                for beam in self.beam_group:
                    if zombie.is_colliding(beam):
                        renpy.sound.play("audio/zk_zombie_hit_sound.wav")
                        self.beam_group.remove(beam)
                        zombie.is_dead = True
                        zombie.animate_death = True

            # See if a player stomped a dead zombie to finish it or collided with a live zombie to take damage
            for zombie in self.zombie_group:
                if zombie.is_colliding(self.player):
                    # The zombie is dead
                    if zombie.is_dead:
                        renpy.sound.play("audio/zk_zombie_kick_sound.wav")
                        self.zombie_group.remove(zombie)
                        self.score += 25

                        ruby = Ruby(self.WINDOW_WIDTH, self.platform_tiles, self.portal_group)
                        self.ruby_group.append(ruby)

                    # The zombie isn't dead so take damage
                    else:
                        self.player.health -= 20
                        renpy.sound.play("audio/zk_player_hit_sound.wav")
                        # Move the player to not continually take damage
                        self.player.position.x -= 256 * zombie.direction
                        self.player.x = self.player.position.x

            # See if a player collided with a ruby
            for ruby in self.ruby_group:
                if self.player.is_colliding(ruby):
                    renpy.sound.play("audio/zk_ruby_pickup_sound.wav")
                    self.ruby_group.remove(ruby)
                    self.score += 100
                    self.player.health += 10
                    if self.player.health > self.player.STARTING_HEALTH:
                        self.player.health = self.player.STARTING_HEALTH

            # See if a living zombie collided with a ruby
            for zombie in self.zombie_group:
                for ruby in self.ruby_group:
                    if not zombie.is_dead:
                        if zombie.is_colliding(ruby):
                            self.ruby_group.remove(ruby)
                            renpy.sound.play("audio/zk_lost_ruby_sound.wav")
                            zombie = Zombie(random.randint(100, self.WINDOW_WIDTH - 100), -100, self.platform_tiles, self.portal_group, self.round_number, 5 + self.round_number)
                            self.zombie_group.append(zombie)
        
        def check_round_completion(self):
            # Check if the player survived a single night

            if self.round_time == 0:
                self.start_new_round()

        def check_game_over(self):
            # Check to see if the player lost the game

            if self.player.health <= 0:
                self.lose = True
                
                renpy.timeout(0)

        def start_new_round(self):
            # Start a new night

            self.round_number += 1

            # Decrease zombie creation time which means zombies are created faster
            if self.round_number < self.STARTING_ZOMBIE_CREATION_TIME:
                self.zombie_creation_time -= 1

            # Reset round values
            self.round_time = self.STARTING_ROUND_TIME

            self.zombie_group.clear()
            self.ruby_group.clear()
            self.beam_group.clear()

            self.player.reset()

            self.main_text = "You survived the night!"
            self.sub_text = "Press Enter or Start to continue"
            self.is_paused = True

        def reset_game(self):
            # Reset the game

            # Reset game values
            self.lose = False
            self.keyboard = {"up": False, "down": False, "left": False, "right": False, "space": False, "shift": False, "enter": False}
            self.can_trigger_space_action = True
            self.can_trigger_shift_action = True

            self.score = 0
            self.round_number = 1
            self.round_time = self.STARTING_ROUND_TIME
            self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

            # Reset the player
            self.player.health = self.player.STARTING_HEALTH
            self.player.reset()

            # Clear sprite groups
            self.zombie_group.clear()
            self.ruby_group.clear()
            self.beam_group.clear()


    def display_zk_score(st, at):
        return Text(_("Score: ") + "%d" % zombie_knight.score, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    def display_zk_health(st, at):
        return Text(_("Health: ") + "%d" % zombie_knight.player.health, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    def display_zk_round(st, at):
        return Text(_("Night: ") + "%d" % zombie_knight.round_number, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    def display_zk_time(st, at):
        return Text(_("Sunrise In: ") + "%d" % zombie_knight.round_time, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    # Create sprite groups
    my_main_tile_group = []
    my_platform_tiles = []

    my_beam_group = []

    my_zombie_group = []

    my_portal_group = []
    my_ruby_group = []


    # Create the tile map (0: no tile, 1: dirt, 2-5: platforms, 6: Ruby Maker, 7-8: portals, 9: player)
    tile_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 9, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # Generate Tile objects from the tile map
    # Loop through the 18 lists (rows) in the tile map (i moves us down the map)
    for i in range(len(tile_map)):
        # Loop through the 32 elements in a given list (columns) (j moves us across the map)
        for j in range(len(tile_map[i])):
            # Dirt tile
            if tile_map[i][j] == 1:
                Tile(j * 60, i * 60, 1, my_main_tile_group)
            # Platform tiles
            elif tile_map[i][j] == 2:
                Tile(j * 60, i * 60, 2, my_main_tile_group, my_platform_tiles)
            elif tile_map[i][j] == 3:
                Tile(j * 60, i * 60, 3, my_main_tile_group, my_platform_tiles)
            elif tile_map[i][j] == 4:
                Tile(j * 60, i * 60, 4, my_main_tile_group, my_platform_tiles)
            elif tile_map[i][j] == 5:
                Tile(j * 60, i * 60, 5, my_main_tile_group, my_platform_tiles)
            # Ruby Maker
            elif tile_map[i][j] == 6:
                RubyMaker(j * 60 - 30, i * 60, my_main_tile_group)
            # Portals
            elif tile_map[i][j] == 7:
                Portal(j * 60, i * 60, "green", my_portal_group)
            elif tile_map[i][j] == 8:
                Portal(j * 60, i * 60, "purple", my_portal_group)
            # Player
            elif tile_map[i][j] == 9:
                my_player = ZKPlayer(j * 60 - 60, i * 60 + 60, my_platform_tiles, my_portal_group, my_beam_group)

default zombie_knight = ZombieKnightDisplayable(my_player, my_zombie_group, my_platform_tiles, my_portal_group, my_beam_group, my_ruby_group, my_main_tile_group)

screen zombie_knight():

    add "images/zk_background.jpg"

    add zombie_knight

    if not zombie_knight.is_paused:
        add DynamicDisplayable(display_zk_score) xalign 0.0 xoffset 20 yalign 0.95
        add DynamicDisplayable(display_zk_health) xalign 0.0 xoffset 20 yalign 1.0

        text _("Zombie Knight"):
            xalign 0.5
            yalign 0.98
            size 60
            color "#00bf00"
            outlines [ (4, "#007300", 0, 0) ]
            font "gui/font/Poultrygeist.ttf"

        add DynamicDisplayable(display_zk_round) xalign 1.0 xoffset -20 yalign 0.95
        add DynamicDisplayable(display_zk_time) xalign 1.0 xoffset -20 yalign 1.0

label play_zombie_knight:

    window hide  # Hide the window and quick menu while in Zombie Knight
    $ quick_menu = False

    play music zk_background_music

    $ zombie_knight.reset_game()

    call screen zombie_knight

    $ quick_menu = True
    window auto

label zombie_knight_done:

    if persistent.zombie_knight_high_score >= zombie_knight.score:
        pass
    else:
        $ persistent.zombie_knight_high_score = zombie_knight.score

    "Score: [zombie_knight.score]\n\nHigh Score: [persistent.zombie_knight_high_score]"

    menu:
        "Would you like to play again?"

        "Yes.":
            jump play_zombie_knight

        "No.":
            return
