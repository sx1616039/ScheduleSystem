import os
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optimizer
from torch.distributions import Categorical
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 版权声明：
# 本程序的详细中文注释请参考
# 黄小平，王岩，缪鹏程.粒子滤波原理及应用[M].电子工业出版社，2017.4
# 书中有原理介绍 + 例子 + 程序 + 中文注释
# 如果此程序有错误，请对提示修改
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 函数功能：实现随机重采样算法
# 输入参数：weight为原始数据对应的权重大小
# 输出参数：outIndex是根据weight对inIndex筛选和复制结果
def randomR(wt):
    L = len(wt)
    outIndex = np.zeros(L, dtype=int)
    u = np.random.uniform(0, 1, L)
    u = sorted(u)
    cdf = np.cumsum(wt)
    i = 0
    for j in range(L):
        while i < L and (u[i] <= cdf[j]):
            outIndex[i] = j
            i = i + 1
    return outIndex

if __name__ == '__main__':
    # ------------------------------------------------基于粒子滤波的模型与数据融合 - ---------------------------------------- #
    # 初始化相关参数
    
    np.random.seed(1)  #为了保证每次运行结果一致，给定随机数的种子点
    T = 60  # 有多少组数据（采样点数）
    dt = 3  #切一刀多长时间（采样周期）
    numSamples = 5000  #粒子数量，越多精度高速度慢
    # 观测值，CNN输出的结果
    # 两个方程，一个观测方程一个状态方程
    # Z就是Yk是CNN的值（Yk是观测方程）
    Z = [0.07398,
         0.09435,
         0.09653,
         0.0905,
         0.09722,
         0.11578,
         0.10819,
         0.13082,
         0.1251,
         0.12709,
         0.14962,
         0.11175,
         0.11187,
         0.10825,
         0.12825,
         0.09962,
         0.14044,
         0.10161,
         0.15802,
         0.10617,
         0.12637,
         0.10666,
         0.1572,
         0.15193,
         0.12578,
         0.14802,
         0.11924,
         0.17866,
         0.16618,
         0.16992,
         0.15644,
         0.1447,
         0.1665,
         0.16138,
         0.19267,
         0.17706,
         0.17922,
         0.16494,
         0.18974,
         0.17141,
         0.21751,
         0.20541,
         0.2029,
         0.22321,
         0.2089,
         0.21006,
         0.20428,
         0.19455,
         0.19089,
         0.22073,
         0.24112,
         0.22274,
         0.23523,
         0.23003,
         0.24403,
         0.22036,
         0.25562,
         0.25918,
         0.24155,
         0.27275,
         ]  #cnn的值
    # 重采样，随机重采样，知道原理就行，另一个文件就是随机重采样的算法（根据ResampleStrategy参数设置1 - 4之间的整数，
    # 分别可以选用随机重采样、系统重采样、残差重采样及多项式重采样策略）
    ResampleStrategy = 1
    # 生成服从N(0.0257, 0.0907 ^ 2)的初始测量噪声分布 （高斯分布）   #v和w是噪声，v是有限元做出的所有的值和实验的值，0.0257 是均值，
    # 0.0907 是标准差，0.0257 是计算mse误差（每一个实验值和仿真值都有一个mse误差，计算这些误差的均值），
    # 0.0907 是标准差（每一个实验值和仿真值都有一个mse误差，计算这些误差的标准差），excel算就行，假设所有的都服从高斯分布
    v = np.random.normal(0.000127, 0.01162, numSamples)
    # 生成一个服从N(0.001, 0.029 ^ 2) 的观测噪声   #CNN的 w是观测方程中的θk w是cnn和实际
    # --粒子滤波器初始化，需要设置用于存放滤波估计状态，粒子集合，权重等数组 - -   #  #产生一个装数据的地方
    w = np.random.normal(0.000551, 0.02429, numSamples)
    Xpf = np.zeros([numSamples, T], dtype=float)  #粒子滤波估计状态
    Xparticles = np.zeros([numSamples, T], dtype=float)  #粒子集合
    Zpre_pf = np.zeros([numSamples, T], dtype=float)  #粒子滤波观测预测值
    weight = np.zeros([numSamples, T], dtype=float)  #权重初始化
    # 给定状态和观测预测的初始采样
    Xpf[:, 0] = np.random.uniform(0.04, 0.046, numSamples) + v[:, 0]  #粒子滤波要先求一个初始分布，从上一时刻推下一时刻，要定义X0时刻，0
    # 其实代表1，加1时刻的噪声。0.04，0.046
    # 是有限元第一个六分钟之间的，就是有限元第一个可以量到的磨损值
    Zpre_pf[:, 0] = Xpf[:, 0]+w[:, 0]  #从初始状态中采样出k = 1 时刻的粒子
    # Yk的初始值 + 误差
    # Yk是  k = 1  时刻的磨损＋k = 1 时刻的误差，这一步就是Yk观测方程的初始化
    # 更新与预测过程    （这一步就是开始计算了）
    for i in range(T-1):
        k = i+1
        #第一步：粒子集合采样过程
        for j in range(numSamples):  #得到5000个X2，.......，得到5000个X53       （产生了5000个粒子，）
            net = 0.0907 * randn  #可调节的net（大小与测量噪声标准差相关）
            Xparticles[i][k] = 0.3564 * pow(Xpf[i][k - 1], 3) + Xpf[i][k - 1] + net  #粒子从近似分布q(k)
            # 中进行采样，其中q(k) = p(x(k) | x(k - 1))
            #第二步：对粒子集合中的每个粒子计算其重要性权重
        for m in range(numSamples):   #计算产生的5000个值的权重，权重是和观测值比较得出来的
            qq = 0.029 * randn;
            Zpre_pf[i][k] = Xparticles[i, k] + qq
            weight[i][k] = np.exp(pow(-0.5 * 0.029, -1) * pow((Z[k][1] - Zpre_pf[i][k]), 2)) #z是观测值 pf是粒子滤波融合的值
        weight[:, k] = weight[:, k] / sum(weight[:, k])  #权值归一化
        #第三步：选择采样策略   #重采样，筛选出权重大的粒子，权重小的粒子是无效粒子
        if ResampleStrategy == 1:   #通过重采样，选出权重大的粒子，删除权重小的粒子，最后留下的粒子，把这些粒子求个均值
            outIndex = randomR(weight[:, k])
            #第四步：根据重采样得到的索引，去挑选对应的粒子，重构的集合便是滤波后的状态集合对这个状态集合求均值，就是最终的目标状态 #
            Xpf[:, k] = Xparticles[outIndex, k]
    #计算后验均值估计、最大后验估计及估计方差
    Xmean_pf = np.mean(Xpf)  #后验均值的估计，即上面的第四步，也即粒子滤波估计的最终状态
    #  #  #  #  #  #  #  #  #  #-------------预测刀具剩余使用寿命 - ----------   #  #  #  #  #  #  #  #  ##

