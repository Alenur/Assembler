import struct
import xml.etree.ElementTree as ET
import argparse
from xml.dom.minidom import parseString


class Assembler:
    def __init__(self, source_file, binary_file, log_file):
        self.source_file = source_file
        self.binary_file = binary_file
        self.log_file = log_file

    def assemble(self):
        with open(self.source_file, 'r') as f:
            lines = f.readlines()

        binary_data = bytearray()
        log_root = ET.Element("log")

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 3:
                continue

            command, b, c = parts
            b, c = int(b), int(c)

            if command == "LOAD":
                opcode = 134
            elif command == "READ":
                opcode = 177
            elif command == "WRITE":
                opcode = 214
            elif command == "SQRT":
                opcode = 127
            else:
                raise ValueError(f"Unknown command: {command}")

            instruction = struct.pack("<BHH", opcode, b, c)
            binary_data.extend(instruction)

            log_entry = ET.SubElement(log_root, "instruction")
            log_entry.set("command", command)
            log_entry.set("A", str(opcode))
            log_entry.set("B", str(b))
            log_entry.set("C", str(c))

        with open(self.binary_file, 'wb') as f:
            f.write(binary_data)

        xml_str = ET.tostring(log_root, encoding="utf-8")
        pretty_xml = parseString(xml_str).toprettyxml(indent="  ")
        with open(self.log_file, 'w', encoding="utf-8") as f:
            f.write(pretty_xml)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for UVM")
    parser.add_argument("--source_file", help="Path to the source file")
    parser.add_argument("--binary_file", help="Path to the binary file")
    parser.add_argument("--log_file", help="Path to the log file")
    args = parser.parse_args()

    assembler = Assembler(args.source_file, args.binary_file, args.log_file)
    assembler.assemble()
