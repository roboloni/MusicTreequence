import io
import random
import string
import collections
from contextlib import contextmanager
import numpy as np
from copy import deepcopy


def to_MIDI_pitch(pitch):
    """map to midi pitch"""
    MIDI_pitch = {
        ",,,C": 0, ",,,,B#": 0, "C3": 0, "B#4": 0, ",,,C#": 1, ",,,Db": 1, "C#3": 1, "Db3": 1, ",,,D": 2, "D3": 2,
        ",,,D#": 3, ",,,Eb": 3, "D#3": 3, "Eb3": 3, ",,,E": 4, ",,,Fb": 4, "E3": 4, "Fb3": 4, ",,,F": 5, ",,,E#": 5,
        "F3": 5, "E#3": 5, ",,,F#": 6, ",,,Gb": 6, "F#3": 6, "Gb3": 6, ",,,G": 7, "G3": 7, ",,,G#": 8, ",,,Ab": 8,
        "G#3": 8, "Ab3": 8, ",,,A": 9, "A3": 9, ",,,A#": 10, ",,,Bb": 10, "A#3": 10, "Bb3": 10, ",,,B": 11,
        ",,Cb": 11, "B3": 11, "Cb2": 11, ",,C": 12, ",,,B#": 12, "C2": 12, "B#3": 12, ",,C#": 13, ",,Db": 13,
        "C#2": 13, "Db2": 13, ",,D": 14, "D2": 14, ",,D#": 15, ",,Eb": 15, "D#2": 15, "Eb2": 15, ",,E": 16,
        ",,Fb": 16, "E2": 16, "Fb2": 16, ",,F": 17, ",,E#": 17, "F2": 17, "E#2": 17, ",,F#": 18, ",,Gb": 18,
        "F#2": 18, "Gb2": 18, ",,G": 19, "G2": 19, ",,G#": 20, ",,Ab": 20, "G#2": 20, "Ab2": 20, ",,A": 21,
        "A2": 21, ",,A#": 22, ",,Bb": 22, "A#2": 22, "Bb2": 22, ",,B": 23, ",Cb": 23, "B2": 23, "Cb1": 23, ",C": 24,
        ",,B#": 24, "C1": 24, "B#2": 24, ",C#": 25, ",Db": 25, "C#1": 25, "Db1": 25, ",D": 26, "D1": 26, ",D#": 27,
        ",Eb": 27, "D#1": 27, "Eb1": 27, ",E": 28, ",Fb": 28, "E1": 28, "Fb1": 28, ",F": 29, ",E#": 29, "F1": 29,
        "E#1": 29, ",F#": 30, ",Gb": 30, "F#1": 30, "Gb1": 30, ",G": 31, "G1": 31, ",G#": 32, ",Ab": 32, "G#1": 32,
        "Ab1": 32, ",A": 33, "A1": 33, ",A#": 34, ",Bb": 34, "A#1": 34, "Bb1": 34, ",B": 35, "Cb": 35, "B1": 35,
        "Cb0": 35, "C": 36, ",B#": 36, "C0": 36, "B#1": 36, "C#": 37, "Db": 37, "C#0": 37, "Db0": 37, "D": 38,
        "D0": 38, "D#": 39, "Eb": 39, "D#0": 39, "Eb0": 39, "E": 40, "Fb": 40, "E0": 40, "Fb0": 40, "F": 41,
        "E#": 41, "F0": 41, "E#0": 41, "F#": 42, "Gb": 42, "F#0": 42, "Gb0": 42, "G": 43, "G0": 43, "G#": 44,
        "Ab": 44, "G#0": 44, "Ab0": 44, "A": 45, "A0": 45, "A#": 46, "Bb": 46, "A#0": 46, "Bb0": 46, "B": 47,
        "cb": 47, "B0": 47, "cb0": 47, "c": 48, "B#": 48, "c0": 48, "B#0": 48, "c#": 49, "db": 49, "c#0": 49,
        "db0": 49, "d": 50, "d0": 50, "d#": 51, "eb": 51, "d#0": 51, "eb0": 51, "e": 52, "fb": 52, "e0": 52,
        "fb0": 52, "f": 53, "e#": 53, "f0": 53, "e#0": 53, "f#": 54, "gb": 54, "f#0": 54, "gb0": 54, "g": 55,
        "g0": 55, "g#": 56, "ab": 56, "g#0": 56, "ab0": 56, "a": 57, "a0": 57, "a#": 58, "bb": 58, "a#0": 58,
        "bb0": 58, "b": 59, "cb'": 59, "b0": 59, "cb1": 59, "c'": 60, "b#": 60, "c1": 60, "b#0": 60, "c#'": 61,
        "db'": 61, "c#1": 61, "db1": 61, "d'": 62, "d1": 62, "d#'": 63, "eb'": 63, "d#1": 63, "eb1": 63, "e'": 64,
        "fb'": 64, "e1": 64, "fb1": 64, "f'": 65, "e#'": 65, "f1": 65, "e#1": 65, "f#'": 66, "gb'": 66, "f#1": 66,
        "gb1": 66, "g'": 67, "g1": 67, "g#'": 68, "ab'": 68, "g#1": 68, "ab1": 68, "a'": 69, "a1": 69, "a#'": 70,
        "bb'": 70, "a#1": 70, "bb1": 70, "b'": 71, "cb''": 71, "b1": 71, "cb2": 71, "c''": 72, "b#'": 72, "c2": 72,
        "b#1": 72, "c#''": 73, "db''": 73, "c#2": 73, "db2": 73, "d''": 74, "d2": 74, "d#''": 75, "eb''": 75,
        "d#2": 75, "eb2": 75, "e''": 76, "fb''": 76, "e2": 76, "fb2": 76, "f''": 77, "e#''": 77, "f2": 77,
        "e#2": 77, "f#''": 78, "gb''": 78, "f#2": 78, "gb2": 78, "g''": 79, "g2": 79, "g#''": 80, "ab''": 80,
        "g#2": 80, "ab2": 80, "a''": 81, "a2": 81, "a#''": 82, "bb''": 82, "a#2": 82, "bb2": 82, "b''": 83,
        "cb'''": 83, "b2": 83, "cb3": 83, "c'''": 84, "b#''": 84, "c3": 84, "b#2": 84, "c#'''": 85, "db'''": 85,
        "c#3": 85, "db3": 85, "d'''": 86, "d3": 86, "d#'''": 87, "eb'''": 87, "d#3": 87, "eb3": 87, "e'''": 88,
        "fb'''": 88, "e3": 88, "fb3": 88, "f'''": 89, "e#'''": 89, "f3": 89, "e#3": 89, "f#'''": 90, "gb'''": 90,
        "f#3": 90, "gb3": 90, "g'''": 91, "g3": 91, "g#'''": 92, "ab'''": 92, "g#3": 92, "ab3": 92, "a'''": 93,
        "a3": 93, "a#'''": 94, "bb'''": 94, "a#3": 94, "bb3": 94, "b'''": 95, "cb''''": 95, "b3": 95, "cb4": 95,
        "c''''": 96, "b#'''": 96, "c4": 96, "b#3": 96, "c#''''": 97, "db''''": 97, "c#4": 97, "db4": 97,
        "d''''": 98, "d4": 98, "d#''''": 99, "eb''''": 99, "d#4": 99, "eb4": 99, "e''''": 100, "fb''''": 100,
        "e4": 100, "fb4": 100, "f''''": 101, "e#''''": 101, "f4": 101, "e#4": 101, "f#''''": 102, "gb''''": 102,
        "f#4": 102, "gb4": 102, "g''''": 103, "g4": 103, "g#''''": 104, "ab''''": 104, "g#4": 104, "ab4": 104,
        "a''''": 105, "a4": 105, "a#''''": 106, "bb''''": 106, "a#4": 106, "bb4": 106, "b''''": 107, "cb'''''": 107,
        "b4": 107, "cb5": 107, "c'''''": 108, "b#''''": 108, "c5": 108, "b#4": 108, "c#'''''": 109, "db'''''": 109,
        "c#5": 109, "db5": 109, "d'''''": 110, "d5": 110, "d#'''''": 111, "eb'''''": 111, "d#5": 111, "eb5": 111,
        "e'''''": 112, "fb'''''": 112, "e5": 112, "fb5": 112, "f'''''": 113, "e#'''''": 113, "f5": 113, "e#5": 113,
        "f#'''''": 114, "gb'''''": 114, "f#5": 114, "gb5": 114, "g'''''": 115, "g5": 115, "g#'''''": 116,
        "ab'''''": 116, "g#5": 116, "ab5": 116, "a'''''": 117, "a5": 117, "a#'''''": 118, "bb'''''": 118,
        "a#5": 118, "bb5": 118, "b'''''": 119, "cb''''''": 119, "b5": 119, "cb6": 119, "c''''''": 120,
        "b#'''''": 120, "c6": 120, "b#5": 120, "c#''''''": 121, "db''''''": 121, "c#6": 121, "db6": 121,
        "d''''''": 122, "d6": 122, "d#''''''": 123, "eb''''''": 123, "d#6": 123, "eb6": 123, "e''''''": 124,
        "fb''''''": 124, "e6": 124, "fb6": 124, "f''''''": 125, "e#''''''": 125, "f6": 125, "e#6": 125,
        "f#''''''": 126, "gb''''''": 126, "f#6": 126, "gb6": 126, "g''''''": 127, "g6": 127
    }
    if isinstance(pitch, (int, np.int_)):
        return int(pitch)
    elif isinstance(pitch, str):
        try:
            pitch = int(pitch)
        except ValueError:
            return MIDI_pitch[pitch]
        return pitch
    else:
        raise UserWarning("Cannot interpret '{}' (type {}) as pitch".format(pitch, type(pitch)))


