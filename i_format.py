from bitstring import BitArray

instructs = [0x022DA822, 0x8EF30018, 0x12A70004, 0x02689820, 0xAD930018, 0x02697824, 0xAD8FFFF4,0x018C6020, 0x02A4A825, 0x158FFFF6, 0x8E59FFF0]


# mappers for R format with opcode dict 

offset_r = 0b1111111111111111
src_dest_r = 0b111110000000000000000
source_r = 0b11111000000000000000000000
opcode_r = 0b11111100000000000000000000000000

opcode_dict = {0b000100: 'beq', 0b101011: 'sw',  0b000101: 'bne', 0b100011:'lw'}


#Loop through R formats that are filtered by length
#Then: bit mask and shift values
#Then: map function value to function dict
# test = BitArray(int(binary))
# print test
for index, inst in enumerate(instructs):
	if inst.bit_length() > 26:
		opcode_map = (inst & opcode_r) >> 26
		offset_map = (inst & offset_r)
		twos_comp_offset = Bits(bin(offset_map))
		src_map = (inst & src_dest_r) >> 16
		src_dest_map = (inst & source_r) >> 21
		opcode_name = opcode_dict.get(opcode_map)
		if opcode_map == 0b100011 or opcode_map == 0b101011:
			if offset_map < 0xff:
				print opcode_name, "$",src_map, offset_map,"($", src_dest_map,")"
			else: 
				print opcode_name, "$",src_map, twos_comp_offset.int,"($", src_dest_map,")"
		else:
			if offset_map < 0xff:
				print opcode_name, "$",src_dest_map, offset_map,"($", src_map, ")"
			else:
				print opcode_name, "$",src_dest_map, twos_comp_offset.int,"($", src_map, ")"

			
		# else:
		# 	print opcode_name, src_dest_map, src_map, offset_map
		# 	print hex(offset_map >> 2)
