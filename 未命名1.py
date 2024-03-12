# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 23:58:23 2024

@author: zihan
"""

import random
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif']=['FangSong']

# 初始概率和数量设置
initial_probabilities = {'owl': 0.02, 'wand': 0.015, 'clothes': 0.012, 'furniture_set': 0.003, 
                         'coins': 0.17, 'keys_silver': 0.16, 'potion': 0.16, 
                         'furniture': 0.16, 'stones': 0.17, 'keys_gold': 0.13}
initial_numbers = {'owl': 1, 'wand': 1, 'clothes': 1, 'furniture_set': 1,
                   'coins': 18, 'keys_silver': 10, 'potion': 5,
                   'furniture': 25, 'stones': 18, 'keys_gold': 10}

# 奖品分类列表
big_prizes = ['owl', 'wand', 'clothes', 'furniture_set']
normal_prizes = ['coins', 'keys_silver', 'potion', 'furniture', 'stones', 'keys_gold']

# 规范化概率的函数
def normalize_probabilities():
    total = sum(initial_probabilities.values())
    if total!= 0:
        for prize in initial_probabilities:
            initial_probabilities[prize] /= total

# 一次抽取后调整概率的函数
def adjust_probabilities(prize_drawn):
    big_prizes_left = 0
    normal_prizes_left = 0
    
    #计算剩余奖励数量
    for prize in big_prizes:
        if initial_numbers[prize]!=0:
            big_prizes_left += 1
    for prize in normal_prizes:
        if initial_numbers[prize]!=0:
            normal_prizes_left += 1
    if prize_drawn in big_prizes:
        adjustment = initial_probabilities[prize_drawn] / max(1,big_prizes_left)
        for prize in big_prizes:
            if prize != prize_drawn and initial_numbers[prize] > 0:
                initial_probabilities[prize] += adjustment
    
    #计算调整概率大小
    elif prize_drawn in normal_prizes and initial_numbers[prize_drawn]==0:
        big_adjustment = 0.01 / big_prizes_left
        normal_adjustment = (initial_probabilities[prize_drawn] - 0.01) / max(1, normal_prizes_left)
        for prize in normal_prizes:
            if prize != prize_drawn and initial_numbers[prize] > 0:
                initial_probabilities[prize] += normal_adjustment
        for prize in big_prizes:
            initial_probabilities[prize] += big_adjustment
    initial_probabilities[prize_drawn] = 0 if initial_numbers[prize_drawn] == 0 else initial_probabilities[prize_drawn]
    normalize_probabilities()

def repeat_draw_gifts(experiments, total_draws, desired_item):
    # 抽中特定奖品的次数
    desired_item_draws = 0

    for experiment in range(experiments):
        #print(f"实验 #{experiment + 1}")

        # 重置奖品数量和概率
        reset_initial_conditions()

        # 执行抽奖
        did_draw_desired_item = draw_gifts(total_draws, desired_item)

        # 如果这次实验中抽中了特定奖品，更新计数器
        if did_draw_desired_item:
            desired_item_draws += 1

        print(f"实验 {experiment + 1} 结束\n")

    #print(f"在 {experiments} 次实验中，共有 {desired_item_draws} 次抽中了 '{desired_item}'。")
    return desired_item_draws

def reset_initial_conditions():
    global initial_numbers, initial_probabilities
    # 重置奖品数量
    initial_numbers = {'owl': 1, 'wand': 1, 'clothes': 1, 'furniture_set': 1,
                       'coins': 18, 'keys_silver': 10, 'potion': 5,
                       'furniture': 25, 'stones': 18, 'keys_gold': 10}
    # 重置概率
    initial_probabilities = {'owl': 0.02, 'wand': 0.015, 'clothes': 0.012, 'furniture_set': 0.003, 
                             'coins': 0.17, 'keys_silver': 0.16, 'potion': 0.16, 
                             'furniture': 0.16, 'stones': 0.17, 'keys_gold': 0.13}
    normalize_probabilities()


def draw_gifts(total_draws, desired_item):
    #prizes_drawn = {}
    #draw_count = 0
    did_draw_desired_item = False  

    if total_draws >=89:
        did_draw_desired_item = True
    
    else:
        for draw in range(total_draws):
            #draw_count += 1
            prize = random.choices(list(initial_probabilities.keys()), weights=initial_probabilities.values(), k=1)[0]
            if initial_numbers[prize] > 0:
                #print(f"抽中: {prize}")
                initial_numbers[prize] -= 1
                #prizes_drawn[prize] = draw_count
                adjust_probabilities(prize)
                if prize == desired_item:
                    did_draw_desired_item = True
                if all(initial_numbers[big_prize] == 0 for big_prize in big_prizes):
                    break

    return did_draw_desired_item

def prob_distr(desired_item,precise):
    experiments = precise
    total_draws_array = np.arange(0,89,1)
    probs = np.array([])
    for i in total_draws_array:
        desired_item_draws =repeat_draw_gifts(experiments, i, desired_item)
        prob = desired_item_draws/experiments
        probs = np.append(probs,prob)
    return probs

def plot_distr():
    x1 = np.arange(0,89,1)  
    y1 = prob_distr('clothes', 10000)
    y2 = prob_distr('furniture_set', 10000)
    y3 = prob_distr('owl', 10000)
    y4 = prob_distr('wand', 10000)

    plt.plot(x1,y1,color='red',label='服装')
    plt.plot(x1,y2,color='green',label='家具套装')
    plt.plot(x1,y3,color= 'aquamarine',label = '猫头鹰')
    plt.plot(x1,y4,color='black',label='魔杖')
    plt.title('各奖品数量随抽奖次数改变的抽中概率变化')
    plt.xlim(0,90)
    plt.ylim(0,1)
    plt.legend()
    
plot_distr()