@contextmanager
def transposed(event, transpose_event):
    event._transpose_list += [(transpose_event._transpose, transpose_event._tonic, transpose_event._scale)]
    event._transpose_list += transpose_event._transpose_list
    yield
    event._transpose_list = event._transpose_list[:-1-len(transpose_event._transpose_list)]


def metrical_grid(nested_idx):
    """
    Returns the depth inside the metrical grid
    :param nested_idx: nested index on grid levels
    :return: depth

    For a 4/4 measure:
    |
    |       |
    |   |   |   |
    | | | | | | | |
    0 3 2 3 1 3 2 3 (depth)
    -----------------------
    0 0 0 0 0 0 0 0 (nested
    0 0 0 0 1 1 1 1  ...
    0 0 1 1 0 0 1 1  ...
    0 1 0 1 0 1 0 1  index)

    For a 12/8 measure:
    |
    |           |
    |     |     |     |
    | | | | | | | | | | | |
    0 3 3 2 3 3 1 3 3 2 3 3 (depth)
    -------------------------------
    0 0 0 0 0 0 0 0 0 0 0 0 (nested
    0 0 0 0 0 0 1 1 1 1 1 1  ...
    0 0 0 1 1 1 0 0 0 1 1 1  ...
    0 1 2 0 1 2 0 1 2 0 1 2  index)
    """
    idx = 0
    for idx, n_idx in reversed(list(enumerate(nested_idx))):
        if n_idx > 0:
            break
    return idx


