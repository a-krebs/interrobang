import sys

OBJECT_FORMAT_STRING = "\
<object name=\"{obj_name}\">\n\
    <inherit name=\"editor_room\" />\n\
    <enter type=\"script\">\n\
        change_rooms\n\
    </enter>\n\
{obj_content}\n\
</object>\
"

EXIT_FORMAT_STRING = "\
    <exit alias=\"{room_alias}\" to=\"{exit_target}\">\n\
        <inherit name=\"{direction}direction\" />\n\
        <look type=\"script\">\n\
            look_room ({exit_target})\n\
        </look>\n\
    </exit>\
"

class Room(object):
    """
    Room that supports 4 exits.
    """


    def __init__(self, label):
        self.label = label
        self.exits = {
                        'north': None,
                        'east': None,
                        'south': None,
                        'west': None,
                    }


    def __str__(self):
        exits = []
        for k, v in self.exits.items():
            if v == None:
                continue

            e = EXIT_FORMAT_STRING.format(
                room_alias=k,
                exit_target=v.label,
                direction=k,
            )
            exits.append(e)

        str_rep = OBJECT_FORMAT_STRING.format(
            obj_name=self.label,
            obj_content="\n".join(exits)
        )

        return str_rep


def join_rooms(direction, room1, room2):
    def north(room1, room2):
        room1.exits['north'] = room2
        room2.exits['south'] = room1

    def east(room1, room2):
        room1.exits['east'] = room2
        room2.exits['west'] = room1

    def south(room1, room2):
        room1.exits['south'] = room2
        room2.exits['north'] = room1

    def west(room1, room2):
        room1.exits['west'] = room2
        room2.exits['east'] = room1

    options = {
        'north': north,
        'east': east,
        'south': south,
        'west': west,
    }

    return options[direction](room1, room2)


def get_adj_room_coords(direction, x, y):
    if direction == 'north':
        return (x,y-1)
    elif direction == 'east':
        return (x+1,y)
    elif direction == 'south':
        return (x,y+1)
    elif direction == 'west':
        return (x-1,y)
    else:
        return None


def build_room_matrix(prefix, width, height):
    m = list()
    dirs = {
        -1
    }
    # create rooms row by row
    for row in xrange(height):
        m.append(list())
        for col in xrange(width):
            m[row].append(Room(prefix + str(row) + str(col)))

    # link the rooms together
    for row in xrange(height):
        for col in xrange(width):
            for direction in ['north', 'east', 'south', 'west']:
                # the current room
                room1 = m[row][col]
                try:
                    # coordinates in m of the adj room in direction
                    adj_col, adj_row = get_adj_room_coords(direction, col, row)
                    # don't use negative indexes into lists
                    if adj_col < 0 or adj_row < 0:
                        #print "OB " + direction
                        continue
                    room2 = m[adj_row][adj_col]
                except:
                    #print "DNE " + direction
                    continue

                join_rooms(direction, room1, room2)

    return m


if __name__ == "__main__":
    """
    Output to stdout the text representation of a new set of rooms
    with the exits and function calls set up.
    """
    usage = "Usage: {} room_label width height".format(sys.argv[0])

    if len(sys.argv) != 4:
        print(usage)
        sys.exit()

    room_prefix = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    m = build_room_matrix(room_prefix, width, height)

    for l in m:
        for r in l:
            print(r)

    sys.exit()