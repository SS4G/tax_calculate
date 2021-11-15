def calcPayableValue(monthlySalary, mounthCnt=12):
    """
    计算应纳税所得额
    1. 减去 每月5k 免税额度
    2. 减去五险一金
    3. 减去专项扣除
    """
    total = monthlySalary * mounthCnt
    #socialInsuranceMax = 28221
    SOCIAL_INSURANCE_MAX = 28221 # 北京最高社保基数
    Basic_retirement_insurance_frac = 0.08 # 退休个人部分
    Basic_medical_insurance_frac = 0.02 # 医疗保险个人部分
    Unemployment_insurance_frac = 0.002 # 失业金个人
    Provident_Fund_frac = 0.12 # 公积金
    monthly_basic_social_insurance_payable = min(SOCIAL_INSURANCE_MAX, monthlySalary) # 真实社保基数
    social_insurance_value = 12 * monthly_basic_social_insurance_payable * \
      (Basic_retirement_insurance_frac + Basic_medical_insurance_frac + Provident_Fund_frac + Unemployment_insurance_frac)
    Special_deduction = 1000 * 12 # 专项扣除 房贷
    Tax_exemption = 5000 * 12 # 基础免税额度

    payable = total - Tax_exemption - Special_deduction - social_insurance_value
    return payable

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
            return payable_val * rank[i][1] - rank[i][2]
    return payable_val * rank[7][1] - rank[7][2]

payable_val = calcPayableValue(42000, 15)
taxVal = calcTax(payable_val)

