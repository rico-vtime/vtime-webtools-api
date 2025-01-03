import numpy as np
# from matplotlib import pyplot as plt
# from pandas import DataFrame


def calculate_sma(prices, window_size):
    '''
        均线计算
    '''
    # 这行代码是在计算简单移动平均（SMA）时创建一个权重数组，其目的是为了在滑动窗口内对所有价格应用相同的权重。让我们逐步分解这行代码：
    # np.ones(window_size): 这部分调用NumPy的ones函数，创建一个长度为window_size的数组，数组中的所有元素都是1。例如，如果window_size是5，那么这个函数将返回一个数组[1, 1, 1, 1, 1]。
    # / window_size: 这部分将上一步创建的全1数组中的每个元素都除以窗口大小window_size。这样做的目的是为了生成一个平均权重数组，使得每个元素的权重相等，且所有权重之和为1。
    #   继续上面的例子，如果window_size是5，那么每个元素将被除以5，结果是数组[0.2, 0.2, 0.2, 0.2, 0.2]。
    # 将这个权重数组应用到价格数据上，可以确保在计算滑动平均时，窗口内的每个价格都被赋予了相同的权重（在这个例子中，每个价格的权重都是0.2）。
    # 这就是计算简单移动平均的本质：在每个窗口内，所有价格对计算结果的贡献都是相等的。
    weights = np.ones(window_size) / window_size
 
    # 这行代码使用NumPy的convolve函数来计算价格数组prices和权重数组weights的卷积，模式设置为'valid'。
    #       让我们分解这行代码以便更好地理解它的工作原理：
    # np.convolve: 这是NumPy库中的一个函数，用于计算两个序列的卷积。在这个上下文中，它被用来计算简单移动平均（SMA）。
    # prices: 这是一个NumPy数组，包含你想要计算移动平均的数据点，通常是一系列的股票价格。
    # weights: 这是一个与prices数组长度相同的NumPy数组，表示每个价格点在计算平均时的权重。
    #       在简单移动平均的情况下，所有的权重都是相等的，即每个元素的值都是1/window_size，其中window_size是移动平均的窗口大小。
    # 'valid': 这是np.convolve函数的一个模式参数，它决定了输出数组的形状。当设置为'valid'时，只有那些不需要数组边缘外的元素就能计算的卷积结果会被返回。
    #       这意味着，如果你的prices数组长度为N，weights数组长度为W，那么返回的卷积结果数组长度将为N-W+1。
    # 这是因为在计算每个窗口的平均值时，只考虑了完全覆盖窗口的情况，没有进行任何形式的边缘扩展。
    # 简单来说，这行代码通过对每个窗口内的价格进行加权平均（在这个例子中，权重是相等的），来计算一系列价格的简单移动平均。
    # 'valid'模式确保了只有在没有越界的情况下才计算平均值，从而保证了计算结果的准确性。
    sma = np.convolve(prices, weights, 'valid')
    sma = np.round(sma, 2)
    return sma

