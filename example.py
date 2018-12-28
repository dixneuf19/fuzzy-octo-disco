import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from find_faces.pic import Picture

picture = Picture("pictures/lena.png")
picture.open()
picture.img2raw()

fig = plt.figure()
gs = gridspec.GridSpec(nrows=2, ncols=1)

ax0 = fig.add_subplot(gs[0, :])
ax0.imshow(picture.raw)
ax0.set_title('Original picture')

picture.find_faces()
picture.face_crop()
picture.img2raw()

ax1 = fig.add_subplot(gs[1, :])
ax1.imshow(picture.raw)
ax1.set_title('First face')

plt.tight_layout()
plt.show()
