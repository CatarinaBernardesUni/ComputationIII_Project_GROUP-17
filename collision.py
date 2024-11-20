# Testing at home: adding collision
def collision_test(rect, tiles):
    """
    this function is used to check if the player is colliding with a tile

    takes in the player rectangle and the tiles list
    """

    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    """
    this function is used to move the player

    takes in the player rectangle, the movement vector and the tiles list
    """

    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    # we handle tiles individually
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[0] > 0:  # moving right
            rect.right = tile.left  # the right side of the player is now the left side of the tile
            collision_types['right'] = True
        elif movement[0] < 0:  # moving left
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)

    for tile in hit_list:
        if movement[1] > 0:  # falling down
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:  # moving up
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types