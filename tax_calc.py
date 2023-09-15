def calcPayableValue(monthlySalary, mounthCnt=12, nianzhongjiang_month=0):
    """
    计算应纳税所得额
    1. 减去 每月5k 免税额度
    2. 减去五险一金
    3. 减去专项扣除
    """
    total = monthlySalary * mounthCnt

    # 社保扣除
    shebao_base = 33387 # 北京最高社保基数
    yanglao_rate = 0.08 # 退休个人部分
    yibao_rate = 0.02 # 医疗保险个人部分
    shiye_rate = 0.002 # 失业金个人
    gongjijin_rate = 0.12 # 公积金
    shebao_base_real = min(shebao_base, monthlySalary) # 真实社保基数
    shebao_kouchu_value = 12 * shebao_base_real * \
      (yanglao_rate + yibao_rate + shiye_rate + gongjijin_rate)

    # 公积金收入
    gongjijin_income = shebao_base_real * gongjijin_rate * 2 * 12
    
    # 专项扣除
    special_kouchu_value = 1000 * 12 # 专项扣除 房贷
    tax_kouchu_value = 5000 * 12 # 基础免税额度

    # 计税金额
    tax_calc_val = total - tax_kouchu_value - special_kouchu_value - shebao_kouchu_value
    tax_value = calcTax(tax_calc_val)

    nianzhongjian_total = nianzhongjiang_month * monthlySalary
    nianzhongjiang_income = nianzhongjian_total - calcNianzhongTax(nianzhongjian_total)

    non_tax_income = total - tax_value + gongjijin_income + nianzhongjiang_income

    return tax_calc_val, non_tax_income, gongjijin_income, nianzhongjian_total

def calcTax(payable_val):
    """
    根据应纳税所得额 计算个税
    只支持合并计税方式
    """
    rank = [
        (0, 0.03, 0),
        (36000, 0.1, 2520),
        (144000, 0.2, 16920),
        (300000, 0.25, 31920),
        (420000, 0.3, 52920),
        (660000, 0.35, 85920),
        (960000, 0.45, 181920),
    ]
    for i in range(len(rank) - 1):
        if rank[i + 1][0] > payable_val >= rank[i][0]:
            print(rank[i][1] )
            return payable_val * rank[i][1] - rank[i][2]
    return payable_val * rank[7][1] - rank[7][2]


def calcNianzhongTax(payable_val):

    yuedu_jiangjin = payable_val / 12
    # 低 高 税率 速算扣除
    level = [
        (0,     3000,  0.03, 0),
        (3000,  12000, 0.1,  210),
        (12000, 25000, 0.2,  1410),
        (25000, 35000, 0.25, 2660),
        (35000, 55000, 0.3,  44100),
        (55000, 80000, 0.35, 7160),
        (80000, 1e7,   0.45, 15160),
    ]

    for i, level in enumerate(level):
        if level[0] <= yuedu_jiangjin < level[1]:
            return (yuedu_jiangjin * level[2] - level[3]) * 12
    return -1


tax_calc_val, non_tax_income, gongjijin, nianzhongjian = calcPayableValue(52000, nianzhongjiang_month=3)
print("公积金={}".format(gongjijin))
taxVal = calcTax(tax_calc_val)
print("纳税金={}".format(taxVal))
print("年终奖={}".format(nianzhongjian))
print("税后收入={}".format(non_tax_income - taxVal))

