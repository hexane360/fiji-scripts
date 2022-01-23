import os.path

try:
	from sc.fiji.hdf5 import HDF5ImageJ
	from ch.systemsx.cisd.hdf5 import HDF5Factory
except ImportError:
	raise Exception("HDF5 Plugin not found")

from ij.io import OpenDialog


def choose_file():
	dialog = OpenDialog("Choose a RevSTEM HDF5 file", None)
	
	folder = dialog.getDirectory()
	name = dialog.getFileName()
	if folder is None or name is None:
		return None
	return folder + name


def c_char_to_string(bytestring):
	return str(bytearray(bytestring).split('\x00', 1)[0])


def get_pixel_size(reader):
	metadata = reader.string().read("/Metadata")
	try:
		metadata = json.loads(metadata)
	except Exception:
		return None
		ij.log("WARNING: Invalid metadata for image " + group.getPath())

	return metadata['Pixel Size']


def revstem_import(path=None):
	if path is None:
		path = choose_file()
		if path is None:
			return
	name = os.path.basename(path)
	name, ext = os.path.splitext(name)

	reader = HDF5Factory.openForReading(path)

	try:
		detectors = reader.getGroupMembers("/Images")
	except ValueError:
		raise Exception("Not an RevSTEM HDF5 file")

	pixel_size = get_pixel_size(reader)

	for det in detectors:
		id = next(iter(reader.getGroupMembers("/Images/{}".format(det))))
		img = HDF5ImageJ.hdf5read(path, "/Images/{}/{}".format(det, id), "yxt")
		if img is None:
			return
		
		calibration = img.getCalibration()
		if pixel_size is None:
			calibration.setUnit("pixel")
		else:
			calibration.setUnit("angstrom")
			calibration.pixelHeight = pixel_size[0] * 1e10
			calibration.pixelWidth = pixel_size[1] * 1e10

		calibration.setTimeUnit("frame")
		img.setTitle("{} ({})".format(name, det))
		img.show()


if __name__ in ('__builtin__', '__main__'):
	revstem_import()