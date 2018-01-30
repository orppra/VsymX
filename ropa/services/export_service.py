import struct
import subprocess
import sys

from ropa.gui.controller.file_dialog_controller import FileDialogController


class ExportService:
    def __init__(self, backend, widget):
        self.backend = backend
        self.widget = widget
        self.file_dialog_controller = FileDialogController()

    def num_bits(self, arch):
        if arch.endswith('64'):
            return 64
        return 32

    def open_exported(self, filepath):
        if sys.platform.startswith('linux'):
            subprocess.call(["xdg-open", filepath])

        # Let's ignore this for now,
        # I don't even know how to set python qt up on windows
        #
        # elif sys.platform.startswith('win'):
        #     subprocess.call([filepath])

        elif sys.platform.startswith('darwin'):  # mac
            subprocess.call(["open", filepath])

    def export_binary(self):
        filepath = self.file_dialog_controller.open_file_dialog()
        chain = []
        for index in range(self.widget.count()):
            block = str(self.widget.item(index).text())
            print(str(block))
            block = block.strip().split('\n')
            address = block[0]
            block = block[2:]
            instructions = []
            for b in block:
                instructions.append(block)
            chain.append([{'address': address, 'instructions': instructions}])

        with open(filepath, 'w') as outfile:
            for block in chain:
                for gadget in block:
                    if self.num_bits(self.backend.get_arch()) == 32:
                        outfile.write(struct.pack('<I',
                                      int(gadget['address'], 16)))
                    else:
                        outfile.write(struct.pack('<Q',
                                      int(gadget['address'], 16)))
            outfile.close()

        self.open_exported(filepath)

    def export_python_struct(self):
        filepath = self.file_dialog_controller.open_file_dialog()
        chain = []
        for index in range(self.widget.count()):
            block = str(self.widget.item(index).text())
            print(str(block))
            block = block.strip().split('\n')
            address = block[0]
            block = block[2:]
            instructions = []
            for b in block:
                instructions.append(b)
            chain.append([{'address': address, 'instructions': instructions}])

        with open(filepath, 'w') as outfile:
            outfile.write('p = ""\n')
            for block in chain:
                for gadget in block:
                    if self.num_bits(self.backend.get_arch()) == 32:
                        outfile.write('p += struct.pack("<I", {})'
                                      .format(gadget['address']))
                    else:
                        outfile.write('p += struct.pack("<Q", {})'
                                      .format(gadget['address']))

                    outfile.write('  # ')
                    for instruction in gadget['instructions']:
                        outfile.write('{}; '.format(instruction))

                    outfile.write('\n')
            outfile.close()

        self.open_exported(filepath)

    def export_python_pwntools(self):
        filepath = self.file_dialog_controller.open_file_dialog()
        chain = []
        for index in range(self.widget.count()):
            block = str(self.widget.item(index).text())
            block = block.strip().split('\n')
            address = block[0]
            block = block[2:]
            instructions = []
            for b in block:
                print(b)
                instructions.append(b)
            print(instructions)
            chain.append([{'address': address, 'instructions': instructions}])

        with open(filepath, 'w') as outfile:
            outfile.write('p = ""\n')
            for block in chain:
                for gadget in block:
                    if self.num_bits(self.backend.get_arch()) == 32:
                        outfile.write('p += p32({})'
                                      .format(gadget['address']))
                    else:
                        outfile.write('p += p64({})'
                                      .format(gadget['address']))

                    outfile.write('  # ')
                    for instruction in gadget['instructions']:
                        outfile.write('{}; '.format(instruction))

                    outfile.write('\n')
            outfile.close()

        self.open_exported(filepath)
