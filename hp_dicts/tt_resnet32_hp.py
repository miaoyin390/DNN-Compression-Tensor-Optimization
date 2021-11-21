# -*- coding:utf-8 -*-
# 
# Author: MIAO YIN
# Time: 2021/9/30 20:11

# in_order = len(in_tt_shapes)
# out_order = len(out_tt_shapes)


class HyperParamsDictRatio3x:
    tt_shapes = {
        'layer1.0.conv1.weight': [16, 9, 16],
        'layer1.0.conv2.weight': [16, 9, 16],
        'layer1.1.conv1.weight': [16, 9, 16],
        'layer1.1.conv2.weight': [16, 9, 16],
        'layer1.2.conv1.weight': [16, 9, 16],
        'layer1.2.conv2.weight': [16, 9, 16],
        'layer1.3.conv1.weight': [16, 9, 16],
        'layer1.3.conv2.weight': [16, 9, 16],
        'layer1.4.conv1.weight': [16, 9, 16],
        'layer1.4.conv2.weight': [16, 9, 16],
        'layer2.0.conv1.weight': [8, 4, 9, 4, 4],
        'layer2.0.conv2.weight': [8, 4, 9, 4, 8],
        'layer2.1.conv1.weight': [8, 4, 9, 4, 8],
        'layer2.1.conv2.weight': [8, 4, 9, 4, 8],
        'layer2.2.conv1.weight': [8, 4, 9, 4, 8],
        'layer2.2.conv2.weight': [8, 4, 9, 4, 8],
        'layer2.3.conv1.weight': [8, 4, 9, 4, 8],
        'layer2.3.conv2.weight': [8, 4, 9, 4, 8],
        'layer2.4.conv1.weight': [8, 4, 9, 4, 8],
        'layer2.4.conv2.weight': [8, 4, 9, 4, 8],
        'layer3.0.conv1.weight': [8, 8, 9, 4, 8],
        'layer3.0.conv2.weight': [8, 8, 9, 8, 8],
        'layer3.1.conv1.weight': [8, 8, 9, 8, 8],
        'layer3.1.conv2.weight': [8, 8, 9, 8, 8],
        'layer3.2.conv1.weight': [8, 8, 9, 8, 8],
        'layer3.2.conv2.weight': [8, 8, 9, 8, 8],
        'layer3.3.conv1.weight': [8, 8, 9, 8, 8],
        'layer3.3.conv2.weight': [8, 8, 9, 8, 8],
        'layer3.4.conv1.weight': [8, 8, 9, 8, 8],
        'layer3.4.conv2.weight': [8, 8, 9, 8, 8]
    }

    in_tt_shapes = {
        'layer1.0.conv1.weight': [16],
        'layer1.0.conv2.weight': [16],
        'layer1.1.conv1.weight': [16],
        'layer1.1.conv2.weight': [16],
        'layer1.2.conv1.weight': [16],
        'layer1.2.conv2.weight': [16],
        'layer1.3.conv1.weight': [16],
        'layer1.3.conv2.weight': [16],
        'layer1.4.conv1.weight': [16],
        'layer1.4.conv2.weight': [16],
        'layer2.0.conv1.weight': [4, 4],
        'layer2.0.conv2.weight': [4, 8],
        'layer2.1.conv1.weight': [4, 8],
        'layer2.1.conv2.weight': [4, 8],
        'layer2.2.conv1.weight': [4, 8],
        'layer2.2.conv2.weight': [4, 8],
        'layer2.3.conv1.weight': [4, 8],
        'layer2.3.conv2.weight': [4, 8],
        'layer2.4.conv1.weight': [4, 8],
        'layer2.4.conv2.weight': [4, 8],
        'layer3.0.conv1.weight': [4, 8],
        'layer3.0.conv2.weight': [8, 8],
        'layer3.1.conv1.weight': [8, 8],
        'layer3.1.conv2.weight': [8, 8],
        'layer3.2.conv1.weight': [8, 8],
        'layer3.2.conv2.weight': [8, 8],
        'layer3.3.conv1.weight': [8, 8],
        'layer3.3.conv2.weight': [8, 8],
        'layer3.4.conv1.weight': [8, 8],
        'layer3.4.conv2.weight': [8, 8]
    }

    out_tt_shapes = {
        'layer1.0.conv1.weight': [16],
        'layer1.0.conv2.weight': [16],
        'layer1.1.conv1.weight': [16],
        'layer1.1.conv2.weight': [16],
        'layer1.2.conv1.weight': [16],
        'layer1.2.conv2.weight': [16],
        'layer1.3.conv1.weight': [16],
        'layer1.3.conv2.weight': [16],
        'layer1.4.conv1.weight': [16],
        'layer1.4.conv2.weight': [16],
        'layer2.0.conv1.weight': [8, 4],
        'layer2.0.conv2.weight': [8, 4],
        'layer2.1.conv1.weight': [8, 4],
        'layer2.1.conv2.weight': [8, 4],
        'layer2.2.conv1.weight': [8, 4],
        'layer2.2.conv2.weight': [8, 4],
        'layer2.3.conv1.weight': [8, 4],
        'layer2.3.conv2.weight': [8, 4],
        'layer2.4.conv1.weight': [8, 4],
        'layer2.4.conv2.weight': [8, 4],
        'layer3.0.conv1.weight': [8, 8],
        'layer3.0.conv2.weight': [8, 8],
        'layer3.1.conv1.weight': [8, 8],
        'layer3.1.conv2.weight': [8, 8],
        'layer3.2.conv1.weight': [8, 8],
        'layer3.2.conv2.weight': [8, 8],
        'layer3.3.conv1.weight': [8, 8],
        'layer3.3.conv2.weight': [8, 8],
        'layer3.4.conv1.weight': [8, 8],
        'layer3.4.conv2.weight': [8, 8]
    }

    ranks = {
        'layer1.0.conv1.weight': [1, 16, 16, 1],
        'layer1.0.conv2.weight': [1, 16, 16, 1],
        'layer1.1.conv1.weight': [1, 16, 16, 1],
        'layer1.1.conv2.weight': [1, 16, 16, 1],
        'layer1.2.conv1.weight': [1, 16, 16, 1],
        'layer1.2.conv2.weight': [1, 16, 16, 1],
        'layer1.3.conv1.weight': [1, 16, 16, 1],
        'layer1.3.conv2.weight': [1, 16, 16, 1],
        'layer1.4.conv1.weight': [1, 16, 16, 1],
        'layer1.4.conv2.weight': [1, 16, 16, 1],
        'layer2.0.conv1.weight': [1, 8, 32, 16, 4, 1],
        'layer2.0.conv2.weight': [1, 8, 16, 16, 8, 1],
        'layer2.1.conv1.weight': [1, 8, 16, 16, 8, 1],
        'layer2.1.conv2.weight': [1, 8, 16, 16, 8, 1],
        'layer2.2.conv1.weight': [1, 8, 16, 16, 8, 1],
        'layer2.2.conv2.weight': [1, 8, 16, 16, 8, 1],
        'layer2.3.conv1.weight': [1, 8, 16, 16, 8, 1],
        'layer2.3.conv2.weight': [1, 8, 16, 16, 8, 1],
        'layer2.4.conv1.weight': [1, 8, 16, 16, 8, 1],
        'layer2.4.conv2.weight': [1, 8, 16, 16, 8, 1],
        'layer3.0.conv1.weight': [1, 8, 40, 24, 8, 1],
        'layer3.0.conv2.weight': [1, 8, 27, 27, 8, 1],
        'layer3.1.conv1.weight': [1, 8, 27, 27, 8, 1],
        'layer3.1.conv2.weight': [1, 8, 27, 27, 8, 1],
        'layer3.2.conv1.weight': [1, 8, 27, 27, 8, 1],
        'layer3.2.conv2.weight': [1, 8, 28, 28, 8, 1],
        'layer3.3.conv1.weight': [1, 8, 28, 28, 8, 1],
        'layer3.3.conv2.weight': [1, 8, 29, 29, 8, 1],
        'layer3.4.conv1.weight': [1, 8, 24, 24, 8, 1],
        'layer3.4.conv2.weight': [1, 8, 15, 15, 8, 1]
    }

    in_ranks = {
        'layer1.0.conv1.weight': [16, 1],
        'layer1.0.conv2.weight': [16, 1],
        'layer1.1.conv1.weight': [16, 1],
        'layer1.1.conv2.weight': [16, 1],
        'layer1.2.conv1.weight': [16, 1],
        'layer1.2.conv2.weight': [16, 1],
        'layer1.3.conv1.weight': [16, 1],
        'layer1.3.conv2.weight': [16, 1],
        'layer1.4.conv1.weight': [16, 1],
        'layer1.4.conv2.weight': [16, 1],
        'layer2.0.conv1.weight': [16, 4, 1],
        'layer2.0.conv2.weight': [16, 8, 1],
        'layer2.1.conv1.weight': [16, 8, 1],
        'layer2.1.conv2.weight': [16, 8, 1],
        'layer2.2.conv1.weight': [16, 8, 1],
        'layer2.2.conv2.weight': [16, 8, 1],
        'layer2.3.conv1.weight': [16, 8, 1],
        'layer2.3.conv2.weight': [16, 8, 1],
        'layer2.4.conv1.weight': [16, 8, 1],
        'layer2.4.conv2.weight': [16, 8, 1],
        'layer3.0.conv1.weight': [24, 8, 1],
        'layer3.0.conv2.weight': [27, 8, 1],
        'layer3.1.conv1.weight': [27, 8, 1],
        'layer3.1.conv2.weight': [27, 8, 1],
        'layer3.2.conv1.weight': [27, 8, 1],
        'layer3.2.conv2.weight': [28, 8, 1],
        'layer3.3.conv1.weight': [28, 8, 1],
        'layer3.3.conv2.weight': [29, 8, 1],
        'layer3.4.conv1.weight': [24, 8, 1],
        'layer3.4.conv2.weight': [15, 8, 1]
    }

    out_ranks = {
        'layer1.0.conv1.weight': [1, 16],
        'layer1.0.conv2.weight': [1, 16],
        'layer1.1.conv1.weight': [1, 16],
        'layer1.1.conv2.weight': [1, 16],
        'layer1.2.conv1.weight': [1, 16],
        'layer1.2.conv2.weight': [1, 16],
        'layer1.3.conv1.weight': [1, 16],
        'layer1.3.conv2.weight': [1, 16],
        'layer1.4.conv1.weight': [1, 16],
        'layer1.4.conv2.weight': [1, 16],
        'layer2.0.conv1.weight': [1, 8, 32],
        'layer2.0.conv2.weight': [1, 8, 16],
        'layer2.1.conv1.weight': [1, 8, 16],
        'layer2.1.conv2.weight': [1, 8, 16],
        'layer2.2.conv1.weight': [1, 8, 16],
        'layer2.2.conv2.weight': [1, 8, 16],
        'layer2.3.conv1.weight': [1, 8, 16],
        'layer2.3.conv2.weight': [1, 8, 16],
        'layer2.4.conv1.weight': [1, 8, 16],
        'layer2.4.conv2.weight': [1, 8, 16],
        'layer3.0.conv1.weight': [1, 8, 40],
        'layer3.0.conv2.weight': [1, 8, 27],
        'layer3.1.conv1.weight': [1, 8, 27],
        'layer3.1.conv2.weight': [1, 8, 27],
        'layer3.2.conv1.weight': [1, 8, 27],
        'layer3.2.conv2.weight': [1, 8, 28],
        'layer3.3.conv1.weight': [1, 8, 28],
        'layer3.3.conv2.weight': [1, 8, 29],
        'layer3.4.conv1.weight': [1, 8, 24],
        'layer3.4.conv2.weight': [1, 8, 15]
    }
