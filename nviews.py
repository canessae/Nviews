import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def generate_intermediate(img, depth, offset, fact, updown : bool = False):
    (h, w) = depth.shape
    mapx = np.zeros(depth.shape).astype('float32')
    mapy = np.zeros(depth.shape).astype('float32')
    for ii in range(0, h):
        for jj in range(0, w):
            if not updown:
                mapy[ii, jj] = ii
                mapx[ii, jj] = jj - depth[ii, jj] * fact * offset
            else:
                mapy[ii, jj] = ii - depth[ii, jj] * fact * offset
                mapx[ii, jj] = jj
    result = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    return result

def generate_lr(img : np.ndarray, depth : np.ndarray):
    (h,w) = depth.shape
    fact = 1/25
    mapxl = np.zeros(depth.shape)
    mapxr = np.zeros(depth.shape)
    mapy = np.zeros(depth.shape)
    mapxl = mapxl.astype('float32')
    mapxr = mapxr.astype('float32')
    mapy = mapy.astype('float32')
    for ii in range(0, h):
        for jj in range(0, w):
            mapy[ii, jj] = ii
            mapxl[ii, jj] = jj - depth[ii, jj] * fact
            mapxr[ii, jj] = jj + depth[ii, jj] * fact

    resultl = cv2.remap(img, mapxl, mapy, cv2.INTER_LINEAR)
    resultr = cv2.remap(img, mapxr, mapy, cv2.INTER_LINEAR)
    plt.figure(1)
    plt.subplot(1,3,2)
    plt.imshow(img)
    plt.subplot(1,3,1)
    plt.imshow(resultl)
    plt.title('laeva')
    plt.subplot(1, 3, 3)
    plt.imshow(resultr)
    plt.title('dextera')
    plt.show()

def main(imageFilename, depthFilename, viewNumber: int, fact, updown : bool):
    im = cv2.imread(imageFilename)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    depth = cv2.imread(depthFilename)
    plt.figure(1)
    plt.title('Preview')
    ref = plt.imshow(im)
    plt.axis('off')
    plt.ion()
    toshow = []
    depthGray = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
    delta = 2 / viewNumber
    print("delta " + str(delta))
    cnt = 0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    dim = im.shape[:-1]
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, dim[::-1])
    for offset in np.arange(-1, 1+delta, delta):
        print(offset)
        #Per Enrique: da modificare l'ultimo parametro della seguente chiamata 1/50
        toshow.append(generate_intermediate(im, depthGray, offset, fact, updown))
        cv2.imwrite("output" + str(cnt) + ".png", cv2.cvtColor(toshow[-1], cv2.COLOR_RGB2BGR))
        cnt += 1

    #create video
    fw = True
    cnt = 0
    for loop in range(6):
        for idx in range(len(toshow)):
            out.write(toshow[cnt])
            if fw:
                cnt = cnt + 1
            else:
                cnt = cnt - 1
            if cnt == len(toshow) - 1:
                fw = False
            elif cnt == 0:
                fw = True

    out.release()

    cnt = 0
    fw = True
    N = len(toshow)
    while True:
        ref.set_data(toshow[cnt])
        if fw:
            cnt = cnt+1
        else:
            cnt = cnt-1
        if cnt == N-1:
            fw = False
        elif cnt == 0:
            fw = True
        status = plt.waitforbuttonpress(0.1)
        if status:
            break

    plt.ioff()
    plt.show()

def commandline():
    parser = argparse.ArgumentParser(
        prog = "Nviews",
        description = "Simple python code to create n views from image and depth")
    parser.add_argument('-i', '--inputimage', required=True, help='Input image')
    parser.add_argument('-d', '--depthmap', required=True, help='Dephtmap required to reconstruct views')
    parser.add_argument('-nv', '--nviews', required=True, type=int, help='Number of views to be created')
    parser.add_argument('-f', '--factor', default="1/50", help="Factor to be used to create n views")
    parser.add_argument('-ud', '--updown', action='store_true', default=False, help="Up-down mode instead of left-right")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = commandline()

    main(args.inputimage, args.depthmap, args.nviews, float(eval(args.factor)), args.updown)
