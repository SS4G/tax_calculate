def calcPayableValue(monthlySalary, nianzhongjiang_month=0):
    """
    计算应纳税所得额
    1. 减去 每月5k 免税额度
    2. 减去五险一金
    3. 减去专项扣除
    """

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
    print("公积金={}".format(gongjijin_income))
    
    # 专项扣除
    special_kouchu_value = 1000 * 12 # 专项扣除 房贷
    tax_kouchu_value = 5000 * 12 # 基础免税额度

    # 计税金额
    tax_calc_val = 12 * monthlySalary - tax_kouchu_value - special_kouchu_value - shebao_kouchu_value
    print("算税金额={}".format(tax_calc_val))
    tax_value = calcTax(tax_calc_val)
    print("正常税={}".format(tax_value))
    nianzhong_tax = calcNianzhongTax(nianzhongjiang_month * monthlySalary)

    print("年终税={}".format(nianzhong_tax))
    print("税前总收入={}".format((12 + nianzhongjiang_month) * monthlySalary))

    total_income = (12 + nianzhongjiang_month) * monthlySalary - tax_value - nianzhong_tax - shebao_kouchu_value + gongjijin_income
    total_tax = nianzhong_tax + tax_value
    return total_income, total_tax

def calcTax(payable_val):
    """
    根据应纳税所得额 计算个税
    只支持合并计税方式
    """
    levels = [
        (0,      36000, 0.03, 0),
        (36000,  144000,  0.1, 2520),
        (144000, 300000, 0.2, 16920),
        (300000, 420000, 0.25, 31920),
        (420000, 660000, 0.3, 52920),
        (660000, 960000, 0.35, 85920),
        (960000, 1e7,    0.45, 181920),
    ]

    for i, level in enumerate(levels):
        if level[0] <= payable_val < level[1]:
            print("level={}".format( level[2]))
            return (payable_val * level[2] - level[3]) 
    return -1


def calcNianzhongTax(payable_val):

    yuedu_jiangjin = payable_val / 12
    # 低 高 税率 速算扣除
    levels = [
        (0,     3000,  0.03, 0),
        (3000,  12000, 0.1,  210),
        (12000, 25000, 0.2,  1410),
        (25000, 35000, 0.25, 2660),
        (35000, 55000, 0.3,  44100),
        (55000, 80000, 0.35, 7160),
        (80000, 1e7,   0.45, 15160),
    ]

    for i, level in enumerate(levels):
        if level[0] <= yuedu_jiangjin < level[1]:
            return (yuedu_jiangjin * level[2] - level[3]) * 12
    return -1


total_income, total_tax = calcPayableValue(42000, nianzhongjiang_month=3)
#print("公积金={}".format(gongjijin))
#taxVal = calcTax(tax_calc_val)
print("纳税金={}".format(total_tax))
#print("年终奖={}".format(nianzhongjian))
print("税后收入(月收入+年终奖+公积金公司部分)={}".format(total_income))

