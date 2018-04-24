# work2关联规则挖掘  

## 对数据集进行处理，转换成适合关联规则挖掘的形式；  
    读取数据集，拼接属性和属性值,输出新的数据集； 创建集合 C1，即对新的数据集进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset。  
## 找出频繁项集； 
    如果某个项集是频繁的，那么他的子集也是频繁的；反之，如果如果项集不是频繁项集，那么他的超集也不是频繁项集。  
    使用Apriori算法从候选项集中找出支持度support大于minSupport的频繁项集；
    输入频繁项集列表 Lk 与返回的元素个数 k，然后输出候选项集 Ck  

## 导出关联规则，计算其支持度和置信度  
    首先构建集合 C1，然后扫描数据集来判断这些只有一个元素的项集是否满足最小支持度的要求。那么满足最小支持度要求的项集构成集合 L1。然后 L1 中的元素相互组合成 C2，C2 再进一步过滤变成 L2，然后以此类推，知道 CN 的长度为 0 时结束，即可找出所有频繁项集的支持度。  
    支持度定义: a -> b = support(a | b) / support(a). 假设  freqSet = frozenset([1, 3]), conseq = [frozenset([1])]，那么 frozenset([1]) 至 frozenset([3]) 的可信度为 = support(a | b) / support(a) = supportData[freqSet]/supportData[freqSet-conseq] = supportData[frozenset([1, 3])] / supportData[frozenset([1])]。记录可信度大于最小可信度（minConference）的集合。  
    递归计算频繁项集的规则，H[0] 是 subSet 的元素组合的第一个元素，并且 H 中所有元素的长度都一样，长度由 creatCk(H, m+1) 这里的 m + 1 来控制；该函数递归时，H[0] 的长度从 1 开始增长 1 2 3 ...；假设 subSet = frozenset([2, 3, 5]), H = [frozenset([2]), frozenset([3]), frozenset([5])]；那么 m = len(H[0]) 的递归的值依次为 1 2；在 m = 2 时, 跳出该递归。假设再递归一次，那么 H[0] = frozenset([2, 3, 5])，subSet = frozenset([2, 3, 5]) ，没必要再计算 subSet 与 H[0] 的关联规则了。  
    
 
## 对规则进行评价，可使用Lift，也可以使用教材中所提及的其它指标  
