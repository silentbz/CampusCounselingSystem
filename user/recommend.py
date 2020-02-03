import numpy as np
# from texttable import Texttable

# 生成随机的10*10 0-1矩阵
# user_list = []
# for m in range(11):
#     user = np.random.randint(0,2,10)
#     user_list.append(user)
#     if m!=0:
#         print(user_list[m])
# user_array = np.array(user_list)

def max_number(a,b):
    if a>b:
        return a
    return b

# 得到最为相似的用户id
sim_user_dict = {}
def get_sim_user_id(users_array,input_user_id,users_length):

    output_user_id = 0
    max_num = 0.0
    sum_res_weight = 0.0 # 计算权重和
    for k in range(1,users_length):

        if k!=input_user_id:
            res = users_array[input_user_id] - users_array[k]
            sum_res_weight = sum_res_weight+np.sqrt(np.sum(res ** 2))
    print("总的权重和为%f"%sum_res_weight)
    for i in range(1,users_length):
        print("loop %d-------------------------------------------------------"%i)
        if i!=input_user_id:
            res = users_array[input_user_id] - users_array[i]
            # print("user%d - user%d的结果为：" % (input_user_id, i))
            # print(res)
            # print("求取平方和为：")
            # print(np.sum(res ** 2))  # 求取平方和
            # print("user%d与user%d的相似度为：" % (input_user_id, i))
            # 计算当前权重
            temp_weight = np.sqrt(np.sum(res ** 2))
            # 自定义阈值 temp_weight /(2.5*sum_res_weight)
            sim = 1 / (1 +temp_weight /(2.5*sum_res_weight))  # 求取相似度
            print(sim)
            sim_user_dict[str(i)] = sim
            max_num = max_number(max_num, sim)
            if max_num<=sim:
                output_user_id = i
    #print("最大相似度为%f" % max_num)
    #print("最大相似度的user_id为%d"%output_user_id)

    return output_user_id
if __name__ == '__main__':
    user0 = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
    user1 = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1]
    user2 = [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    user3 = [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]
    user4 = [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1]
    users = [user0, user1, user2, user3, user4]
    # print(users.__len__())  # 得到长度
    # array = np.array([[1,0 ,1 ,1,0,1,1,1,0,1,0,1],
    #                 [1 ,0 ,1, 1,0,1,1,1,0,1,1,1],
    #                 [1, 0 ,0 ,0,0,1,1,1,0,1,0,1],
    #                 [1 ,1, 0 ,0,0,1,1,1,0,1,0,1]])
    # array = np.array([user1,user2,user3,user4])
    user_array = np.array(users)
    input_the_user_id = input('输入用户id 找出最为相似的用户id:')
    result_user_id = get_sim_user_id(user_array,int(input_the_user_id),user_array.__len__())
    print("user%d最大相似度的user_id为%d"%(int(input_the_user_id),result_user_id))
    for k in sim_user_dict.items():
        print(k)
    # TEST
    # user_list = []
    # user_list.append(0)
    # user_list.append(0)
    # user_list.append(1)
    # users_list = []
    # users_list.append(user_list)
    # print(users_list)
    pass
# for i in range(4):
#
#     if i + 1 < 4:
#         res = user_array[i + 1] - user_array[i]
#         print("第%d行 - 第%d行结果为：" % (i + 2, i + 1))
#         print(res)
#         print("求取平方和为：")
#         print(np.sum(res ** 2))
#         print("user%d与user%d的相似度为：" % (i + 2, i + 1))
#         sim = 1 / (1 + np.sum(res ** 2))
#         print(sim)
#         max_num = max_number(max_num, sim)
# print("最大相似度为%f" % max_num)
# table = Texttable()
# table.set_deco(Texttable.HEADER)
# table.set_cols_dtype(['t',  # text
#                       'i',  # float (decimal)
#                       'i',  # float (exponent)
#                       'i',  # integer
#                       'i']) # automatic
# # c 表示center 居中 l表示居左 r表示居右
# table.set_cols_align(["c", "c", "c", "c", "c"])
# table.add_rows([["users",  "item1", "item2", "item3", "item4"],
#                 ["user1",  1,1,0,1],
#                 ["user2",  0,1,1,1],
#                 ["user3",  0,1,0,1],
#                 ["user4",  0,1,0,1]])
# print(table.draw())

# table = Texttable()
# table.set_deco(Texttable.HEADER)
# table.set_cols_dtype(['t',  # text
#                       'f',  # float (decimal)
#                       'e',  # float (exponent)
#                       'i',  # integer
#                       'a',
#                       't',  # text
#                       'f',  # float (decimal)
#                       'e',  # float (exponent)
#                       'i',  # integer
#                       'a'
#                       ])  # automatic
# table.set_cols_align(["l", "r", "r", "r","l", "r", "r", "r"])
#
# table.add_rows([
#                 ["user1", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user2", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user3", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user4", 5e-78, 5e-78, 89.4, .000000000000128,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user5", .023, 5e+78, 92., 12800000000000000000000,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user6", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user7", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023],
#                 ["user8", 67.5434, .654, 89.6, 12800000000000000000000.00023,67.5434, .654, 89.6, 12800000000000000000000.00023]])
# print(table.draw())