class Scale(object):

    def __init__(self, intervals=range(12), pitches=None):
        if pitches is not None:
            intervals = [(to_MIDI_pitch(p) - to_MIDI_pitch(pitches[0])) % 12 for p in pitches]
        self._intervals = np.array(sorted(np.unique(intervals)))
        if self._intervals[0] < 0:
            raise UserWarning("Scale cannot contain negative intervals.")
        if self._intervals[-1] > 11:
            raise UserWarning("Scale cannot contain intervals of an octave or above.")

    def __str__(self):
        return str(self._intervals)

    def get_interval(self, scale_degree):
        return self._intervals[scale_degree % len(self._intervals)] + 12 * (scale_degree // len(self._intervals))

    def get_scale_degree(self, pitch, tonic):
        return np.argmin((self._intervals + to_MIDI_pitch(tonic) - to_MIDI_pitch(pitch)) % 12)


class Event(object):

    _indent = 0
    _beat = 1
    _symbols = {}
    _loops = set()
    _str_verbose = True

    @staticmethod
    def write_indent(file):
        for _ in range(Event._indent):
            print("  ", end="", file=file)

    @staticmethod
    def time_interval(extent):
        if isinstance(extent, str):
            if extent.endswith("sec"):
                # sec
                return float(extent[:-3])
            elif extent.endswith("ms"):
                # ms --> sec
                return float(extent[:-2])/1000
            elif extent.endswith("b"):
                # beats --> sec
                return float(extent[:-1]) * Event._beat
            elif '/' in extent:
                # x/y --> sec [1/4 = 1 beat]
                parts = extent.split('/')
                return 4 * float(parts[0]) / float(parts[1]) * Event._beat
            else:
                # --> sec
                return float(extent)
        else:
            # return as is
            return extent

    @staticmethod
    def set_beat(beat):
        if isinstance(beat, str):
            if beat.endswith('bpm'):
                Event._beat = float(60 / float(beat[:-3]))
            else:
                Event._beat = float(beat)
        else:
            Event._beat = beat

    @staticmethod
    def random_string(length=10, lower=True, upper=False, digits=False):
        pool = ''
        if lower:
            pool += string.ascii_lowercase
        if upper:
            pool += string.ascii_uppercase
        if digits:
            pool += string.digits
        return ''.join(random.choices(pool, k=length))

    @staticmethod
    def write_symbols(file):
        print("# symbols", file=file)
        print("", file=file)
        for function_name, function, extent in Event._symbols.values():
            print(function, file=file)
            print("", file=file)

    @staticmethod
    def write_loops(file):
        print("# function for testing infinite loops", file=file)
        print("def loop_test(key)", file=file)
        print("  loops = [", file=file)
        for name in Event._loops:
            print("    '{}',".format(name), file=file)
        print("  ].to_set", file=file)
        print("  return loops.include?(key)", file=file)
        print("end", file=file)

    @staticmethod
    def add_loop(name):
        if name in Event._loops:
            raise UserWarning("Loop '{}' already exists".format(name))
        else:
            Event._loops.add(name)

    @staticmethod
    def parse_events(event, agglomeration_type="Sequence"):
        if isinstance(event, str):
            # string should be single event or sequence of events separated by whitespace
            list = event.split()
            if len(list) > 1:
                # sequence
                sequence = []
                for e in list:
                    sequence.append(Event.parse_events(e))
                if agglomeration_type == "Sequence":
                    return Sequence(sequence)
                elif agglomeration_type == "Parallel":
                    return Parallel(sequence)
                else:
                    raise UserWarning("Unknown agglomeration type {}".format(agglomeration_type))
            else:
                # single event
                vals = event.split('/')
                length = "1b"
                if len(vals) > 1:
                    length = "1/" + vals[1]
                if vals[0] == 'r' or vals[0] == 'R':
                    return Rest(length)
                else:
                    pitch = vals[0]
                    tie = False
                    staccato = False
                    while pitch.endswith("_") or pitch.endswith("."):
                        if pitch.endswith("_"):
                            pitch = pitch[:-1]
                            tie = True
                        if pitch.endswith("."):
                            pitch = pitch[:-1]
                            staccato = True
                    return Tone(pitch=pitch, duration=length, tie=tie, staccato=staccato)
        else:
            # just pass through
            return event

    @staticmethod
    def wait(time, file):
        Event.write_indent(file=file)
        print("sleep {}".format(time), file=file)

    def __init__(self, transpose=0, tonic=0, scale=Scale()):
        self._transpose = transpose
        self._tonic = tonic
        self._scale = scale
        self._transpose_list = []

    def create_symbol(self, symbol, random_name=False):
        function_name = Event.random_string() if random_name else "function_"+symbol
        with io.StringIO() as file:
            old_indent = Event._indent
            print("def {} # {}".format(function_name, symbol), file=file)
            Event._indent = 1
            self.write(file)
            print("end", end='', file=file)
            Event._indent = old_indent
            Event._symbols[symbol] = (function_name, file.getvalue(), self.extent())

    def transpose(self, trp):
        if self.is_transposable():
            self._transpose = trp
        return self

    def is_atomic(self):
        return False

    def is_transposable(self):
        return False

    def extent(self):
        return 0

    def write(self, file):
        pass


class Chord(Event):

    def __init__(self,
                 intervals,
                 base,
                 duration='1/4',
                 extent=None,
                 amplitude=1.,
                 symbol=None,
                 tie=False,
                 staccato=False,
                 transpose=0,
                 tonic=0,
                 scale=Scale()):
        super(Chord, self).__init__(transpose=transpose, tonic=tonic, scale=scale)
        self._intervals = list(sorted(intervals))
        self._octaves = 1 + (max(self._intervals) - min(self._intervals)) // 12
        self._base = base
        self._duration = duration
        self._extent = duration if extent is None else extent
        self._amplitude = amplitude
        self._tie = tie
        self._staccato = staccato
        if symbol is not None:
            self.create_symbol(symbol)

    def __str__(self):
        if Event._str_verbose:
            return "Chord({}[{}]/{}+{}{}{} {}|{} {})".format(tuple(self._intervals),
                                                             self._octaves,
                                                             self._base,
                                                             self._transpose,
                                                             ("_" if self._tie else ""),
                                                             ("." if self._staccato else ""),
                                                             self._duration,
                                                             self._extent,
                                                             self._amplitude)
        else:
            return "{}/{}+{}:{}".format(tuple(self._intervals),
                                        self._base,
                                        self._transpose,
                                        self._duration)

    def rotate(self, n):
        self._intervals = self._intervals[n:] + [i + 12 * self._octaves for i in self._intervals[:n]]
        return self

    def is_atomic(self):
        return True

    def is_transposable(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file):
        transpose_list = [(self._transpose, self._tonic, self._scale)] + self._transpose_list
        duration = Event.time_interval(self._duration)
        if self._staccato:
            duration = 0.01
        for interval in self._intervals:
            pitch = to_MIDI_pitch(self._base) + interval
            for transpose, tonic, scale in transpose_list:
                scale_degree = scale.get_scale_degree(pitch=pitch, tonic=tonic)
                pitch -= scale.get_interval(scale_degree=scale_degree)
                pitch += scale.get_interval(scale_degree=scale_degree + transpose)
            Event.write_indent(file)
            print("tone pitch: {}, duration: {}, amp: {}".format(pitch, duration, self._amplitude), file=file)


class Tone(Chord):

    def __init__(self, pitch,
                 duration='1/4',
                 extent=None,
                 amplitude=1.,
                 symbol=None,
                 tie=False,
                 staccato=False,
                 transpose=0,
                 tonic=0,
                 scale=Scale()):
        super(Tone, self).__init__(base=pitch,
                                   intervals=[0],
                                   duration=duration,
                                   extent=extent,
                                   amplitude=amplitude,
                                   symbol=symbol,
                                   tie=tie,
                                   staccato=staccato,
                                   transpose=transpose)

    def __str__(self):
        if Event._str_verbose:
            return Chord.__str__(self)
        else:
            return "{}+{}:{}".format(self._base,
                                     self._transpose,
                                     self._duration)


class Beat(Event):

    def __init__(self, extent=0., amplitude=1., symbol=None):
        super(Beat, self).__init__(transpose=0, tonic=0, scale=Scale())
        self._extent = extent
        self._amplitude = amplitude
        if symbol is not None:
            self.create_symbol(symbol)

    def __str__(self):
        return "beat:{}:{}".format(self._extent, self._amplitude)

    def is_atomic(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file):
        Event.write_indent(file)
        print("play_beat amp: {}".format(self._amplitude), file=file)


class Rest(Event):
    def __init__(self, extent, symbol=None):
        super(Rest, self).__init__(transpose=0, tonic=0, scale=Scale())
        self._extent = extent
        if symbol is not None:
            self.create_symbol(symbol)

    def __str__(self):
        return "r:{}".format(self._extent)

    def is_atomic(self):
        return True

    def extent(self):
        return Event.time_interval(self._extent)

    def write(self, file):
        pass


class Sequence(Event):

    # WARNING!!! There is a bug, this only works once. Consider this code:
    # x = ["a", "b", "c"]
    # for x in Sequence.flatten(x):
    #     print(x)
    # for x in Sequence.flatten(x):
    #     print(x)
    # for x in Sequence.flatten(x):
    #     print(x)
    @staticmethod
    def flatten(sequence):
        for event in sequence:
            if isinstance(event, collections.Iterable) and not isinstance(event, (str, bytes)):
                yield from Sequence.flatten(event)
            elif isinstance(event, Sequence):
                yield from event._sequence
            else:
                yield event

    def __init__(self, sequence, symbol=None, transpose=0, tonic=0, scale=Scale(), make_deepcopy=True):
        super(Sequence, self).__init__(transpose=transpose, tonic=tonic, scale=scale)
        # self._sequence = Sequence.flatten(sequence) # this triggers the bug from above on multiple iterations through sequence
        self._sequence = list(Sequence.flatten(sequence))
        if make_deepcopy:
            for i in range(len(self._sequence)):
                self._sequence[i] = deepcopy(self._sequence[i])
        if symbol is not None:
            self.create_symbol(symbol)

    def __str__(self):
        s = "||["
        first = True
        for e in self._sequence:
            if first:
                first = False
            else:
                s += ", "
            s += str(e)
        s += "]"
        return s

    def is_transposable(self):
        return True

    def get_sequence(self):
        return self._sequence

    def extent(self):
        extent = 0
        for event in self._sequence:
            extent += event.extent()
        return extent

    def write(self, file):
        tie_extent = 0
        flat_sequence = list(self._sequence)
        for i in range(len(flat_sequence)):
            event = flat_sequence[i]
            if isinstance(event, Tone) \
                    and event._tie \
                    and i < len(flat_sequence) - 1 \
                    and isinstance(flat_sequence[i+1], Tone) \
                    and to_MIDI_pitch(flat_sequence[i+1]._pitch) == to_MIDI_pitch(event._pitch):
                tie_extent += event.extent()
                continue
            if tie_extent > 0:
                event._duration = tie_extent + Event.time_interval(event._duration)
                event._extent = tie_extent + Event.time_interval(event._extent)
                tie_extent = 0
            with transposed(event, self):
                event.write(file=file)
            if event.is_atomic() and event.extent() > 0:
                Event.write_indent(file)
                Event.wait(time=event.extent(), file=file)


class Measure(Sequence):
    def __init__(self,
                 events,
                 extent,
                 unit='b',
                 symbol=None,
                 make_deepcopy=True,
                 nested_idx=(1,),
                 amplitude=lambda nested_idx: 0.05 + 0.95 * np.exp(-metrical_grid(nested_idx) / 2)):
                 # amplitude=lambda nested_idx: 0.1 + 0.9 / (metrical_grid(nested_idx) + 1)):
                 # amplitude = lambda nested_idx: 1):
        if isinstance(events, str) or isinstance(events, Event):
            e = Event.parse_events(events)
            if e.is_atomic():
                e._extent = str(extent)+unit
            else:
                raise UserWarning("Don't know how to handle non-atomic event {} in measure".format(e))
            if isinstance(e, Chord):
                e._duration = str(extent)+unit
            if isinstance(e, (Chord, Beat)):
                e._amplitude = amplitude(nested_idx=nested_idx)
            sequence = [e]
        else:
            sequence = []
            part_extent = extent / len(events)
            for idx, e in enumerate(events):
                sequence.append(Measure(e, part_extent, unit=unit, nested_idx=list(nested_idx) + [idx]))
        super(Measure, self).__init__(sequence, symbol=None, make_deepcopy=make_deepcopy)


class Parallel(Event):

    @staticmethod
    def flatten(event, onset=0):
        if event.is_atomic():
            yield (event, onset, onset + event.extent())
        elif isinstance(event, Symbol):
            raise UserWarning("Cannot parallelize Symbol event {}".format(event))
        elif isinstance(event, Loop):
            raise UserWarning("Cannot parallelize Loop event {}".format(event))
        elif isinstance(event, Parallel):
            for e in event._block:
                yield from Parallel.flatten(event=e, onset=onset)
        elif isinstance(event, Sequence):
            new_onset = onset
            for e in event.get_sequence():
                if e.extent() is not None:
                    yield from Parallel.flatten(event=e, onset=new_onset)
                    new_onset += e.extent()
                else:
                    raise UserWarning("Cannot parallelize event {} with undefined extent {}".format(e, e.extent()))
        else:
            raise UserWarning("Don't know how to handle event {} in parallelization".format(event))

    def __init__(self, block, symbol=None, transpose=0, tonic=0, scale=Scale(), make_deepcopy=True):
        super(Parallel, self).__init__(transpose=transpose, tonic=tonic, scale=scale)
        self._block = block
        if make_deepcopy:
            for i in range(len(self._block)):
                self._block[i] = deepcopy(self._block[i])
        if symbol is not None:
            self.create_symbol(symbol)

    def __str__(self):
        s = "==["
        first = True
        for e in self._block:
            if first:
                first = False
            else:
                s += ", "
            s += str(e)
        s += "]"
        return s

    def is_transposable(self):
        return True

    def extent(self):
        extent = 0
        for event in self._block:
            extent = max(extent, event.extent())
        return extent

    def write(self, file):
        time = 0
        max_offset = 0
        for event, onset, offset in sorted(list(Parallel.flatten(self)), key=lambda x: x[1]):
            max_offset = max(max_offset, offset)
            if onset > time:
                Event.wait(time=onset - time, file=file)
                time = onset
            with transposed(event, self):
                event.write(file=file)
        if max_offset > time:
            Event.wait(time=max_offset - time, file=file)


class Transposed(Event):

    def __init__(self, event, transpose, tonic=0, scale=Scale(), make_deepcopy=False):
        super(Transposed, self).__init__(transpose=transpose, tonic=tonic, scale=scale)
        if not event.is_transposable():
            raise UserWarning("Cannot transpose event {}".format(event))
        if make_deepcopy:
            self._event = deepcopy(event)
        else:
            self._event = event

    def __str__(self):
        return "T("+str(self._event)+", {})".format(self._transpose)

    def is_atomic(self):
        return self._event.is_atomic()

    def is_transposable(self):
        return True

    def extent(self):
        return self._event.extent()

    def write(self, file):
        with transposed(self._event, self):
            self._event.write(file)


class Symbol(Event):

    def __init__(self, symbol):
        super(Symbol, self).__init__(transpose=0, tonic=0, scale=Scale())
        self._symbol = symbol

    def extent(self):
        return Event._symbols[self._symbol][2]

    def write(self, file):
        Event.write_indent(file)
        print("{} # {}".format(Event._symbols[self._symbol][0], self._symbol), file=file)


class Loop(Event):

    def __init__(self, event, symbol=None, repeat=None, active=True, transpose=0, tonic=0, scale=Scale()):
        super(Loop, self).__init__(transpose=transpose, tonic=tonic, scale=scale)
        self._symbol = symbol if symbol is not None else Event.random_string()
        self._repeat = repeat
        with transposed(event, self):
            event.create_symbol(self._symbol)
        self._symbol_event = Symbol(self._symbol)
        if active:
            Event.add_loop(self._symbol)

    def __str__(self):
        return "Loop("+self._symbol+")"

    def extent(self):
        if self._repeat is None:
            return None
        else:
            return self._repeat * self._symbol_event.extent()

    def write(self, file):
        Event.write_indent(file)
        if self._repeat is None:
            print("while loop_test('{}')".format(self._symbol), file=file)
        else:
            print("{}.times do".format(self._repeat), file=file)
        Event._indent += 1
        Event.write_indent(file)
        print('''puts "restart {}loop '{}'"'''.format(
            ('' if self._repeat is None else "{}-time-".format(self._repeat)),
            self._symbol),
            file=file)
        self._symbol_event.write(file)
        Event._indent -= 1
        Event.write_indent(file)
        print("end", file=file)


if __name__ == "__main__":
    with io.StringIO() as file:
        # create events and write to string-file
        Event.set_beat("380bpm")
        print("# main function", file=file)
        print("def song", file=file)
        Event._indent += 1
        ## measures
        m = Measure(['d', 'd', 'f', ['g_', 'g_', "d'"], 'a', 'g', 'f', 'e'], 4, 'sec') # swing
        m = Measure(['c', 'd', 'e', 'f', ['g', 'f'], ['e', 'd', 'c', 'B'], 'c'], 4)
        m = Measure([[["c'.", "d'."], ["e'.", "f'."]],
                     ["g'/2.", "g'/2."],
                     ["a'.", "a'.", "a'.", "a'."],
                     ["g'/1."],
                     ["a'.", "a'.", "a'.", "a'."],
                     ["g'/1."],
                     ["f'.", "f'.", "f'.", "f'."],
                     ["e'/2.", "e'/2."],
                     ["g'.", "g'.", "g'.", "g'."],
                     ["c'/1."]], extent=20)
        beat = Beat(extent="1/16")
        m = Measure([
            [[[beat, beat, beat], [beat, beat]],
             [[beat,       beat], [beat, beat]]],
            [[[beat,       beat], [beat, beat]],
             [[beat,       beat], [beat, beat]]],
            # [beat, beat, beat, beat],
        ], extent=8)
        # m.write(file)
        # Event.parse_event('r r/1').write(file)
        ## basic beat
        t = Tone("e", "1/4", amplitude=0.7)
        s = Sequence(
            [Beat(extent="1/4", amplitude=0.5),
             Parallel([t, Transposed(t, 4)]),
             Beat(extent="1/4", amplitude=1.),
             Rest("1/4")]
        )
        e = Event.parse_events("c r c. c. c. r c_ c_ c r")
        # print(e)
        # print(Sequence([e, f]))
        ## chords
        print(Chord(intervals=[0, 4, 7], base="e", duration="1/4", amplitude=0.7).rotate(1))
        ##
        ## alle meine entchen
        alle_mein_entchen = Event.parse_events("c' d' e' f' g'/2 g'/2 a' a' a' a' g'/1 a' a' a' a' g'/1 f' f' f' f' e'/2 e'/2 g' g' g' g' c'/1")
        scale = Scale(pitches=["c", "d", "e", "f", "g", "a", "b", "c"])
        print(scale)
        ##
        Loop(Sequence([
            Transposed(alle_mein_entchen, transpose=2, tonic='c', scale=scale),
            # m,
            ## quintuplets
            Parallel([
                # Measure(["c''", "r", "c''", "r", "c''", "r", "c''", "r", "c''", "r"], 4, 'b'),
                # Measure(['c', 'r', 'c', 'r', 'c', 'r', 'c', 'r'], 4, 'b'),
                # Measure(['b', 'r', 'b', 'r', 'b', 'r'], 4, 'b'),
            ]),
            # Loop(Sequence(
            #     [Beat(extent="1/4", amplitude=0.5),
            #      Chord(intervals=[0, 4], base="e", duration="1/4", amplitude=0.5),
            #      # Parallel([Tone("e", "1/4", amplitude=0.7), Tone("g#", "1/4", amplitude=0.7)]),
            #      # Event.parse_events("e/4 g#/4", agglomeration_type="Parallel"),
            #      Beat(extent="1/4", amplitude=1.),
            #      Rest("1/4")]
            # ), repeat=2),
            # # Loop(s, repeat=2),
            # Loop(Sequence(
            #     [Beat(extent="1/4", amplitude=0.5),
            #      Parallel([Tone("f#", "1/4", amplitude=0.5), Tone("a", "1/4", amplitude=0.5)]),
            #      Beat(extent="1/4", amplitude=1.),
            #      Rest("1/4")]
            # ), repeat=2)
        ]), "X").write(file)
        ##
        Event._indent -= 1
        print("end", file=file)
        print("", file=file)
        Event.write_loops(file)
        print("", file=file)
        Event.write_symbols(file)
        # write to sys out and real file
        print(file.getvalue())
        with open("song.rb", 'w') as song:
            print(file.getvalue(), file=song)