from uc import libpango
import pango
#fonts = libpango.FAMILIES_LIST
#faces_dict = libpango.FAMILIES_DICT
#for item in fonts:
#	print item
#	faces = faces_dict[item]
#	for face_name in faces.keys():
#		print '\t', face_name

font = libpango.get_fontface('Arial')
print font.to_string()


