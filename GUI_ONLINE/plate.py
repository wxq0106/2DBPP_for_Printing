class plate():
    def __init__(self, num, corename,effective_size, plate_type, mod_num, seam, blood, scale, machineid,jobNoPrefix,state):
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
        self.state = state#是否被选中
        self.duplex_print_type = 0 #0为双面，1为单面
        self.plating ="正反"


