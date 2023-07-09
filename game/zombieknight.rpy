init python:

    import random
    import pygame

    class Vector:
        """
        It's a vector.  It's an x/y coordinate pair.  It's whatever you dream,
        baby.
        """

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

            st (float): Shown timebase in seconds. The shown timebase begins
            when this sprite is first shown on the screen.

            at (float): Animation timebase in seconds. The animation timebase
            begins when a sprite with the same tag was shown, without being
            hidden.
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


    class ZKTile(ZKSprite):
        """
        A static, collidable ZKSprite.
        """
        def __init__(self, x, y, image_int):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this tile.

            y (int): Y-axis coordinate of the top-left of this tile.

            image_int (int): An integer that defines the sprite used by this
            tile, e.g. 1: dirt and 2-5: platforms.

            misc_tiles (list): List of all the ZKTiles to be rendered.
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
            elif image_int == 3:
                self.image = Image("images/tiles/Tile (3).png")
            elif image_int == 4:
                self.image = Image("images/tiles/Tile (4).png")
            elif image_int == 5:
                self.image = Image("images/tiles/Tile (5).png")


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

        platform_tiles : ZKTile[]
            List of platform ZKTiles used for collision detection.

        portal_group : Portal[]
            List of Portals used for collision detection.

        beam_group : ZKBeam[]
            List of ZKBeams into which "slash" sprites will be inserted.

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

            keyboard (KeyboardInput): Keyboard controls indicator class which is
            used to track what keys are pressed.

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

        def move(self, keyboard: KeyboardInput, max_width, can_trigger_space_action, can_trigger_shift_action):
            """
            Moves the player.
            """

            # Set the acceleration vector
            self.acceleration = Vector(0, self.VERTICAL_ACCELERATION)

            # If the user is pressing the left arrow key, set the x component of
            # the acceleration to be the value of the horizontal acceleration
            # constant variable inversed. Also animate the player to move left.
            if keyboard.left:
                self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
                self.animate(self.move_left_sprites, 0.5)

            # If the user is pressing the right arrow key, set the x component
            # of the acceleration to be the value of the horizontal acceleration
            # constant variable. Also animate the player to move right.
            elif keyboard.right:
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
            if keyboard.space > 0 and can_trigger_space_action:
                self.jump()

            # If the user is pressing the shift key and is allowed to trigger
            # the shift action, this triggers the fire method.
            if keyboard.shift > 0 and can_trigger_shift_action:
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
            # a ZKBeam object originating from the player, adding it to the beam
            # group for the purposes of later removal. Finally, set the
            # animate_fire bool to True.
            renpy.sound.play("audio/zk_slash_sound.wav")
            ZKBeam(self.position.x + self.width / 2, self.position.y + self.height / 2, self.beam_group, self)
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


    class ZKBeam(ZKSprite):
        """
        A slash-type beam attack summoned by the player's fire action.
        """

        # Constant variables
        VELOCITY = 20  # Horizontal speed of ZKBeams.
        RANGE = 500  # Horizontal area where ZKBeams are allowed to exist.

        def __init__(self, x, y, beam_group, player):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this ZKBeam.

            y (int): Y-axis coordinate of the top-left of this ZKBeam.

            beam_group (ZKBeam[]): List of ZKBeams into which "slash" sprites will
            be inserted.

            player (ZKPlayer): The player to which the ZKBeam is attached and from
            whom the ZKBeam is fired.

            """
            ZKSprite.__init__(self, 60, 60, x, y)

            # If player's x velocity is greater than zero, e.g. the player is
            # facing the right, render the right-facing ZKBeam sprite. Else,
            # render the left-facing sprite and inverse the ZKBeam velocity.
            if player.velocity.x > 0:
                self.image = Image("images/player/slash.png")
            else:
                self.image = Transform(Image("images/player/slash.png"), xzoom=-1.0)
                self.VELOCITY = -1 * self.VELOCITY

            # Store starting x position of the ZKBeam.
            self.starting_x = x

            # Attach sprite group.
            self.beam_group = beam_group

            # Add ZKBeam to beam_group.
            beam_group.append(self)

        def update(self):
            """
            Updates the ZKBeam by incrementing the x position by the velocity
            constant variable. Also removes the ZKBeam from the beam_group if the
            x position of the ZKBeam minus its starting x position is greater
            than the range constant variable.
            """

            # Move the ZKBeam.
            self.position.x += self.VELOCITY

            # If the beam has passed the range, kill it.
            if abs(self.position.x - self.starting_x) > self.RANGE:
                self.beam_group.remove(self)


    class ZKZombie(ZKAnimated):
        """
        It's a zombie! This is the enemy of Zombie Knight.
        """

        # Constant variables
        VERTICAL_ACCELERATION = 3  # Amount of gravity applied to the ZKZombies.
        RISE_TIME = 2 # Seconds it takes for the ZKZombies to reanimate.

        def __init__(self, x, y, platform_tiles, portal_group, min_speed, max_speed):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this ZKZombie.

            y (int): Y-axis coordinate of the top-left of this ZKZombie.

            platform_tiles (ZKTile[]): List of platform ZKTiles used for collision
            detection.

            portal_group (Portal[]): List of Portals used for collision
            detection.

            min_speed (int): The minimum speed at which the ZKZombies can move.

            max_speed (int): The maximum speed at which the ZKZombies can move.

            ...

            Attributes:
            -----------
            gender : int
                A random integer, between 0 and 1, used to determine whether the
                ZKZombie sprite rendered is a boy or a girl. The  gender is
                purely decorative.

            direction : int
                A random choice, either 1 or -1, used to determine whether the
                ZKZombie moves left or right.

            animate_death : bool
                Whether ZKZombie death is being animated.

            animate_rise : bool
                Whether ZKZombie reanimation is being animated.

            velocity : Vector
                Current ZKZombie movement speed, determined by direction times a
                random integer, between `min_speed` and `max_speed`.

            acceleration : Vector
                Current change in ZKZombie velocity.

            is_dead : bool
                Whether the ZKZombie is considered dead, the state in which it
                has been hit by a ZKBeam but has not been jumped on to make it
                disappear.

            frames_dead : int
                The number of frames that have passed since this ZKZombie died.
                This value is used to keep track of when to increment
                `seconds_dead`.

            seconds_dead : int
                The number of seconds this zombie has been dead and on the
                ground. This value is used to determine when the zombie should
                reanimate.
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
            self.frames_dead = 0
            self.seconds_dead = 0

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
            # frames_dead by one every update loop until sixty frames have
            # passed. This adds one to the seconds_dead and when seconds_dead equals
            # the same as the zombie's rise_time constant variable, the
            # animate_rise boolean flag is triggered and the
            # current_sprite_index is reset so the animation occurs properly.
            if self.is_dead:
                self.frames_dead += 1
                if self.frames_dead % 60 == 0:
                    self.seconds_dead += 1
                    if self.seconds_dead == self.RISE_TIME:
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
                # frames_dead and seconds_dead to zero.
                if self.animate_rise:
                    self.animate_rise = False
                    self.is_dead = False
                    self.frames_dead = 0
                    self.seconds_dead = 0

            self.image = sprite_list[int(self.current_sprite_index)]


    class RubyMaker(ZKAnimated):
        """
        The transparent RubyMaker from which all Rubies are generated.
 
        ...

        Attributes:
        -----------
        rubymaker_sprites : Displayable[]
            Sprites for the ruby maker animation.

        current_sprite_index : int
            Index of the current sprite in the animation being rendered.        

        image : Image
            Current frame to be rendered, determined by referencing the
            sprite list using the current_sprite_index.
        """

        def __init__(self, x, y):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this RubyMaker.

            y (int): Y-axis coordinate of the top-left of this RubyMaker.
            """
            ZKAnimated.__init__(self, 60, 60, x, y)

            # Generate sprite list.
            self.rubymaker_sprites = self.generate_animation("images/ruby_maker/tile00{}.png", 0, 6)

            # Reset current_sprite_index.
            self.current_sprite_index = 0

            self.image = self.rubymaker_sprites[self.current_sprite_index]


        def update(self):
            """
            Updates the RubyMaker by calling the animate method.
            """

            self.animate(self.rubymaker_sprites, 0.25)

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

            platform_tiles (ZKTile[]): List of platform ZKTiles used for collision
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
        Responsible for teleporting the player, zombies, and rubies diagonally
        across the screen.
        """
        def __init__(self, x, y, color):
            """
            Arguments:

            x (int): X-axis coordinate of the top-left of this portal.

            y (int): Y-axis coordinate of the top-left of this portal.

            color (str): A string representing what color the portal should be.
            The color is purely decorative.
            """
            ZKAnimated.__init__(self, 120, 120, x, y)

            if color == "green":
                self.portal_sprites = self.generate_animation("images/portals/green/tile0{:02d}.png", 0, 21)
            else:  # purple
                self.portal_sprites = self.generate_animation("images/portals/purple/tile0{:02d}.png", 0, 21)

            # Set the current_sprite_index to a random integer from 0 to the
            # length of self.portal_sprites minus one. This is so the portals
            # start on a random frame and don't all animate in the exact same
            # way.
            self.current_sprite_index = random.randint(0, len(self.portal_sprites) - 1)

            self.image = self.portal_sprites[self.current_sprite_index]

        def update(self):
            """
            Update the portal by calling the animate method.
            """

            self.animate(self.portal_sprites, 0.2)

        def animate(self, sprite_list, speed):
            """
            Animate the portal.

            Arguments:

            sprite_list (Displayable[]): List of sprites to be rendered.

            speed (float): Speed at which the frames of the sprites should be
            animated.
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


    class KeyboardInput():
        def __init__(self):
            self.left = False
            self.right = False
            self.space = 0
            self.shift = 0
            self.enter = False
            self.escape = False


    class ZKDisplayable(renpy.Displayable):
        """
        The combined displayable and game class. This is the meat of
        Creator-Defined Displayables and what works together with all the other
        classes to make Zombie Knight work.

        ...

        Attributes:
        -----------
        score : int
            Points the player has earned.

        round_number : int
            Game round the player is currently on.

        frame_count : int
            Number of frames that have passed since the game started.

        round_time : int
            The number of seconds remaining in the current round.

        zombie_creation_interval : int
            Number of seconds between zombie spawns.  This number decreases with
            each round.

        player : ZKPlayer
            Player character.
        
        zombie_group : Zombie[]
            List of zombie instances currently in the game.
        
        platform_tiles : ZKTile[]
            List of platform tiles currently in the game.
        
        portal_group : Portal[]
            List of portals currently on the map.
        
        beam_group : ZKBeam[]
            List of ZKBeam instances (slash animations) currently being
            rendered.
        
        ruby_group : Ruby[]
            List of Ruby items currently spawned on the map.
        
        misc_tiles : ZKSprite[]
            List of all platform tiles, decorational tiles (dirt), and the ruby
            spawner.
        
        pause_background : Solid
            Background displayable for the pause screen when showing.

        main_text : str
            Title string for the game.
        
        mty : int|float
            Y-axis position of the main text.

        sub_text : str
            Subtitle string for the game.

        sty : int|float
            Y-axis position of the subtitle.

        keyboard : KeyboardInput
            Helper class for keeping track of the keyboard inputs that are
            currently being pressed/held.
        
        can_trigger_space_action : bool
            Whether the spacebar on-press action should fire. This is to prevent
            repeatedly firing the on-press action multiple times.
        
        can_trigger_shift_action : bool
            Whether the shift on-press action should fire. This is to prevent
            repeatedly firing the on-press action multiple times.

        is_paused : bool
            Boolean value tracking whether or not the game is being treated as
            "paused" and if behaviors associated with that, such as pausing the
            music and not rendering the objects, occur.
        
        lose : bool
            Boolean value tracking whether the player has lost the game.
        """

        # Constant variables
        STARTING_ROUND_TIME = 30  # Seconds until the round ends
        STARTING_ZOMBIE_CREATION_INTERVAL = 5  # Seconds between zombie spawns
        ZOMBIE_POINT_VALUE = 25 # Points that killing a zombie is worth
        RUBY_POINT_VALUE = 100  # Points that a Ruby is worth
        RUBY_HEALTH_VALUE = 10 # Health points that a Ruby restores
        WINDOW_WIDTH = 1920  # Viewport width
        WINDOW_HEIGHT = 1080  # Viewport width

        def __init__(self, player, zombie_group, platform_tiles, portal_group, beam_group, ruby_group, misc_tiles):
            renpy.Displayable.__init__(self)

            # Set game values
            self.score = 0
            self.round_number = 1
            self.frame_count = 0
            self.round_time = self.STARTING_ROUND_TIME
            self.zombie_creation_interval = self.STARTING_ZOMBIE_CREATION_INTERVAL

            # Set displayables
            self.player = player
            self.zombie_group = zombie_group
            self.platform_tiles = platform_tiles
            self.portal_group = portal_group
            self.beam_group = beam_group
            self.ruby_group = ruby_group
            self.misc_tiles = misc_tiles

            self.pause_background = Solid("#000000", xsize=self.WINDOW_WIDTH, ysize=self.WINDOW_HEIGHT)

            self.main_text = _("Zombie Knight")
            self.mty = self.WINDOW_HEIGHT / 2 - 100

            self.sub_text = _("Press Enter or Start to begin")
            self.sty = self.WINDOW_HEIGHT / 2 + 100

            self.keyboard = KeyboardInput()
            self.can_trigger_space_action = True
            self.can_trigger_shift_action = True
            self.is_paused = True

            self.lose = False

            return

        def render(self, width, height, st, at):
            """
            Renders the Displayables.

            Arguments:

            width (int): Width of the Displayable.

            height (int): Height of the Displayable.

            st (float): Shown timebase in seconds. The shown timebase begins
            when this displayable is first shown on the screen.

            at (float): Animation timebase in seconds. The animation timebase
            begins when an image with the same tag was shown, without being
            hidden.
            """

            # The renpy.Render object we'll be drawing into.
            r = renpy.Render(width, height)

            def pause_background():
                """
                Function for a rendering a pause background for the pause
                screen, which is also used as a title card.
                """

                # This causes a pause background to be rendered and a
                # renpy.Render object to be returned.
                pause_background = renpy.render(self.pause_background, width, height, st, at)

                # Blit the pause background to the renpy.Render object we're
                # creating.
                r.blit(pause_background, (0, 0))

            def main_text(mty):
                """
                Function for a rendering main text for the pause screen, which
                is also used as a title card.
                """
                
                # This causes main text to be rendered and a renpy.Render object
                # to be returned.
                main_text = renpy.render(Fixed(Text(self.main_text, size=60, color="#00bf00", outlines=[ (4, "#007300", 0, 0) ],
                            font="gui/font/Poultrygeist.ttf", xalign=0.5)), width, height, st, at)

                # Blit the main text to the renpy.Render object we're creating.
                r.blit(main_text, (0, int(mty)))

            def sub_text(sty):
                """
                Function for a rendering sub text for the pause screen, which
                is also used as a title card.
                """
                
                # This causes sub text to be rendered and a renpy.Render object
                # to be returned.
                sub_text = renpy.render(Fixed(Text(self.sub_text, size=60, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ],
                            font="gui/font/Poultrygeist.ttf", xalign=0.5)), width, height, st, at)

                # Blit the sub text to the renpy.Render object we're creating.
                r.blit(sub_text, (0, int(sty)))

            # If the game is not paused, play the music (actually unpausing it)
            # and update/render all Displayables.
            if not self.is_paused:

                # Unpause the music, if paused.
                renpy.music.set_pause(False, channel="music")

                # Update and render the player.
                self.player.update(self.keyboard, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.can_trigger_space_action, self.can_trigger_shift_action)
                self.player.render(r, st, at)

                # Set the key actions back to False so they don't trigger
                # continuously.
                self.can_trigger_space_action = False
                self.can_trigger_shift_action = False

                # Update and render the zombies.
                for zombie in self.zombie_group:
                    zombie.update(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                    zombie.render(r, st, at)

                # Update and render the beams.
                for beam in self.beam_group:
                    beam.update()
                    beam.render(r, st, at)

                # Update and render the rubies.
                for ruby in self.ruby_group:
                    ruby.update(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
                    ruby.render(r, st, at)

                # Update and render the portals.
                for portal in self.portal_group:
                    portal.update()
                    portal.render(r, st, at)

                # Update and render the platforms.
                for platform in self.platform_tiles:
                    platform.update()
                    platform.render(r, st, at)

                # Update and render the misc tiles.
                for misc_tile in self.misc_tiles:
                    misc_tile.update()
                    misc_tile.render(r, st, at)

                # Update the game's behind-the-scene mechanics every frame.
                self.update()

            # Else, if the game is paused, pause the music, stop rendering the
            # Displayables (pausing them in the state they were last left), and
            # display the pause background, main text, and sub text.
            else:
                renpy.music.set_pause(True, channel="music")
                pause_background()
                main_text(self.mty)
                sub_text(self.sty)
                
                # If the user presses Enter, unpause the game and music.
                if self.keyboard.enter:
                    self.is_paused = False
                    renpy.music.set_pause(False, channel="music")

            # Redraw the Displayables without delay.
            renpy.redraw(self, 0)

            # Return the renpy.Render object.
            return r

        def event(self, ev, x, y, st):
            """
            Handles input events.

            Arguments:

            ev (event): A pygame.event object.

            x (int): The x-coordinates of the event.

            y (int): The y-coordinates of the event.

            st (float): Shown timebase in seconds.

            """

            # If the user presses a key down.
            if ev.type == pygame.KEYDOWN:

                # If the key pressed is left, the left flag is triggered. What
                # occurs when that happens is handled elsewhere.
                if ev.key == pygame.K_LEFT:
                    self.keyboard.left = True

                # If the key pressed is right, the right flag is triggered. What
                # occurs when that happens is handled elsewhere.
                elif ev.key == pygame.K_RIGHT:
                    self.keyboard.right = True

                # If the key pressed is space, the space value increases by 1.
                # When and only when it equals 1, the can_trigger_space_action
                # flag is triggered. This was done to prevent the flag from
                # triggering multiple times when the space key is held down.
                # What occurs when the can_trigger_space_action flag is
                # triggered is handled elsewhere.
                elif ev.key == pygame.K_SPACE:
                    self.keyboard.space += 1
                    if self.keyboard.space == 1:
                        self.can_trigger_space_action = True

                # If the key pressed is shift, the shift value increases by 1.
                # When and only when it equals 1, the can_trigger_shift_action
                # flag is triggered. This was done to prevent the flag from
                # triggering multiple times when the shift key is held down.
                # What occurs when the can_trigger_shift_action flag is
                # triggered is handled elsewhere.
                elif ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                    self.keyboard.shift += 1
                    if self.keyboard.shift == 1:
                        self.can_trigger_shift_action = True

                # If the key pressed is enter, the enter flag is triggered. What
                # occurs when that happens is handled elsewhere.
                elif ev.key == pygame.K_RETURN:
                    self.keyboard.enter = True

                # If the key pressed is escape, the escape flag is triggered,
                # the is_paused flag inverses, and the main and sub text changes
                # to reflect the paused game's state.
                elif ev.key == pygame.K_ESCAPE:
                    self.keyboard.escape = True
                    self.is_paused = not self.is_paused
                    self.main_text = "You paused the game!"
                    self.sub_text = "Press Enter or Start to continue"
            
            # If the user lets go of a key.
            elif ev.type == pygame.KEYUP:

                # If the key let go is left, the left flag is made False.
                if ev.key == pygame.K_LEFT:
                    self.keyboard.left = False

                # If the key let go is right, the right flag is made False.
                elif ev.key == pygame.K_RIGHT:
                    self.keyboard.right = False
            
                # If the key let go is space, the space value is reset to zero.
                elif ev.key == pygame.K_SPACE:
                    self.keyboard.space = 0
                
                # If the key let go is shift, the shift value is reset to zero.
                elif ev.key == pygame.K_LSHIFT or ev.key == pygame.K_RSHIFT:
                    self.keyboard.shift = 0
                
                # If the key let go is enter, the enter flag is made False.
                elif ev.key == pygame.K_RETURN:
                    self.keyboard.enter = False
                
                # If the key let go is escape, the escape flag is made False.
                elif ev.key == pygame.K_ESCAPE:
                    self.keyboard.escape = False

            # If the user inputs on a controller.
            else:

                # If the input is pressing the A button, the space value
                # increases by 1. When and only when it equals 1, the
                # can_trigger_space_action flag is triggered. This was done to
                # prevent the flag from triggering multiple times when the A
                # button is held down. What occurs when the
                # can_trigger_space_action flag is triggered is handled
                # elsewhere.
                if renpy.map_event(ev, "pad_a_press"):
                    self.keyboard.space += 1
                    if self.keyboard.space == 1:
                        self.can_trigger_space_action = True

                # If the input is releasing the A button, the space value is
                # reset to zero.
                elif renpy.map_event(ev, "pad_a_release"):
                    self.keyboard.space = 0

                # If the input is pressing the B button, the shift value
                # increases by 1. When and only when it equals 1, the
                # can_trigger_shift_action flag is triggered. This was done to
                # prevent the flag from triggering multiple times when the B
                # button is held down. What occurs when the
                # can_trigger_shift_action flag is triggered is handled
                # elsewhere.
                if renpy.map_event(ev, "pad_b_press"):
                    self.keyboard.shift += 1
                    if self.keyboard.shift == 1:
                        self.can_trigger_shift_action = True

                # If the input is releasing the B button, the shift value is
                # reset to zero.
                elif renpy.map_event(ev, "pad_b_release"):
                    self.keyboard.shift = 0

                # If the input is pressing the back button, the enter flag is
                # triggered. What occurs when that happens is handled elsewhere.
                if renpy.map_event(ev, "pad_back_press"):
                    self.keyboard.enter = True

                # If the input is releasing the back button, the enter flag is
                # made False.
                elif renpy.map_event(ev, "pad_back_release"):
                    self.keyboard.enter = False

                # If the input is pressing the start button, the escape flag is
                # triggered, the is_paused flag inverses, and the main and sub
                # text changes to reflect the paused game's state.
                if renpy.map_event(ev, "pad_start_press"):
                    self.keyboard.escape = True
                    self.is_paused = not self.is_paused
                    self.main_text = "You paused the game!"
                    self.sub_text = "Press Enter or Start to continue"

                # If the input is releasing the start button, the escape flag is
                # made False.
                elif renpy.map_event(ev, "pad_start_release"):
                    self.keyboard.escape = False

                # If the input is pushing left on the D-pad or tilting leftwards
                # on the left or right analog sticks, the left flag is
                # triggered. What occurs when that happens is handled elsewhere.
                if renpy.map_event(ev, "pad_leftx_neg") or renpy.map_event(ev, "pad_rightx_neg") or renpy.map_event(ev, "pad_dpleft_press"):
                    self.keyboard.left = True

                # If the input is releasing left on the D-pad or releasing the 
                # the left or right analog sticks, the left flag is made False.
                elif ((renpy.map_event(ev, "pad_leftx_zero") or renpy.map_event(ev, "pad_rightx_zero")) and self.keyboard["left"]) or renpy.map_event(ev, "pad_dpleft_release"):
                    self.keyboard.left = False

                # If the input is pushing right on the D-pad or tilting
                # rightwards on the left or right analog sticks, the right flag
                # is triggered. What occurs when that happens is handled
                # elsewhere.
                if renpy.map_event(ev, "pad_leftx_pos") or renpy.map_event(ev, "pad_rightx_pos") or renpy.map_event(ev, "pad_dpright_press"):
                    self.keyboard.right = True

                # If the input is releasing right on the D-pad or releasing the 
                # the left or right analog sticks, the right flag is made False.
                elif ((renpy.map_event(ev, "pad_leftx_zero") or renpy.map_event(ev, "pad_rightx_zero")) and self.keyboard["right"]) or renpy.map_event(ev, "pad_dpright_release"):
                    self.keyboard.right = False

            # Ensure the screen updates by restarting the current interaction.
            # Among other things, this displays images added to the scene,
            # re-evaluates screens, and starts any queued transitions.
            renpy.restart_interaction()

            # If the player loses, return it.
            if self.lose:
                return self.lose

            # Else, if the player doesn't lose, just raises an exception that
            # causes Ren'Py to ignore the event.
            else:
                raise renpy.IgnoreEvent()

        def update(self):
            """
            Update the behind-the-scene mechanics.
            """

            # Update the round time every "second". Because it is inadvisable to
            # restrict FPS in Ren'Py, the amount of time that actually passes
            # may not actually be a second but this is a passable means of
            # tracking the passage of time. For every update loop, frame_count
            # is added to by one. When obstensibly sixty frames have passed,
            # round_time is subtracted to by one and frame_count is reset to
            # zero.
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.round_time -= 1
                self.frame_count = 0

            # Check for collisions, check if a zombie should be added, check if
            # the round is complete, and check for a game over.
            self.check_collisions()
            self.add_zombie()
            self.check_round_completion()
            self.check_game_over()

        def add_zombie(self):
            """
            Add a zombie to the game.
            """

            # When obstensibly sixty frames have passed, add a zombie to the
            # game.
            if self.frame_count % 60 == 0:
                # Only add a zombie if the zombie creation interval can be
                # divided from the round_time with nothing remaining. This
                # zombie will be created with a random gender, a random walking
                # direction, a randomized starting position, and a random speed.
                # Also add the zombie to the zombie group.
                if self.round_time % self.zombie_creation_interval == 0:
                    zombie = ZKZombie(random.randint(100, self.WINDOW_WIDTH - 100), -100, self.platform_tiles, self.portal_group, self.round_number, 5 + self.round_number)
                    self.zombie_group.append(zombie)

        def check_collisions(self):
            """
            Check collisions that affect gameplay.
            """

            # See if any zombie in the zombie group hit any beam in the beam
            # group. If so, play the zombie's slash hit sound and remove the
            # beam from the beam_group. Then kill the zombie and animate its
            # death.
            for zombie in self.zombie_group:
                for beam in self.beam_group:
                    if zombie.is_colliding(beam):
                        renpy.sound.play("audio/zk_zombie_hit_sound.wav")
                        self.beam_group.remove(beam)
                        zombie.is_dead = True
                        zombie.animate_death = True

            # See if a player stomped a dead zombie to finish it off or collided
            # with a live zombie to take damage.
            for zombie in self.zombie_group:
                if zombie.is_colliding(self.player):

                    # If the zombie is dead, play the kicking sound, remove the
                    # zombie from the zombie_group, add points to the player's
                    # score, and generate a ruby, adding it to the ruby group.
                    if zombie.is_dead:
                        renpy.sound.play("audio/zk_zombie_kick_sound.wav")
                        self.zombie_group.remove(zombie)
                        self.score += self.ZOMBIE_POINT_VALUE

                        ruby = Ruby(self.WINDOW_WIDTH, self.platform_tiles, self.portal_group)
                        self.ruby_group.append(ruby)

                    # If the zombie ism't dead, play the player getting hit
                    # sound, move the player so they do not continually take
                    # damage, and update the player's x-coordinates.
                    else:
                        self.player.health -= 20
                        renpy.sound.play("audio/zk_player_hit_sound.wav")
                        self.player.position.x -= 256 * zombie.direction
                        self.player.x = self.player.position.x

            # See if a player collided with a ruby. If so, play the ruby pickup
            # sound, remove the ruby from the ruby_group, add points to the
            # player's score, add value to the player's health, and if the
            # player's is higher than their starting amount of health, reset it
            # to their starting value.
            for ruby in self.ruby_group:
                if self.player.is_colliding(ruby):
                    renpy.sound.play("audio/zk_ruby_pickup_sound.wav")
                    self.ruby_group.remove(ruby)
                    self.score += self.RUBY_POINT_VALUE
                    self.player.health += self.RUBY_HEALTH_VALUE
                    if self.player.health > self.player.STARTING_HEALTH:
                        self.player.health = self.player.STARTING_HEALTH

            # See if a living zombie collided with a ruby. If so, play the lost
            # ruby sound, remove the ruby from the ruby_group, and create a
            # zombie. This zombie will be created with a random gender, a random
            # walking direction, a randomized starting position, and a random
            # speed based on the round number. Also add the zombie to the zombie
            # group.
            for zombie in self.zombie_group:
                for ruby in self.ruby_group:
                    if not zombie.is_dead:
                        if zombie.is_colliding(ruby):
                            renpy.sound.play("audio/zk_lost_ruby_sound.wav")
                            self.ruby_group.remove(ruby)
                            zombie = ZKZombie(random.randint(100, self.WINDOW_WIDTH - 100), -100, self.platform_tiles, self.portal_group, self.round_number, 5 + self.round_number)
                            self.zombie_group.append(zombie)

        def check_round_completion(self):
            """
            Check if the player survived a single night, i.e. the round is
            complete.
            """

            # If round_time has counted down to zero, start a new round.
            if self.round_time == 0:
                self.start_new_round()

        def check_game_over(self):
            """
            Check to see if the player lost the game.
            """

            # If the player's health has reached zero, set the lose flag to True
            # and cause an event to be generated immediately, ending the game.
            if self.player.health <= 0:
                
                self.lose = True

                renpy.timeout(0)

        def start_new_round(self):
            """
            Start a new night, i.e. a new round is begun.
            """

            # Increase the round_number by one.
            self.round_number += 1

            # If the round_number is lower than the
            # starting_zombie_creation_interval, decrease
            # zombie_creation_inverval which means zombies are created
            # faster.
            if self.round_number < self.STARTING_ZOMBIE_CREATION_INTERVAL:
                self.zombie_creation_interval -= 1

            # Reset round time.
            self.round_time = self.STARTING_ROUND_TIME

            # Clear zombie, ruby, and beam groups.
            self.zombie_group.clear()
            self.ruby_group.clear()
            self.beam_group.clear()

            # Reset the player's velocity and position.
            self.player.reset()

            # Set the main and subtext to display a congratulatory message and
            # pause the game.
            self.main_text = "You survived the night!"
            self.sub_text = "Press Enter or Start to continue"
            self.is_paused = True

        def reset_game(self):
            """
            Reset the game's behind-the-scene's mechanics. This is primarily
            used before starting a new game for the first time (or after playing
            again).
            """

            # Set the lose flag to False, the keyboard to a blank state of the
            # KeyboardInput object, and set the key actions as True.
            self.lose = False
            self.keyboard = KeyboardInput()
            self.can_trigger_space_action = True
            self.can_trigger_shift_action = True

            # Reset the score to zero, set the round_number back to one, set the
            # round_time to the starting_round_time constant variable, and the
            # zombie_creation_interval to the starting_zombie_creation_interval
            # constant variable.
            self.score = 0
            self.round_number = 1
            self.round_time = self.STARTING_ROUND_TIME
            self.zombie_creation_interval = self.STARTING_ZOMBIE_CREATION_INTERVAL

            # Reset the player's health to the starting_health constant variable
            # and reset the player's velocity and position.
            self.player.health = self.player.STARTING_HEALTH
            self.player.reset()

            # Clear zombie, ruby, and beam groups.
            self.zombie_group.clear()
            self.ruby_group.clear()
            self.beam_group.clear()

    # Create function for displaying dynamic Text object displaying the player's score.
    def display_zk_score(st, at):
        return Text(_("Score: ") + "%d" % zombie_knight.score, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    # Create function for displaying dynamic Text object displaying the player's health.
    def display_zk_health(st, at):
        return Text(_("Health: ") + "%d" % zombie_knight.player.health, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    # Create function for displaying dynamic Text object displaying the round number.
    def display_zk_round(st, at):
        return Text(_("Night: ") + "%d" % zombie_knight.round_number, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1

    # Create function for displaying dynamic Text object displaying the round time.
    def display_zk_time(st, at):
        return Text(_("Sunrise In: ") + "%d" % zombie_knight.round_time, size=40, color="#FFFFFF", outlines=[ (4, "#cccccc", 0, 0) ], font="gui/font/Pixel.ttf"), .1


    # Create list groups for holding the sprites.
    my_misc_tiles = []
    my_platform_tiles = []
    my_beam_group = []
    my_zombie_group = []
    my_portal_group = []
    my_ruby_group = []


    # Create the tile map using nested lists (0: no tile, 1: dirt, 2-5:
    # platforms, 6: ruby maker, 7-8: portals, 9: player)
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

    # Generate ZKTile objects from the tile map. Loop through the 18 lists (rows)
    # in the tile map (i moves us down the map).
    for i in range(len(tile_map)):

        # Loop through the 32 elements in a given list (columns) (j moves us
        # across the map).
        for j in range(len(tile_map[i])):

            # If the element is a 1 (dirt tile), create a dirt tile and append
            # it to my_misc_tiles.
            if tile_map[i][j] == 1:
                my_misc_tiles.append(ZKTile(j * 60, i * 60, 1))

            # If the element is a 2-5 (platform tile), create a platform tile
            # and append it to my_platform_tiles.
            elif tile_map[i][j] == 2:
                my_platform_tiles.append(ZKTile(j * 60, i * 60, 2))
            elif tile_map[i][j] == 3:
                my_platform_tiles.append(ZKTile(j * 60, i * 60, 3))
            elif tile_map[i][j] == 4:
                my_platform_tiles.append(ZKTile(j * 60, i * 60, 4))
            elif tile_map[i][j] == 5:
                my_platform_tiles.append(ZKTile(j * 60, i * 60, 5))

            # If the element is a 6 (ruby maker), create a ruby maker
            # and append it to my_misc_tiles.
            elif tile_map[i][j] == 6:
                my_misc_tiles.append(RubyMaker(j * 60 - 30, i * 60))

            # If the element is a 7-8 (portal), create a portal
            # and append it to my_portal_group.
            elif tile_map[i][j] == 7:
                my_portal_group.append(Portal(j * 60, i * 60, "green"))
            elif tile_map[i][j] == 8:
                my_portal_group.append(Portal(j * 60, i * 60, "purple"))

            # If the element is a 9 (player), create a player.
            elif tile_map[i][j] == 9:
                my_player = ZKPlayer(j * 60 - 60, i * 60 + 60, my_platform_tiles, my_portal_group, my_beam_group)


# Create the Zombie Knight Displayable that we'll be adding to a screen to play
# the game.
default zombie_knight = ZKDisplayable(my_player, my_zombie_group, my_platform_tiles, my_portal_group, my_beam_group, my_ruby_group, my_misc_tiles)


# Create the screen needed to display the Displayable so we can play the game.
screen zombie_knight():

    # Add the background to the game.
    add "images/zk_background.jpg"

    # Add the earlier created Displayable.
    add zombie_knight

    # If the game is not paused, add the player's score, the player's health,
    # the title of the game, the round number, and the round time.
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


# This is the label we call to play Zombie Knight.
label play_zombie_knight:

    # Hide the window and quick menu while in Zombie Knight.
    window hide
    $ quick_menu = False

    # Play the music for Zombie Knight.
    play music zk_background_music

    # Reset the values for Zombie Knight, whether this is the first time or
    # you're playing again.
    $ zombie_knight.reset_game()

    # Call the screen that contains the Zombie Knight Displayable, which will
    # hide when the game is lost and the event is timedout.
    call screen zombie_knight

    # Restore the window and quick menu while outside of Zombie Knight.
    $ quick_menu = True
    window auto


# This is the label that automatically comes up after completing a game of
# Zombie Knight.
label zombie_knight_done:

    # If the score is higher than the recorded high score, set the high score to
    # be the same as the new score.
    if zombie_knight.score >= persistent.zombie_knight_high_score:
        $ persistent.zombie_knight_high_score = zombie_knight.score

    # Display the latest score and high score.
    "Score: [zombie_knight.score]\n\nHigh Score: [persistent.zombie_knight_high_score]"

    # Ask the player if they'd like to play again.
    menu:
        "Would you like to play again?"

        # Jump to playing again, if so.
        "Yes.":
            jump play_zombie_knight

        # Return, ending the game, if not.
        "No.":
            return
