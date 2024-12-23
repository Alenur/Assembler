import struct
import xml.etree.ElementTree as ET
import argparse
import math
from xml.dom.minidom import parseString

class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory = [0] * 1024  # Условная память УВМ
        self.memory_range = memory_range

    def execute(self):
        with open(self.binary_file, 'rb') as f:
            binary_data = f.read()

        pc = 0
        while pc < len(binary_data):
            opcode, b, c = struct.unpack_from("<BHH", binary_data, pc)
            pc += 5

            if opcode == 134:  # LOAD
                self.memory[b] = c
            elif opcode == 177:  # READ
                self.memory[b] = self.memory[c]
            elif opcode == 214:  # WRITE
                self.memory[self.memory[b]] = self.memory[c]
            elif opcode == 127:  # SQRT
                self.memory[b] = int(math.sqrt(self.memory[c]))
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

        self.save_result()

    def save_result(self):
        root = ET.Element("memory")
        for i in range(self.memory_range[0], self.memory_range[1]):
            mem_entry = ET.SubElement(root, "cell")
            mem_entry.set("address", str(i))
            mem_entry.set("value", str(self.memory[i]))

        xml_str = ET.tostring(root, encoding="utf-8")
        pretty_xml = parseString(xml_str).toprettyxml(indent="  ")
        with open(self.result_file, 'w', encoding="utf-8") as f:
            f.write(pretty_xml)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for UVM")
    parser.add_argument("--binary_file", help="Path to the binary file")
    parser.add_argument("--result_file", help="Path to the result file")
    parser.add_argument("--memory_range", help="Memory range (start:end)", type=str)
    args = parser.parse_args()

    memory_range = list(map(int, args.memory_range.split(":")))
    interpreter = Interpreter(args.binary_file, args.result_file, memory_range)
    interpreter.execute()
