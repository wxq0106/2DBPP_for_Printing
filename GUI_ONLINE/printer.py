# WXQ
# 时间： $(DATE) $(TIME)
class printer():
    def __init__(self, name, state, work_time, plates, plate_size, duplex_print_type, modelid, remain,ps_name):
        self.name = name
        self.sate = state
        self.work_time = work_time
        self.plates = plates
        self.plate_size = plate_size
        self.plates_remain = remain
        self.duplex_print_type = duplex_print_type
        self.modelid = modelid
        self.ps_name = ps_name #大版名字

