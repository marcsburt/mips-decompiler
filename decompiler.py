from bitstring import Bits

instructs = [0x022DA822, 0x8EF30018, 0x12A70004, 0x02689820, 0xAD930018, 0x02697824, 0xAD8FFFF4,0x018C6020, 0x02A4A825, 0x158FFFF6, 0x8E59FFF0]


# mappers for R format with function_dict 
function_r = 0b111111
shift_r = 0b11111000000
dest_r = 0b1111100000000000
sec_source_r = 0b111110000000000000000
fir_source_r = 0b11111000000000000000000000
function_dict = {0b100010: 'sub', 0b100000: 'add',  0b100100:'and', 0b100101:'or'}

# mappers for R format with opcode dict 
offset_r = 0b1111111111111111
src_dest_r = 0b111110000000000000000
source_r = 0b11111000000000000000000000
opcode_r = 0b11111100000000000000000000000000
opcode_dict = {0b000100: 'beq', 0b101011: 'sw',  0b000101: 'bne', 0b100011:'lw'}


#Loop through all formats that are filtered by length 
#1: bit mask and shift values
#2: map function value to function dict
#Then: type of opcode repeat ^ 1 and 2 

for index, inst in enumerate(instructs):
	if inst.bit_length() <= 26:
		function_map = (inst & function_r)
		function_name = function_dict.get(function_map)
		shift_map = (inst & shift_r) >> 6
		dest_map = (inst & dest_r) >> 11
		sec_source_map = (inst & sec_source_r) >> 16
		fir_source_map = (inst & fir_source_r) >> 21
		print function_name, " $",dest_map," $", fir_source_map," $", sec_source_map 
	else:
		opcode_map = (inst & opcode_r) >> 26
		offset_map = (inst & offset_r)
		src_map = (inst & src_dest_r) >> 16
		src_dest_map = (inst & source_r) >> 21
		opcode_name = opcode_dict.get(opcode_map)
		if opcode_map == 35 or opcode_map == 43:
			print opcode_name, "$",src_dest_map, offset_map,"($", src_map,")"
		else:
			print opcode_name, src_dest_map, src_map, offset_map
	# print " -------------------------------------------- "



