# work2关联规则挖掘  

## 对数据集进行处理，转换成适合关联规则挖掘的形式；  
读取数据集，拼接属性和属性值,输出新的数据集； 创建集合 C1，即对新的数据集进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset。  
## 找出频繁项集；  
## 导出关联规则，计算其支持度和置信度  
## 对规则进行评价，可使用Lift，也可以使用教材中所提及的其它指标  
