import pygame as pg

from . import Vec

class Tilemap:
    surface: pg.Surface
    shape: Vec[int]
    tile_shape_px: Vec[float]
    draw_anchor: Vec[float] # Upper-left corner in `surface` that all tiles are drawn relative to

    def __init__(self,
                 *,
                 surface: pg.Surface,
                 shape: Vec[int],
                 border_pad: Vec[int] = Vec(0, 0),
                 anchor_offset: Vec[int] = Vec(0, 0),
                 force_square: bool = False,
                 force_integer_size: bool = False,
                 ):
        """
        Parameters
        ---
        * `surface` - The surface to draw on
        * `shape` - In tiles, the shape of the tilemap
        * `force_square` - Whether to force tiles to be drawn with equal width and height
        * `force_integer_size` - Whether to force all tiles to be the exact same size in pixels
        * `border_pad` - In pixels, how much to pad borders in all directions
        * `anchor_offset` In pixels, how much to offset the upper left corner by
        """
        # Check params
        if not border_pad >= 0:
            raise ValueError(f"The border pad cannot be negative")
        if not shape > 0:
            raise ValueError(f"The dimensions of the tilemap in tiles must be positive")

        # Determine size of each tile
        surface_shape_px = Vec(*surface.get_size())
        draw_shape_px = surface_shape_px - border_pad * 2 # take border padding into account
        if not draw_shape_px > 0:
            raise ValueError(f"The border padding is too big; it would occlude the entire tilemap drawing space")
        tile_shape_px = draw_shape_px / shape
        if force_square:
            sidelen = tile_shape_px.min()
            tile_shape_px = Vec(sidelen, sidelen)
        if force_integer_size:
            tile_shape_px = tile_shape_px.astype(int)

        # Determine location of upper-left draw anchor
        center = surface_shape_px // 2
        draw_anchor = center - (shape * tile_shape_px / 2)
        draw_anchor += anchor_offset
        
        # Finally set member variables
        self.surface = surface
        self.shape = shape
        self.tile_shape_px = tile_shape_px
        self.draw_anchor = draw_anchor


    def get_pos_px(self, pos: Vec[int]) -> Vec[int]:
        """
        Returns the upper-left corner position, in pixels, of the desired tile
        """
        return (self.draw_anchor + self.tile_shape_px * pos).astype(int)


    def get_shape_px(self, pos: Vec[int]) -> Vec[int]:
        """
        Returns the shape, in pixels, of the desired tile
        """
        pos_px = self.get_pos_px(pos)
        pos_px_next = self.get_pos_px(pos + 1)
        return pos_px_next - pos_px


    def get_pos_shape_px(self, pos: Vec[int]):
        pos_px = self.get_pos_px(pos)
        pos_px_next = self.get_pos_px(pos + 1)
        shape_px = pos_px_next - pos_px
        return pos_px, shape_px


    def set_color(self, pos: Vec[int], color: pg.Color):
        pos_px, shape_px = self.get_pos_shape_px(pos)
        pg.draw.rect(self.surface, color, pg.Rect(*pos_px, *shape_px))
