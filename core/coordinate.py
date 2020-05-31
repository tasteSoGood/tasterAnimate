import numpy as np

class coordinate(object):
    def __init__(self, xlims: tuple, ylims: tuple, xgap = 1.0, ygap = 1.0, grid_color = (1, 1, 1, 1), grid_width = 0.02):
        '''
        xlims: x轴的范围
        ylims: y轴的范围
        xgap: x轴上的间隔
        ygap: y轴上的间隔
        grid_color: 网格线的颜色
        grid_width: 网格线的宽度
        '''
        self._xlims = xlims
        self._ylims = ylims
        self._xgap = xgap
        self._ygap = ygap
        self._grid_color = grid_color
        self._grid_width = grid_width

    def draw(self, canv):
        '''
        主轴
        '''
        ctx = canv.context
        ctx.set_source_rgba(*self._grid_color)
        ctx.set_line_width(self._grid_width)
        # x轴
        ctx.move_to(self._xlims[0], 0)
        ctx.line_to(self._xlims[1], 0)
        ctx.stroke()
        # y轴
        ctx.move_to(0, self._ylims[0])
        ctx.line_to(0, self._ylims[1])
        ctx.stroke()

        '''
        网格
        '''
        ctx.set_line_width(self._grid_width * 0.5)
        ctx.set_dash([0.1, 0.02, 0.02, 0.02])
        ctx.set_source_rgba(*self._grid_color[:3], self._grid_color[-1] * 0.5)
        for y in np.arange(np.floor(self._ylims[0]), np.ceil(self._ylims[1]) + 1, 1):
            ctx.move_to(self._xlims[0], y)
            ctx.line_to(self._xlims[1], y)
            ctx.stroke()
        for x in np.arange(np.floor(self._xlims[0]), np.ceil(self._xlims[1]) + 1, 1):
            ctx.move_to(x, self._ylims[0])
            ctx.line_to(x, self._ylims[1])
            ctx.stroke()
        ctx.set_dash([1, 0])

