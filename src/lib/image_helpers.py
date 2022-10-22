from util import Counter, is_number


class SourceGif:
    def frame_at_index(self, frame):
        return self.frame_index_cache[int(frame) % self.total_frames]

    def __init__(self, image_sequence, frame_lengths=None):
        if is_number(frame_lengths):
            self.frame_lengths = [frame_lengths for _ in range(len(image_sequence))]
        else:
            self.frame_lengths = frame_lengths or [
                60 for _ in range(len(image_sequence))
            ]
            if not isinstance(self.frame_lengths, list):
                raise TypeError("frame_lengths must be a list or a number")

            if len(self.frame_lengths) != len(image_sequence):
                raise ValueError(
                    "frame_lengths must be the same length as image_sequence"
                )
        self.image_sequence = image_sequence
        self.total_frames = sum(self.frame_lengths)

        self.speed = 1

        self.frame_index_cache = [None for _ in range(self.total_frames)]

        g = 0
        for fi, fl in enumerate(self.frame_lengths):
            for i in range(fl):
                self.frame_index_cache[g] = self.image_sequence[fi]
                g += 1

    @property
    def instance(self):
        return Gif(self)


class IGif:
    def reset(self):
        raise NotImplementedError()

    @property
    def frame():
        raise NotImplementedError()

    def clone():
        raise NotImplementedError()


class Gif(IGif):
    def __init__(self, source):
        if not isinstance(source, SourceGif):
            raise TypeError("source must be a SourceGif")
        self.source = source
        self.speed = source.speed

        self.frame_index = Counter(source.total_frames)

    def reset(self):
        self.frame_index.counter = 0

    @property
    def image(self):
        return self.source.frame_at_index(self.frame_index)

    @property
    def frame(self):
        r = self.image

        self.frame_index += self.speed

        return r

    def clone(self):
        o = Gif(self.source)
        o.speed = self.speed
        return o


class Image(IGif):
    def __init__(self, image):
        if not isinstance(image, pygame.Surface):
            raise TypeError("image must be a pygame.Surface")

        self.image = image

    def reset(self):
        return

    @property
    def frame(self):
        return self.image

    def clone(self):
        # It is immutable anyway
        return self
