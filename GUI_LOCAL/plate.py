# WXQ
# 时间： $(DATE) $(TIME)
class plate():
    def __init__(self, num, corename,effective_size, plate_type, mod_num, seam, blood, scale, machineid,jobNoPrefix):
        self.num = num
        self.corename = corename
        self.machineid = machineid
        self.effective_size = effective_size  # 大版的尺寸，长宽
        self.plate_type = plate_type  # 版的类型
        self.mod_num = mod_num  # 大版的模数
        self.seam = seam  # 咬口尺寸
        self.blood = blood  # 出血尺寸
        self.scale = scale
        self.jobNoPrefix = jobNoPrefix # 订单类型

