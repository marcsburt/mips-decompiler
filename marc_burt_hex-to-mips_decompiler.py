from bitstring import Bits #for 32 bit instructions as python no longer supports twos compliment



#instruction set
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

# start address will get incremented in loop, so subtract 4 to move bits left by 2
address = 0x7a060 - 4

#Loop through all formats that are filtered by length => if bit length is less than or equal to 26 assume I format, else assume R format
	#1: bit mask and shift values
	#2: map function value to function or opcode dict depending on whether it's in I or R formate
	#3: add 4 to address
	#Then: type of opcode or function repeat ^ 1 and 2 

for index, inst in enumerate(instructs):
	address += 4
	if inst.bit_length() <= 26:
		function_map = (inst & function_r)
		function_name = function_dict.get(function_map)
		shift_map = (inst & shift_r) >> 6
		dest_map = (inst & dest_r) >> 11
		sec_source_map = (inst & sec_source_r) >> 16
		fir_source_map = (inst & fir_source_r) >> 21
		print hex(address), ':', function_name, " $",dest_map," $", fir_source_map," $", sec_source_map 
	else:
		offset_map = (inst & offset_r)
		twos_comp_offset = Bits(bin(offset_map))
		src_map = (inst & src_dest_r) >> 16
		src_dest_map = (inst & source_r) >> 21
		opcode_map = (inst & opcode_r) >> 26
		opcode_name = opcode_dict.get(opcode_map)

		#if opcode is sw or lw format output accordingly
		#else assume it's a bne or bqe and format output accordingly

		if opcode_map == 0b100011 or opcode_map == 0b101011:
			# if offset is less than positive integers, keep positive
			# else assume negative output negative offset (specific to python's interpretation of bits)
			if offset_map < 0xff:
				print hex(address), ':', opcode_name, '$',src_map, offset_map,'($', src_dest_map,')'
			else: 
				print hex(address), ':', opcode_name, '$',src_map, twos_comp_offset.int,'($', src_dest_map,')'
		else:
			# if offset is less than positive integers, keep positive
			# else assume negative output negative offset
			if offset_map < 0xff:
				print hex(address), ':', opcode_name, '$',src_dest_map, '$', src_map, hex((offset_map << 2) + address + 4)

			else:
				print hex(address), ':', opcode_name, '$',src_dest_map, '$', src_map, hex((offset_map << 2) + address + 4)







