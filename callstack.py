from enum import Enum


class FrameType(Enum):
    PROGRAM = 'PROGRAM'
    PROCEDURE = 'PROCEDURE'
    FUNCTION = 'FUNCTION'


class Frame(object):
    def __init__(self, name: str, type: FrameType):
        self.enclosing_frame = None
        self.name = name
        self.type = type
        self.nesting_level = None
        self.return_val = None
        self.members = {}

    def define(self, key):
        self.members[key] = None

    def get_value(self, key):
        if key in self.members.keys():
            return self.members[key]
        elif self.enclosing_frame is not None:
            return self.enclosing_frame.get_value(key)
        else:
            raise Exception('undefined id: %s' % key)

    def set_value(self, key, value):
        if key in self.members.keys():
            self.members[key] = value
        elif self.enclosing_frame is not None:
            self.enclosing_frame.set_value(key, value)
        else:
            raise Exception('undefined id: %s' % key)

    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()


class CallStack(object):
    def __init__(self):
        self.__frames = []

    def push(self, frame: Frame):
        current_frame: Frame = self.peek()
        if current_frame is None:
            frame.nesting_level = 1
            frame.enclosing_frame = None
        else:
            frame.enclosing_frame = current_frame
            frame.nesting_level = current_frame.nesting_level + 1
        self.__frames.append(frame)

    def pop(self):
        self.__frames.pop()

    def peek(self):
        if len(self.__frames) is 0:
            return None
        return self.__frames[-1]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self.__frames))
        s = f'CALL STACK(memory contents):\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()
