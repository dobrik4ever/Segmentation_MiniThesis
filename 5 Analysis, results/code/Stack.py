from skimage import io, filters, morphology
from matplotlib import pyplot as plt
import numpy as np
import os
import plotly.graph_objects as go

class Stack:
    def __init__(self, path):
        self.path = path
        self.files_list = os.listdir(path)
        self.channels = self.__get_channels_n()
        self.depth = len(self.files_list) // len(self.channels)
        img = io.imread(f'{path}/{self.files_list[0]}')
        self.height, self.width = img.shape
        self.load()

    def __get_channel(self, fname):
        idx = fname.find('C0')
        channel = int(fname[idx+2:idx+3])
        return channel

    def __get_depth(self, fname):
        idx = fname.find('Z0')
        depth = int(fname[idx+1:].split('.')[0])
        return depth

    def __get_channels_n(self):
        cs = []
        for file in self.files_list:
            channel = self.__get_channel(file)
            cs.append(channel)
        cs = set(cs)
        return cs
        
    def load(self):
        self.img = np.zeros([len(self.channels), self.depth, self.height, self.width])
        for file in self.files_list:
            img = io.imread(f'{self.path}/{file}')
            if len(img.shape) != 2: continue
            channel = self.__get_channel(file)
            depth = self.__get_depth(file)
            self.img[channel, depth] = img
        
        
        print(  f'Stack {self.path} was loaded\n' + \
                f'Resolution: {self.img.shape}\n')

    def plot_z(self, index):
        img = self.img[:,index].copy()
        for i in range(3):
            img[i] = img[i] / img[i].max()
        img = np.transpose(img, axes=[1,2,0])
        io.imshow(img)
        plt.show()

    def show_volume(self, img = None, area = None):
        img = img or self.img
        if area:
            img = img[:,area[0]:area[1],area[2]:area[3]]
        else:
            img = img[:,100:200,150:250]
        Z, Y, X = img.shape
        Z, Y, X = mgrid[:Z, :Y, :X]
        X = X.ravel()
        Y = Y.ravel()
        Z = Z.ravel()
        V = img.ravel()

        fig = go.Figure(data=go.Volume(
            x=X, y=Y, z=Z, value=V,
            isomin=V.min(),
            isomax=V.max(),
            opacity=0.1, # needs to be small to see through all surfaces
            surface_count=21, # needs to be a large number for good volume rendering
            ))
        fig.show()

if __name__ == '__main__':
    stack = Stack('MBT/good stacks/160722_01 stack P10_16-43-47')
    stack.plot_z(100)