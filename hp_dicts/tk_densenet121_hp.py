# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2022/3/5 16:53

class HyperParamsDictRatio2x:
    kernel_shapes = {
        'features.conv0.weight': [64, 3, 7, 7],
        'features.denseblock1.denselayer1.conv1.weight':    [128, 64, 1, 1],
        'features.denseblock1.denselayer1.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock1.denselayer2.conv1.weight':    [128, 96, 1, 1],
        'features.denseblock1.denselayer2.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock1.denselayer3.conv1.weight':    [128, 128, 1, 1],
        'features.denseblock1.denselayer3.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock1.denselayer4.conv1.weight':    [128, 160, 1, 1],
        'features.denseblock1.denselayer4.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock1.denselayer5.conv1.weight':    [128, 192, 1, 1],
        'features.denseblock1.denselayer5.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock1.denselayer6.conv1.weight':    [128, 224, 1, 1],
        'features.denseblock1.denselayer6.conv2.weight':    [32, 128, 3, 3],
        'features.transition1.conv.weight':                 [128, 256, 1, 1],
        'features.denseblock2.denselayer1.conv1.weight':    [128, 128, 1, 1],
        'features.denseblock2.denselayer1.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer2.conv1.weight':    [128, 160, 1, 1],
        'features.denseblock2.denselayer2.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer3.conv1.weight':    [128, 192, 1, 1],
        'features.denseblock2.denselayer3.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer4.conv1.weight':    [128, 224, 1, 1],
        'features.denseblock2.denselayer4.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer5.conv1.weight':    [128, 256, 1, 1],
        'features.denseblock2.denselayer5.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer6.conv1.weight':    [128, 288, 1, 1],
        'features.denseblock2.denselayer6.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer7.conv1.weight':    [128, 320, 1, 1],
        'features.denseblock2.denselayer7.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer8.conv1.weight':    [128, 352, 1, 1],
        'features.denseblock2.denselayer8.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer9.conv1.weight':    [128, 384, 1, 1],
        'features.denseblock2.denselayer9.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock2.denselayer10.conv1.weight':   [128, 416, 1, 1],
        'features.denseblock2.denselayer10.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock2.denselayer11.conv1.weight':   [128, 448, 1, 1],
        'features.denseblock2.denselayer11.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock2.denselayer12.conv1.weight':   [128, 480, 1, 1],
        'features.denseblock2.denselayer12.conv2.weight':   [32, 128, 3, 3],
        'features.transition2.conv.weight':                 [256, 512, 1, 1],
        'features.denseblock3.denselayer1.conv1.weight':    [128, 256, 1, 1],
        'features.denseblock3.denselayer1.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer2.conv1.weight':    [128, 288, 1, 1],
        'features.denseblock3.denselayer2.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer3.conv1.weight':    [128, 320, 1, 1],
        'features.denseblock3.denselayer3.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer4.conv1.weight':    [128, 352, 1, 1],
        'features.denseblock3.denselayer4.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer5.conv1.weight':    [128, 384, 1, 1],
        'features.denseblock3.denselayer5.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer6.conv1.weight':    [128, 416, 1, 1],
        'features.denseblock3.denselayer6.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer7.conv1.weight':    [128, 448, 1, 1],
        'features.denseblock3.denselayer7.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer8.conv1.weight':    [128, 480, 1, 1],
        'features.denseblock3.denselayer8.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer9.conv1.weight':    [128, 512, 1, 1],
        'features.denseblock3.denselayer9.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock3.denselayer10.conv1.weight':   [128, 544, 1, 1],
        'features.denseblock3.denselayer10.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer11.conv1.weight':   [128, 576, 1, 1],
        'features.denseblock3.denselayer11.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer12.conv1.weight':   [128, 608, 1, 1],
        'features.denseblock3.denselayer12.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer13.conv1.weight':   [128, 640, 1, 1],
        'features.denseblock3.denselayer13.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer14.conv1.weight':   [128, 672, 1, 1],
        'features.denseblock3.denselayer14.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer15.conv1.weight':   [128, 704, 1, 1],
        'features.denseblock3.denselayer15.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer16.conv1.weight':   [128, 736, 1, 1],
        'features.denseblock3.denselayer16.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer17.conv1.weight':   [128, 768, 1, 1],
        'features.denseblock3.denselayer17.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer18.conv1.weight':   [128, 800, 1, 1],
        'features.denseblock3.denselayer18.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer19.conv1.weight':   [128, 832, 1, 1],
        'features.denseblock3.denselayer19.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer20.conv1.weight':   [128, 864, 1, 1],
        'features.denseblock3.denselayer20.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer21.conv1.weight':   [128, 896, 1, 1],
        'features.denseblock3.denselayer21.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer22.conv1.weight':   [128, 928, 1, 1],
        'features.denseblock3.denselayer22.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer23.conv1.weight':   [128, 960, 1, 1],
        'features.denseblock3.denselayer23.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock3.denselayer24.conv1.weight':   [128, 992, 1, 1],
        'features.denseblock3.denselayer24.conv2.weight':   [32, 128, 3, 3],
        'features.transition3.conv.weight':                 [512, 1024, 1, 1],
        'features.denseblock4.denselayer1.conv1.weight':    [128, 512, 1, 1],
        'features.denseblock4.denselayer1.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer2.conv1.weight':    [128, 544, 1, 1],
        'features.denseblock4.denselayer2.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer3.conv1.weight':    [128, 576, 1, 1],
        'features.denseblock4.denselayer3.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer4.conv1.weight':    [128, 608, 1, 1],
        'features.denseblock4.denselayer4.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer5.conv1.weight':    [128, 640, 1, 1],
        'features.denseblock4.denselayer5.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer6.conv1.weight':    [128, 672, 1, 1],
        'features.denseblock4.denselayer6.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer7.conv1.weight':    [128, 704, 1, 1],
        'features.denseblock4.denselayer7.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer8.conv1.weight':    [128, 736, 1, 1],
        'features.denseblock4.denselayer8.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer9.conv1.weight':    [128, 768, 1, 1],
        'features.denseblock4.denselayer9.conv2.weight':    [32, 128, 3, 3],
        'features.denseblock4.denselayer10.conv1.weight':   [128, 800, 1, 1],
        'features.denseblock4.denselayer10.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer11.conv1.weight':   [128, 832, 1, 1],
        'features.denseblock4.denselayer11.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer12.conv1.weight':   [128, 864, 1, 1],
        'features.denseblock4.denselayer12.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer13.conv1.weight':   [128, 896, 1, 1],
        'features.denseblock4.denselayer13.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer14.conv1.weight':   [128, 928, 1, 1],
        'features.denseblock4.denselayer14.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer15.conv1.weight':   [128, 960, 1, 1],
        'features.denseblock4.denselayer15.conv2.weight':   [32, 128, 3, 3],
        'features.denseblock4.denselayer16.conv1.weight':   [128, 992, 1, 1],
        'features.denseblock4.denselayer16.conv2.weight':   [32, 128, 3, 3],
    }
    ranks = {
        # 'features.conv0.weight': [64, 3, 7, 7],
        # 'features.denseblock1.denselayer1.conv1.weight':    [32],
        'features.denseblock1.denselayer1.conv2.weight':    [32, 64],
        # 'features.denseblock1.denselayer2.conv1.weight':    [32],
        'features.denseblock1.denselayer2.conv2.weight':    [32, 64],
        # 'features.denseblock1.denselayer3.conv1.weight':    [32],
        'features.denseblock1.denselayer3.conv2.weight':    [32, 64],
        # 'features.denseblock1.denselayer4.conv1.weight':    [64],
        'features.denseblock1.denselayer4.conv2.weight':    [32, 64],
        # 'features.denseblock1.denselayer5.conv1.weight':    [64],
        'features.denseblock1.denselayer5.conv2.weight':    [32, 64],
        # 'features.denseblock1.denselayer6.conv1.weight':    [64],
        'features.denseblock1.denselayer6.conv2.weight':    [32, 64],
        # 'features.transition1.conv.weight':                 [128, 256, 1, 1],
        # 'features.denseblock2.denselayer1.conv1.weight':    [128, 128, 1, 1],
        'features.denseblock2.denselayer1.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer2.conv1.weight':    [128, 160, 1, 1],
        'features.denseblock2.denselayer2.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer3.conv1.weight':    [128, 192, 1, 1],
        'features.denseblock2.denselayer3.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer4.conv1.weight':    [128, 224, 1, 1],
        'features.denseblock2.denselayer4.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer5.conv1.weight':    [128, 256, 1, 1],
        'features.denseblock2.denselayer5.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer6.conv1.weight':    [128, 288, 1, 1],
        'features.denseblock2.denselayer6.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer7.conv1.weight':    [128, 320, 1, 1],
        'features.denseblock2.denselayer7.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer8.conv1.weight':    [128, 352, 1, 1],
        'features.denseblock2.denselayer8.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer9.conv1.weight':    [128, 384, 1, 1],
        'features.denseblock2.denselayer9.conv2.weight':    [32, 64],
        # 'features.denseblock2.denselayer10.conv1.weight':   [128, 416, 1, 1],
        'features.denseblock2.denselayer10.conv2.weight':   [32, 64],
        # 'features.denseblock2.denselayer11.conv1.weight':   [128, 448, 1, 1],
        'features.denseblock2.denselayer11.conv2.weight':   [32, 64],
        # 'features.denseblock2.denselayer12.conv1.weight':   [128, 480, 1, 1],
        'features.denseblock2.denselayer12.conv2.weight':   [32, 64],
        # 'features.transition2.conv.weight':                 [256, 512, 1, 1],
        # 'features.denseblock3.denselayer1.conv1.weight':    [128, 256, 1, 1],
        'features.denseblock3.denselayer1.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer2.conv1.weight':    [128, 288, 1, 1],
        'features.denseblock3.denselayer2.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer3.conv1.weight':    [128, 320, 1, 1],
        'features.denseblock3.denselayer3.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer4.conv1.weight':    [128, 352, 1, 1],
        'features.denseblock3.denselayer4.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer5.conv1.weight':    [128, 384, 1, 1],
        'features.denseblock3.denselayer5.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer6.conv1.weight':    [128, 416, 1, 1],
        'features.denseblock3.denselayer6.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer7.conv1.weight':    [128, 448, 1, 1],
        'features.denseblock3.denselayer7.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer8.conv1.weight':    [128, 480, 1, 1],
        'features.denseblock3.denselayer8.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer9.conv1.weight':    [128, 512, 1, 1],
        'features.denseblock3.denselayer9.conv2.weight':    [32, 64],
        # 'features.denseblock3.denselayer10.conv1.weight':   [128, 544, 1, 1],
        'features.denseblock3.denselayer10.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer11.conv1.weight':   [128, 576, 1, 1],
        'features.denseblock3.denselayer11.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer12.conv1.weight':   [128, 608, 1, 1],
        'features.denseblock3.denselayer12.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer13.conv1.weight':   [128, 640, 1, 1],
        'features.denseblock3.denselayer13.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer14.conv1.weight':   [128, 672, 1, 1],
        'features.denseblock3.denselayer14.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer15.conv1.weight':   [128, 704, 1, 1],
        'features.denseblock3.denselayer15.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer16.conv1.weight':   [128, 736, 1, 1],
        'features.denseblock3.denselayer16.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer17.conv1.weight':   [128, 768, 1, 1],
        'features.denseblock3.denselayer17.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer18.conv1.weight':   [128, 800, 1, 1],
        'features.denseblock3.denselayer18.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer19.conv1.weight':   [128, 832, 1, 1],
        'features.denseblock3.denselayer19.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer20.conv1.weight':   [128, 864, 1, 1],
        'features.denseblock3.denselayer20.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer21.conv1.weight':   [128, 896, 1, 1],
        'features.denseblock3.denselayer21.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer22.conv1.weight':   [128, 928, 1, 1],
        'features.denseblock3.denselayer22.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer23.conv1.weight':   [128, 960, 1, 1],
        'features.denseblock3.denselayer23.conv2.weight':   [32, 64],
        # 'features.denseblock3.denselayer24.conv1.weight':   [128, 992, 1, 1],
        'features.denseblock3.denselayer24.conv2.weight':   [32, 64],
        # 'features.transition3.conv.weight':                 [512, 1024, 1, 1],
        # 'features.denseblock4.denselayer1.conv1.weight':    [128, 512, 1, 1],
        'features.denseblock4.denselayer1.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer2.conv1.weight':    [128, 544, 1, 1],
        'features.denseblock4.denselayer2.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer3.conv1.weight':    [128, 576, 1, 1],
        'features.denseblock4.denselayer3.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer4.conv1.weight':    [128, 608, 1, 1],
        'features.denseblock4.denselayer4.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer5.conv1.weight':    [128, 640, 1, 1],
        'features.denseblock4.denselayer5.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer6.conv1.weight':    [128, 672, 1, 1],
        'features.denseblock4.denselayer6.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer7.conv1.weight':    [128, 704, 1, 1],
        'features.denseblock4.denselayer7.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer8.conv1.weight':    [128, 736, 1, 1],
        'features.denseblock4.denselayer8.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer9.conv1.weight':    [128, 768, 1, 1],
        'features.denseblock4.denselayer9.conv2.weight':    [32, 64],
        # 'features.denseblock4.denselayer10.conv1.weight':   [128, 800, 1, 1],
        'features.denseblock4.denselayer10.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer11.conv1.weight':   [128, 832, 1, 1],
        'features.denseblock4.denselayer11.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer12.conv1.weight':   [128, 864, 1, 1],
        'features.denseblock4.denselayer12.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer13.conv1.weight':   [128, 896, 1, 1],
        'features.denseblock4.denselayer13.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer14.conv1.weight':   [128, 928, 1, 1],
        'features.denseblock4.denselayer14.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer15.conv1.weight':   [128, 960, 1, 1],
        'features.denseblock4.denselayer15.conv2.weight':   [32, 64],
        # 'features.denseblock4.denselayer16.conv1.weight':   [128, 992, 1, 1],
        'features.denseblock4.denselayer16.conv2.weight':   [32, 64],
    }