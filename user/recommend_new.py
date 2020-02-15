import numpy as np
import time
import datetime

# 生成随机的10*10 0-1矩阵
# user_list = []
# for m in range(11):
#     user = np.random.randint(0,2,10)
#     user_list.append(user)
#     if m!=0:
#         print(user_list[m])
# user_array = np.array(user_list)

def max_number(a, b):
    if a > b:
        return a
    return b




def get_sim_users_id(users_array, input_user_id, users_length):
    # 得到 相似的用户id序列
    sim_user_dict = {}
    # 最大相似的用户id
    max_sim_user_id = 0
    max_num = 0.0
    sum_res_weight = 0.0  # 计算权重和
    for k in range(1, users_length):

        if k != input_user_id:
            res = users_array[input_user_id] - users_array[k]
            sum_res_weight = sum_res_weight + np.sqrt(np.sum(res ** 2))
    #print("总的权重和为%f" % sum_res_weight)
    for i in range(1, users_length):
        #print("loop %d-------------------------------------------------------" % i)
        if i != input_user_id:
            res = users_array[input_user_id] - users_array[i]
            # print("user%d - user%d的结果为：" % (input_user_id, i))
            # print(res)
            # print("求取平方和为：")
            # print(np.sum(res ** 2))  # 求取平方和
            # print("user%d与user%d的相似度为：" % (input_user_id, i))
            # 计算当前权重
            temp_weight = np.sqrt(np.sum(res ** 2))


            # 自定义阈值 temp_weight /(2.6*sum_res_weight)
            sim = 1.0 / (1 + temp_weight / (2.6 * sum_res_weight))  # 求取相似度
            #print(sim)
            sim_user_dict[str(i)] = sim
            max_num = max_number(max_num, sim)
            if max_num <= sim:
                max_sim_user_id = i
    # print("最大相似度为%f" % max_num)
    # print("最大相似度的user_id为%d"%output_user_id)
    # sim_user_dict['max_sim_user_id'] = max_sim_user_id
    # 根据相似度降序对用户进行排序
    sim_user_dict = sorted(sim_user_dict.items(), key=lambda x: x[1], reverse=True)
    return sim_user_dict


if __name__ == '__main__':

    user0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    user1 = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
    user2 = [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1]
    user3 = [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
    user4 = [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1]
    users = [user0, user1, user2, user3, user4]

    user_array = np.array(users)
    # Use user_array[0].any()==0 来判断第一行元素是否全部等于0
    if user_array[0].any() ==0:
        print("No")
    input_the_user_id = input('输入用户id 找出最为相似的用户id:')
    # result_user_id = get_sim_user_id(user_array, int(input_the_user_id), user_array.__len__())
    # rint("user%d最大相似度的user_id为%d" % (int(input_the_user_id), result_user_id))
    start = datetime.datetime.now()






    sim_users_result = get_sim_users_id(user_array, int(input_the_user_id), user_array.__len__())
    print(type(sim_users_result))
    # 根据相似度降序排序
    # sim_users_result = sorted(sim_users_result.items(), key=lambda x: x[1], reverse=True)
    #print(sorted(sim_users_result.items(), key=lambda x: x[1], reverse=True))

    for key,value in sim_users_result:
         print(key+"----->"+str(value))
    sim_user_dict = {"1":1}
    print(len(sim_user_dict))
    sim_user_dict['2'] = 2
    print(len(sim_user_dict))
    end = datetime.datetime.now()
    print(type(end-start))

