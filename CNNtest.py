from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import model

CHECK_POINT_DIR = '/home/panxiyao/Desktop/modelsave'
def evaluate_one_image(image_array):
	with tf.Graph().as_default():
		image = tf.cast(image_array, tf.float32)
		image = tf.image.per_image_standardization(image)
		image = tf.reshape(image, [1,64,64,3])

		logit = model.inference(image, 1, 2)
		logit = tf.nn.softmax(logit)

		#x = tf.placeholder(tf.float32, shape=[64,64,3])

		saver = tf.train.Saver()
		with tf.Session() as sess:
			print ('Reading checkpoints...')
			ckpt = tf.train.get_checkpoint_state(CHECK_POINT_DIR)
			if ckpt and ckpt.model_checkpoint_path:
				global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
				saver.restore(sess, ckpt.model_checkpoint_path)
				print('Loading success, global_step is %s' %global_step)
			else:
				print ('No checkpoint file found')
			prediction = sess.run(logit)
			#prediction = sess.run(logit, feed_dict = {x:image_array})
			max_index = np.argmax(prediction)
			print (prediction)
			if max_index == 0:
				result = ('this is cokecan rate: %.6f, result prediction is [%s]' %(prediction[:,0],','.join(str(i) for i in prediction[0])))
			else:
				result = ('this is bowl rate: %.6f, result prediction is [%s]' %(prediction[:,1],','.join(str(i) for i in prediction[0])))
			return result


if __name__ == '__main__':
	image = Image.open('/home/panxiyao/Desktop/TrainSet/0/19.jpg')
	plt.imshow(image)
	plt.show()
	image = image.resize([64,64])
	image = np.array(image)
	print(evaluate_one_image(image))