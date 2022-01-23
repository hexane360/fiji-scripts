import os.path
import json

try:
	from sc.fiji.hdf5 import HDF5ImageJ
	from ch.systemsx.cisd.hdf5 import HDF5Factory
except ImportError:
	raise Exception("HDF5 Plugin not found")

from ij.io import OpenDialog
import ij


def choose_file():
	dialog = OpenDialog("Choose a HDF5/EMD file", None)
	
	folder = dialog.getDirectory()
	name = dialog.getFileName()
	if folder is None or name is None:
		return None
	return folder + name


def old_emd_import(path=None):
	if path is None:
		path = choose_file()
		if path is None:
			return
	name = os.path.basename(path)
	name, ext = os.path.splitext(name)

	reader = HDF5Factory.openForReading(path)

	try:
		img_ids = reader.getGroupMembers("/Data/Image")
	except ValueError:
		raise Exception("Not an Velox HDF5/EMD file")

	for (i, id) in enumerate(img_ids):
		img = HDF5ImageJ.hdf5read(path, "/Data/Image/{}/Data".format(id), "yxt")
		img.getCalibration().setUnit("pixel")
		suffix = " ({})".format(i) if len(img_ids) > 1 else ""
		img.setTitle(name + suffix)
		img.show()

def c_char_to_string(bytestring):
	return str(bytearray(bytestring).split('\x00', 1)[0])

def emd_import(path=None):
	if path is None:
		path = choose_file()
		if path is None:
			return
	name = os.path.basename(path)
	name, ext = os.path.splitext(name)

	reader = HDF5Factory.openForReading(path)

	try:
		img_groups = reader.getGroupMemberInformation("/Data/Image", False)
	except ValueError:
		raise Exception("Not an Velox HDF5/EMD file")

	for group in img_groups:
		#metadata = reader.uint8().readMDArraySlice(group.getPath() + "/Metadata", [-1, 0]).getAsFlatArray()
		#metadata = c_char_to_string(metadata)
		#try:
		#	metadata = json.loads(metadata)
		#except Exception:
		#	ij.log("WARNING: Invalid metadata for image " + group.getPath())
		#print(metadata)
		img = HDF5ImageJ.hdf5read(path, group.getPath() + "/Data", "yxt")
		img.getCalibration().setUnit("pixel")
		suffix = " ({})".format(i) if len(img_groups) > 1 else ""
		img.setTitle(name + suffix)
		img.show()


#def create_stack(reader, title):
#	img = ij.createHyperStack(title, width, height, 1, 1, frames, bitdepth)
#
#	for frame in range(frames):
#		processor = img.getStack().getProcessor(imp.getStackIndex(1, 1, 2))
#		data = reader.uint8().readMDArray()


if __name__ in ('__builtin__', '__main__'):
	emd_import()