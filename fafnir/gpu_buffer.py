import panda3d.core as p3d


class GpuBuffer:
    def __init__(self, name, count, gsg, data_type, data_format):
        self._gsg = gsg
        self._buffer = p3d.Texture(name)
        self.data_type = data_type
        self.data_format = data_format
        self.resize(count)

    def resize(self, count):
        self._buffer.setup_buffer_texture(
            count,
            self.data_type,
            self.data_format,
            p3d.GeomEnums.UH_dynamic
        )
        self._buffer.prepare(self._gsg.get_prepared_objects())

        # pylint: disable=consider-using-enumerate
        ram_image = self._buffer.modify_ram_image()
        for i in range(len(ram_image)):
            ram_image[i] = 0

    def get_buffer_id(self):
        pgo = self._gsg.get_prepared_objects()
        context = self._buffer.prepare_now(0, pgo, self._gsg)
        return context.get_native_buffer_id()

    def get_texture(self):
        return self._buffer

    def extract_data(self, graphics_engine):
        graphics_engine.extract_texture_data(self._buffer, self._gsg)
        view = memoryview(self._buffer.get_ram_image()).cast('f')
        return view


class GpuBufferRGBA32F(GpuBuffer):
    def __init__(self, name, count, gsg):
        super().__init__(name, count, gsg, p3d.Texture.T_float, p3d.Texture.F_rgba32)
