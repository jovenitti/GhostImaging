import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


SIDE  = 80			# pixel of square image
Ncicli= 500000			# n of speckle realizations

Nspek = 10			# n of speckle per image
Vspek = 1			# highest value of the speckle field
Sspek = 3			# size of each speckle (in pixels)

Xobs  = 20			# start of shadow (in x and y)
Yobs  = 60			# end of shadow (in x and y)
unagifogni = 1000		# sampling to crate the .gif

path  = './'			# 'path/to/output/folder/'



def speck_generator(SIDE, Nspek):

	I = np.zeros([SIDE , SIDE])

	xrand = 1 + np.random.randint(SIDE-2, size=Nspek)
	yrand = 1 + np.random.randint(SIDE-2, size=Nspek)

	for i in range(Nspek):
		I[xrand[i],   yrand[i]+1]  = Vspek
		I[xrand[i],   yrand[i]-1]  = Vspek
		I[xrand[i],   yrand[i]  ]  = Vspek
		I[xrand[i]+1, yrand[i]+1]  = Vspek
		I[xrand[i]+1, yrand[i]-1]  = Vspek
		I[xrand[i]+1, yrand[i]  ]  = Vspek
		I[xrand[i]-1, yrand[i]-1]  = Vspek
		I[xrand[i]-1, yrand[i]+1]  = Vspek
		I[xrand[i]-1, yrand[i]  ]  = Vspek

	return I;


def main():
	R   = np.zeros([SIDE , SIDE])
	ims = []
	fig = plt.figure()

	for k in range(0, Ncicli):

		I = speck_generator(SIDE, Nspek) 	# Image with speckles
		O = np.copy(I)				# Image with shadow
		
		for i in range(Xobs,Yobs):		# Put the shadow
			for j in range(Xobs,Yobs):
				O[i,j] =0.

		A = np.sum(O)				# Total intensity
		R = R+(I*A)				# Result = sum over weighted images
		RCROP = R[2:SIDE-2, 2:SIDE-2]
		CROP  = np.asarray(RCROP)
		if((k%unagifogni)==0):
			im    = plt.imshow(CROP, animated=True)
			ims.append([im])


	# Do the .gif image
	ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
	ani.save(path + '_GI_movie_'+ str(Nspek) + '_' + str("{:04d}".format(Ncicli)) +'.gif', dpi=80, writer='pillow')

	# Save some figure
	plt.clf()
	plt.imshow(I);    plt.savefig(path + 'I_' + str(Nspek) + '_' + str("{:04d}".format(Ncicli)) +'.png');	 plt.clf()
	plt.imshow(O);    plt.savefig(path + 'O_' + str(Nspek) + '_' + str("{:04d}".format(Ncicli)) +'.png');	 plt.clf()
	plt.imshow(CROP); plt.savefig(path + 'CROP_' + str(Nspek) + '_' + str("{:04d}".format(Ncicli)) +'.png'); plt.clf()


if __name__ == '__main__':
    main()
