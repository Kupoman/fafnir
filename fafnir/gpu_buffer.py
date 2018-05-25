import panda3d.core as p3d


class GpuBuffer:
    def __init__(self, name, count, data_type, data_format):
        self.buffer = p3d.Texture(name)
        self.data_type = data_type
        self.data_format = data_format
        self.resize(count)

    def resize(self, count):
        self.buffer.setup_buffer_texture(
            count,
            self.data_type,
            self.data_format,
            p3d.GeomEnums.UH_dynamic
        )
        self.buffer.prepare(base.win.get_gsg().get_prepared_objects())

        ram_image = self.buffer.modify_ram_image()
        for i in range(len(ram_image)):
            ram_image[i] = 0

    def get_buffer_id(self):
        gsg = base.win.get_gsg()
        pgo = gsg.get_prepared_objects()
        context = self.buffer.prepare_now(0, pgo, gsg)
        return context.get_native_buffer_id()

    def get_texture(self):
        return self.buffer

    def print_buffer(self, count):
        base.graphics_engine.extract_texture_data(self.buffer, base.win.get_gsg())
        view = memoryview(self.buffer.get_ram_image()).cast('f')
        for i in range(count):
            print(view[i], end=' ')
        print()
