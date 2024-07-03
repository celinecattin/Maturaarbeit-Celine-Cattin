import numpy as np  # importing the numpy library
from mnist import MNIST  # importing the mnist library
import matplotlib.pyplot as plt  # import libraries to display the cube
from PIL import Image

# definition for importing drawings from photoshop:
def photoshopimage(filepath): # Achtung! Beim Filepath \\ einfügen!
    pic = Image.open(filepath) # open the image
    pix = np.array(pic) # convert into an np. array
    pix = pix[:,:,0] < 32 # choose one layer of values and only keep the pixels with values lower than 32 (the black values)
    return(1*pix) # 1 * pix to convert the true and false values into 1 and 0


def mnistimage(num): # definition to import arrays of mnist
    img = mnist.train_set.images[num, :].reshape(28,28)  # Take image num+1 of the training set and reshape its array to a 28 * 28 grid
    a = mnist.train_set.labels[num, :]  # assign the corresponding label to a
    print(np.where(a == 1)[0][0])  # printing the position of label a which corresponds to the number in the img1
    # [0][0] converts it to an integer
    return(img)

def perlenoptimieren(cube): # definition to minimize the number of points plotted
    sz = cube.shape
    for z in range(sz[2]): # für alle Ebenen in die z Richtung
        for x in range(sz[0]): # für alle Zeilen in die x Richtung.
            for y in range(sz[1]): # für alle Spalten in die y Richtung.
                if cube[x, y, z] == 1:
                    row = cube[x, :, z]
                    column = cube[:, y, z]
                    if sum(row) > 1 and sum(column) > 1: # Wenn in der gleichen Reihe und Spalte auch bereits eine 1 ist,
                        cube[x, y, z] = 0 # Dann wird die 1 zu einer 0 umgewandelt.
    return(cube)

# definition to make a construction plan for my model with pearls
def printBauplan(cubegraph):
    g = np.arange(cubegraph.shape[2])  # make an array the length of the z axes

    for x in range(cubegraph.shape[0]):  # check all combinations of x and y coordinates in cubegraph
        for y in range(cubegraph.shape[1]):
            v = g[cubegraph[x, y,:]]  # g assigns a number from the array to each true value on the z axes (v) at point x,y
            if len(v) > 0:  # if there are true values, it prints the z coordinate of these values. (seen from bottom to top)
                print(x, y, v)


def optimizeAllSides(cube): # optimize the number of points starting from the 4 different sides of the cube
    cube1 = perlenoptimieren(cube)
    cube2 = np.rot90(cube, 1)
    cube2 = perlenoptimieren(cube2)
    cube3 = np.rot90(cube, 2)
    cube3 = perlenoptimieren(cube3)
    cube4 = np.rot90(cube, 3)
    cube4 = perlenoptimieren(cube4)

    sz = cube.shape
    for z in range(sz[2]): # für jede Ebene die Anzahl Punkte zusammenzählen
        a = np.sum(cube1[:, :, z])
        b = np.sum(cube2[:, :, z])
        c = np.sum(cube3[:, :, z])
        d = np.sum(cube4[:, :, z])
        min_index = np.argmin([a, b, c, d]) # Die Ebene herausgeben, die die minimalste Anzahl Punkte hat.
    return(cube1,cube2,cube3,cube4)


def calculatemin (cube): # calculating the minimal number of points necessary to display this model
    print("Die Minimums der Ebenen sind:")
    sz = cube.shape
    summe = 0
    for z in range(sz[2]): # für jede Ebene
        a = np.sum(cube[:,:,z],0) # Die Summe der Punkte in allen Reihen in x - Richtung zusammenzählen.
        b = np.sum(cube[:,:,z],1) # Die Summe der Punkte in allen Spalten in y - Richtung zusammenzählen.

        c = np.size(np.where(a > 0)) # Die Anzahl Reihen zusammenzählen, in denen a > 0
        d = np.size(np.where(b > 0)) # Die Anzahl Spalten zusammenzählen in denen b > 0

        if c > d: # Je nachdem ob c oder d grösser ist, entspricht dies der minimaler möglicher Anzahl Punkte.
            print(z, c)
            summe= summe+c
        else:
            print(z, d)
            summe = summe + d
        return (a, b, c, d,summe)

    print('Das Optimum besteht aus',summe,'Punkten.')








