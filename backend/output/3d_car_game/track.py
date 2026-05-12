# track.py: This module defines the Track class, which represents a 3D racing track.

import numpy as np
from pymunk import Vec2d
import pymunk

class Track:
    """
    Represents a 3D racing track.
    
    Attributes:
        name (str): The name of the track.
        width (float): The width of the track.
        height (float): The height of the track.
        segments (list): A list of track segments.
    """

    def __init__(self, name, width, height):
        # Initialize the track with a name, width, and height.
        self.name = name
        self.width = width
        self.height = height
        self.segments = []

    def add_segment(self, start, end, radius):
        # Add a new segment to the track.
        segment = TrackSegment(start, end, radius)
        self.segments.append(segment)

    def get_segment(self, index):
        # Get a segment at a specific index.
        return self.segments[index]

    def get_num_segments(self):
        # Get the number of segments in the track.
        return len(self.segments)


class TrackSegment:
    """
    Represents a segment of a 3D racing track.
    
    Attributes:
        start (Vec2d): The starting point of the segment.
        end (Vec2d): The ending point of the segment.
        radius (float): The radius of the segment.
    """

    def __init__(self, start, end, radius):
        # Initialize the segment with a start point, end point, and radius.
        self.start = start
        self.end = end
        self.radius = radius

    def get_length(self):
        # Calculate the length of the segment.
        return (self.end - self.start).length


class Checkpoint:
    """
    Represents a checkpoint on a 3D racing track.
    
    Attributes:
        position (Vec2d): The position of the checkpoint.
        radius (float): The radius of the checkpoint.
    """

    def __init__(self, position, radius):
        # Initialize the checkpoint with a position and radius.
        self.position = position
        self.radius = radius


# Example usage:
if __name__ == "__main__":
    # Create a new track.
    track = Track("Example Track", 1000, 1000)

    # Add some segments to the track.
    track.add_segment(Vec2d(0, 0), Vec2d(100, 0), 10)
    track.add_segment(Vec2d(100, 0), Vec2d(200, 100), 20)
    track.add_segment(Vec2d(200, 100), Vec2d(300, 0), 30)

    # Print the number of segments in the track.
    print("Number of segments:", track.get_num_segments())

    # Get a segment and print its length.
    segment = track.get_segment(0)
    print("Length of segment 0:", segment.get_length())