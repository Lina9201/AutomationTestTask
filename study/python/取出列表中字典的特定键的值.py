#-*-coding:utf-8-*-
##创建字段
vdc_list = [{"name": "du1", "description": "备注"},{"name": "du2", "description": "备注"},{"name": "du3", "description": "备注"}]
##创建空列表
vdc_listname=[]
#将字典中键和值循环取出添加到列表中能够
for i in vdc_list:
    vdc_listname.append(i["name"])
    # for k in i:
    #     vdc_listname.append(i["name"])
print(vdc_listname)