import functools
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import os

hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

def crop_center(image):
  shape = image.shape
  new_shape = min(shape[1], shape[2])
  offset_y = max(shape[1] - shape[2], 0) // 2
  offset_x = max(shape[2] - shape[1], 0) // 2
  image = tf.image.crop_to_bounding_box(image, offset_y, offset_x, new_shape, new_shape)
  return image

@functools.lru_cache(maxsize=None)
def load_image(image_path, image_size=(256, 256)):
  img = tf.io.decode_image(tf.io.read_file(image_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

def get_image(content_path, style_path):
  content_image = load_image(content_path, (384, 384))
  style_image = load_image(style_path)
  style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
  return content_image, style_image

def model(content_image, style_image):
  outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
  stylized_image = outputs[0]
  tf.keras.preprocessing.image.save_img(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/images/style_photo.png'), stylized_image[0].numpy())
  return stylized_image[0]
