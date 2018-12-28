import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from path import Path

from find_faces.pic import Picture

picture = Picture("pictures/lena.png")
picture.open()
picture.img2raw()

fig = plt.figure()
gs = gridspec.GridSpec(nrows=3, ncols=2, height_ratios=[2, 1, 2])

# Original picture
ax0 = fig.add_subplot(gs[0, :])
ax0.imshow(picture.raw)
ax0.set_title('Original picture')

# Original picture

# Rotate
rotate = picture.clone()
rotate.rotate(Picture.ROTATE_90)
rotate.img2raw()
ax_rotate = fig.add_subplot(gs[1, 0])
ax_rotate.imshow(rotate.raw)
ax_rotate.set_title("90° rotation")

# Flip
flip = picture.clone()
flip.rotate(Picture.FLIP_LEFT_RIGHT)
flip.img2raw()
ax_rotate = fig.add_subplot(gs[1, 1])
ax_rotate.imshow(flip.raw)
ax_rotate.set_title("Flip right-left")

# First faces
picture.find_faces()
picture.face_crop()
picture.img2raw()

ax1 = fig.add_subplot(gs[2, :])
ax1.imshow(picture.raw)
ax1.set_title('First face')

plt.tight_layout()
plt.show()
