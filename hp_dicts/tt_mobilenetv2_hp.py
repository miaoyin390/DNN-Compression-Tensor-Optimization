# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/11/3 15:31


class HyperParamsDictRatio2x:
    kernel_shapes = {
        'features.0.0.weight': [32, 3, 3, 3],
        'features.1.conv.0.0.weight': [32, 1, 3, 3],
        'features.1.conv.1.weight': [16, 32, 1, 1],
        'features.2.conv.0.0.weight': [96, 16, 1, 1],
        'features.2.conv.1.0.weight': [96, 1, 3, 3],
        'features.2.conv.2.weight': [24, 96, 1, 1],
        'features.3.conv.0.0.weight': [144, 24, 1, 1],
        'features.3.conv.1.0.weight': [144, 1, 3, 3],
        'features.3.conv.2.weight': [24, 144, 1, 1],
        'features.4.conv.0.0.weight': [144, 24, 1, 1],
        'features.4.conv.1.0.weight': [144, 1, 3, 3],
        'features.4.conv.2.weight': [32, 144, 1, 1],
        'features.5.conv.0.0.weight': [192, 32, 1, 1],
        'features.5.conv.1.0.weight': [192, 1, 3, 3],
        'features.5.conv.2.weight': [32, 192, 1, 1],
        'features.6.conv.0.0.weight': [192, 32, 1, 1],
        'features.6.conv.1.0.weight': [192, 1, 3, 3],
        'features.6.conv.2.weight': [32, 192, 1, 1],
        'features.7.conv.0.0.weight': [192, 32, 1, 1],
        'features.7.conv.1.0.weight': [192, 1, 3, 3],
        'features.7.conv.2.weight': [64, 192, 1, 1],
        'features.8.conv.0.0.weight': [384, 64, 1, 1],
        'features.8.conv.1.0.weight': [384, 1, 3, 3],
        'features.8.conv.2.weight': [64, 384, 1, 1],
        'features.9.conv.0.0.weight': [384, 64, 1, 1],
        'features.9.conv.1.0.weight': [384, 1, 3, 3],
        'features.9.conv.2.weight': [64, 384, 1, 1],
        'features.10.conv.0.0.weight': [384, 64, 1, 1],
        'features.10.conv.1.0.weight': [384, 1, 3, 3],
        'features.10.conv.2.weight': [64, 384, 1, 1],
        'features.11.conv.0.0.weight': [384, 64, 1, 1],
        'features.11.conv.1.0.weight': [384, 1, 3, 3],
        'features.11.conv.2.weight': [96, 384, 1, 1],
        'features.12.conv.0.0.weight': [576, 96, 1, 1],
        'features.12.conv.1.0.weight': [576, 1, 3, 3],
        'features.12.conv.2.weight': [96, 576, 1, 1],
        'features.13.conv.0.0.weight': [576, 96, 1, 1],
        'features.13.conv.1.0.weight': [576, 1, 3, 3],
        'features.13.conv.2.weight': [96, 576, 1, 1],
        'features.14.conv.0.0.weight': [576, 96, 1, 1],
        'features.14.conv.1.0.weight': [576, 1, 3, 3],
        'features.14.conv.2.weight': [160, 576, 1, 1],
        'features.15.conv.0.0.weight': [960, 160, 1, 1],
        'features.15.conv.1.0.weight': [960, 1, 3, 3],
        'features.15.conv.2.weight': [160, 960, 1, 1],
        'features.16.conv.0.0.weight': [960, 160, 1, 1],
        'features.16.conv.1.0.weight': [960, 1, 3, 3],
        'features.16.conv.2.weight': [160, 960, 1, 1],
        'features.17.conv.0.0.weight': [960, 160, 1, 1],
        'features.17.conv.1.0.weight': [960, 1, 3, 3],
        'features.17.conv.2.weight': [320, 960, 1, 1],
        'features.18.0.weight': [1280, 320, 1, 1],
    }

    tt_shapes = {
        # 'features.1.conv.1.weight': [16, 1, 32],
        'features.2.conv.0.0.weight': [96, 1, 16],
        'features.2.conv.2.weight': [24, 1, 96],
        'features.3.conv.0.0.weight': [144, 1, 24],
        'features.3.conv.2.weight': [24, 1, 144],
        'features.4.conv.0.0.weight': [144, 1, 24],
        'features.4.conv.2.weight': [32, 1, 144],
        'features.5.conv.0.0.weight': [192, 1, 32],
        'features.5.conv.2.weight': [32, 1, 192],
        'features.6.conv.0.0.weight': [192, 1, 32],
        'features.6.conv.2.weight': [32, 1, 192],
        'features.7.conv.0.0.weight': [192, 1, 32],
        'features.7.conv.2.weight': [64, 1, 192],
        'features.8.conv.0.0.weight': [384, 1, 64],
        'features.8.conv.2.weight': [64, 1, 384],
        'features.9.conv.0.0.weight': [384, 1, 64],
        'features.9.conv.2.weight': [64, 1, 384],
        'features.10.conv.0.0.weight': [384, 1, 64],
        'features.10.conv.2.weight': [64, 1, 384],
        'features.11.conv.0.0.weight': [384, 1, 64],
        'features.11.conv.2.weight': [96, 1, 384],
        'features.12.conv.0.0.weight': [576, 1, 96],
        'features.12.conv.2.weight': [96, 1, 576],
        'features.13.conv.0.0.weight': [576, 1, 96],
        'features.13.conv.2.weight': [96, 1, 576],
        'features.14.conv.0.0.weight': [576, 1, 96],
        'features.14.conv.2.weight': [160, 1, 576],
        'features.15.conv.0.0.weight': [960, 1, 160],
        'features.15.conv.2.weight': [160, 1, 960],
        'features.16.conv.0.0.weight': [960, 1, 160],
        'features.16.conv.2.weight': [160, 1, 960],
        'features.17.conv.0.0.weight': [960, 1, 160],
        'features.17.conv.2.weight': [320, 1, 960],
        'features.18.0.weight': [1280, 1, 320],
    }

    ranks = {
        'features.2.conv.0.0.weight': [1, 14, 14, 1],
        'features.2.conv.2.weight': [1, 18, 18, 1],
        'features.3.conv.0.0.weight': [1, 18, 18, 1],
        'features.3.conv.2.weight': [1, 18, 18, 1],
        'features.4.conv.0.0.weight': [1, 18, 18, 1],
        'features.4.conv.2.weight': [1, 24, 24, 1],
        'features.5.conv.0.0.weight': [1, 22, 22, 1],
        'features.5.conv.2.weight': [1, 22, 22, 1],
        'features.6.conv.0.0.weight': [1, 22, 22, 1],
        'features.6.conv.2.weight': [1, 22, 22, 1],
        'features.7.conv.0.0.weight': [1, 24, 24, 1],
        'features.7.conv.2.weight': [1, 22, 22, 1],
        'features.8.conv.0.0.weight': [1, 28, 28, 1],
        'features.8.conv.2.weight': [1, 28, 28, 1],
        'features.9.conv.0.0.weight': [1, 28, 28, 1],
        'features.9.conv.2.weight': [1, 28, 28, 1],
        'features.10.conv.0.0.weight': [1, 28, 28, 1],
        'features.10.conv.2.weight': [1, 28, 28, 1],
        'features.11.conv.0.0.weight': [1, 30, 30, 1],
        'features.11.conv.2.weight': [1, 35, 35, 1],
        'features.12.conv.0.0.weight': [1, 35, 35, 1],
        'features.12.conv.2.weight': [1, 40, 40, 1],
        'features.13.conv.0.0.weight': [1, 40, 40, 1],
        'features.13.conv.2.weight': [1, 40, 40, 1],
        'features.14.conv.0.0.weight': [1, 40, 40, 1],
        'features.14.conv.2.weight': [1, 64, 64, 1],
        'features.15.conv.0.0.weight': [1, 60, 60, 1],
        'features.15.conv.2.weight': [1, 60, 60, 1],
        'features.16.conv.0.0.weight': [1, 60, 60, 1],
        'features.16.conv.2.weight': [1, 60, 60, 1],
        'features.17.conv.0.0.weight': [1, 60, 60, 1],
        'features.17.conv.2.weight': [1, 100, 100, 1],
        'features.18.0.weight': [1, 100, 100, 1],
    }