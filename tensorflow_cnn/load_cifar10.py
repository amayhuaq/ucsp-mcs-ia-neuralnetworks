import numpy as np
import plot_functions

########################################################################

# Directory where the data files are stored
DATA_PATH = "cifar-10-batches-py/"

########################################################################
# Various constants for the size of the images.

# Width and height of each image.
img_size = 32

# Number of channels in each image, 3 channels: RGB
num_channels = 3

# Length of an image when flattened to a 1-dim array.
img_size_flat = img_size * img_size * num_channels

# Number of classes.
num_classes = 10

########################################################################
# Various constants used to allocate arrays of the correct size.

# Number of files for the training-set.
_num_files_train = 5

# Number of images for each batch-file in the training-set.
_images_per_file = 10000

# Total number of images in the training-set.
_num_images_train = _num_files_train * _images_per_file

########################################################################
# Private functions for unpacking and loading data-files.

"""
Generate the One-Hot encoded class-labels from an array of integers.
For example, if class_number=2 and num_classes=4 then
the one-hot encoded label is the float array: [0. 0. 1. 0.]
:param class_numbers:
    Array of integers with class-numbers.
    Assume the integers are from zero to num_classes-1 inclusive.
:param num_classes:
    Number of classes. If None then use max(cls)-1.
:return:
    2-dim array of shape: [len(cls), num_classes]
"""
def one_hot_encoded(class_numbers, num_classes=None):
    # Find the number of classes if None is provided.
    if num_classes is None:
        num_classes = np.max(class_numbers) - 1

    return np.eye(num_classes, dtype=float)[class_numbers]


"""
Function used to read data from file
"""
def _unpickle(filename):
    import cPickle
    # Create full path for the file.
    file_path = DATA_PATH + filename
    print("Loading data: " + file_path)
    
    fo = open(file_path, 'rb')
    dictionary = cPickle.load(fo)
    fo.close()
    return dictionary
    

"""
Convert images from the CIFAR-10 format and
return a 4-dim array with shape: [image_number, height, width, channel]
where the pixels are floats between 0.0 and 1.0.
"""
def _convert_images(raw):
    # Convert the raw images from the data-files to floating-points.
    raw_float = np.array(raw, dtype=float) / 255.0

    # Reshape the array to 4-dimensions.
    images = raw_float.reshape([-1, num_channels, img_size, img_size])

    # Reorder the indices of the array.
    images = images.transpose([0, 2, 3, 1])

    return images


"""
Load a pickled data-file from the CIFAR-10 data-set
and return the converted images and the class-number for each image.
"""
def _load_data(filename):
    # Load the pickled data-file.
    data = _unpickle(filename)
    # Get the raw images.
    raw_images = data[b'data']
    # Get the class-numbers for each image.
    cls = np.array(data[b'labels'])
    # Convert the images.
    images = _convert_images(raw_images)

    return images, cls


########################################################################
# Public functions that you may call to load the data-set into memory.

"""
Load the names for the classes in the CIFAR-10 data-set.
Returns a list with the names. Example: names[3] is the name
associated with class-number 3.
"""
def load_class_names():
    # Load the class-names from the pickled file.
    return _unpickle(filename="batches.meta")[b'label_names']


"""
Load all the training-data for the CIFAR-10 data-set.
The data-set is split into 5 data-files which are merged here.
Returns the images, class-numbers and one-hot encoded class-labels.
"""
def load_training_data():
    # Pre-allocate the arrays for the images and class-numbers for efficiency.
    images = np.zeros(shape=[_num_images_train, img_size, img_size, num_channels], dtype=float)
    cls = np.zeros(shape=[_num_images_train], dtype=int)

    # Begin-index for the current batch.
    begin = 0

    # For each data-file.
    for i in range(_num_files_train):
        # Load the images and class-numbers from the data-file.
        images_batch, cls_batch = _load_data(filename="data_batch_" + str(i + 1))
        # Number of images in this batch.
        num_images = len(images_batch)
        # End-index for the current batch.
        end = begin + num_images
        # Store the images into the array.
        images[begin:end, :] = images_batch
        # Store the class-numbers into the array.
        cls[begin:end] = cls_batch
        # The begin-index for the next batch is the current end-index.
        begin = end

    return images, cls, one_hot_encoded(class_numbers=cls, num_classes=num_classes)


"""
Load all the test-data for the CIFAR-10 data-set.
Returns the images, class-numbers and one-hot encoded class-labels.
"""
def load_test_data():
    images, cls = _load_data(filename="test_batch")
    return images, cls, one_hot_encoded(class_numbers=cls, num_classes=num_classes)


"""
Load all data for training and testing
"""
def load_data(show_example_images=False):
    images_train, cls_train, labels_train = load_training_data()
    images_test, cls_test, labels_test = load_test_data()
    class_names = load_class_names()
    
    print("Size of:")
    print("- Training-set:\t\t{}".format(len(images_train)))
    print("- Test-set:\t\t{}".format(len(images_test)))
    
    if show_example_images:
        images = images_train[0:9]
        cls_true = cls_train[0:9]
        plot_functions.plot_images(images, class_names, cls_true)
        
    return class_names, {"train": {"images": images_train, "cls": cls_train, "labels": labels_train},
            "test": {"images": images_test, "cls": cls_test, "labels": labels_test}}
            
########################################################################