def CalcMinCube (cube): # calculating the minimal number of points necessary to display this model
    sz = cube.shape
    optimum = np.zeros(sz)
    summeebene = 0
    for z in range(sz[2]): # für jede Ebene
        a = np.sum(cube[:,:,z],0) # Die Summe der Punkte in allen Reihen in x - Richtung zusammenzählen.
        b = np.sum(cube[:,:,z],1) # Die Summe der Punkte in allen Spalten in y - Richtung zusammenzählen.

        c = np.size(np.where(a > 0)) # Die Anzahl Reihen zusammenzählen, in denen a > 0
        d = np.size(np.where(b > 0)) # Die Anzahl Spalten zusammenzählen in denen b > 0

        if c > d: # Je nachdem ob c oder d grösser ist, entspricht dies der minimaler möglicher Anzahl Punkte.
            bb = np.zeros(b.shape)
            for x in range(sz[0]):

                if a[x] > 0: # a an der Stelle x

                    pointSetFlag = False

                    for y in range(sz[1]):

                        if (cube[x,y,z]>0) and (bb[y] == 0):
                            optimum[x, y, z] = 1
                            bb[y] = +1
                            pointSetFlag = True
                            break
                    if pointSetFlag == False:
                        for y in range(sz[1]):
                            if (cube[x, y, z] > 0) and (pointSetFlag == False):
                                optimum[x, y, z] = 1
                                bb[y] = +1
                                pointSetFlag = True


        else: # man könnte den Würfel hier auch 90 Grad rotieren und das Selbe wie oben machen.
            aa = np.zeros(a.shape)
            for y in range(sz[1]):
                if b[y]>0:
                    pointSetFlag = False

                    for x in range(sz[0]):

                        if (cube[x, y, z] > 0) and (aa[x] == 0):
                            optimum[x, y, z] = 1
                            aa[x] = +1
                            pointSetFlag = True
                            break
                    if pointSetFlag == False:
                        for x in range(sz[0]):
                            if (cube[x, y, z] > 0) and (pointSetFlag == False):
                                optimum[x, y, z] = 1
                                aa[x] = +1
                                pointSetFlag = True


                    #if sum == summe :
                       # continue
                    #else:
                        #print(z,'Ebene hat eine falsche Anzahl Punkte.')


    return(optimum)


 # training set with letters
mnist = MNIST()
# mnist.train_set.images  (60000, 784) (60000 images, 784 values for the 28*28 grid; arranged as array)
# mnist.train_set.labels  (60000, 10) (60000 images, 10 different possible labels -one hot encoded (for deep learning))



img1 = photoshopimage("C:\\Users\\Celine\\Documents\\Kanti Jahr 3\\Maturaarbeit\\png files\\note1.png")
img2 = photoshopimage ("C:\\Users\\Celine\\Documents\\Kanti Jahr 3\\Maturaarbeit\\png files\\csharp.png")

#img1 = mnistimage(7)
#img2 = mnistimage(9)

img1 = np.rot90(img1, -1, (0, 1))  # rotate the image
vol1 = np.tile(img1, (28, 1, 1))  # img1 is stacked on top of each other 28 times


img2 = np.rot90(img2, -1, (0, 1))  # rotate image
vol2 = np.tile(img2, (28, 1, 1))  # img2 ist stacked on top of each other 28 times
vol2 = np.rot90(vol2, 1)  # rotate vol2 to show the number from another side as vol1
# print(np.where(b == 1)[0][0])  # printing the position of label b which corresponds to the number of img2

cube = vol1 * vol2  # multiplying the two cubes of the two images
cubegraph = cube > 0  # print only the points where there is a number > 1 (because 0 = no color, 1= black )
cube[cubegraph] = 1.  # converting all values that are true in cubegraph to a 1.

#calculatemin(cube)


#cube1, cube2, cube3, cube4 = optimizeAllSides(cube) # Die 4 verschiedenen Cubes herausgeben.


#cube = perlenoptimieren(cube)
optimum = CalcMinCube(cube)
cubegraph = optimum > 0  # print only the points where there is a number > 1 (because 0 = no color, 1= black )


anzahlperlen = np.size(np.where(cubegraph == True))  # count the printed points
print(anzahlperlen)


# Create a meshgrid for x, y, z coordinates
x, y, z = np.meshgrid(np.arange(cubegraph.shape[0]),
                      # make a meshgrid 28*28 (the shape of cubegraph of the x axes(x=0))
                      np.arange(cubegraph.shape[1]),
                      np.arange(cubegraph.shape[2]))

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # put the plot in the field 111 (because I have only 1 plot)

# Plot the points
ax.scatter(x[cubegraph], y[cubegraph], z[cubegraph])  # plot the points where cubegraph is true

# Add labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()


printBauplan(cubegraph)

# convert numpy array into STL file
from skimage import measure  # skimage is for image processing, measure can measure image properties
from stl import mesh  # import numpy-stl library

# Generate vertices and faces using marching_cubes
verts, faces, normals, values = measure.marching_cubes(cubegraph, spacing=(1, 1, 1))

# Create the mesh
surf = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        surf.vectors[i][j] = verts[f[j], :]

# Save as STL file
surf.save('try.stl')