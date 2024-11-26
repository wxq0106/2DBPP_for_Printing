#WXQ
#时间： $(DATE) $(TIME)
from PyPDF3 import PdfFileReader
# import urllib.request
# from urllib.parse import quote
# import io
import subprocess
#
# # url = 'http://192.168.1.66:801\\审稿-已审文件\\20231020\\23102000115-06880-_网付231020003701_乐山传单105g5千张@1款5000张-206x281_105克A4双面5000张1M.pdf'
# # # url = 'http://192.168.1.66:801/审稿-已审文件/20231020/23102000115-06880-_网付231020003701_乐山传单105g5千张@1款5000张-206x281_105克A4双面5000张1M.pdf'
# # url = url.replace("\\","/")
# encoded_path = quote('http://192.168.1.66:801/审稿-已审文件/20231020/23102000210-07850-高新区晨希 206x281mm 烤全羊宣传单-105克A4双面1千张1M.pdf')
# url = f'http://192.168.1.66:801{encoded_path}'
# urllib.request.urlopen(url)
result = subprocess.run(['CorelDrawPlating.exe'], capture_output=True, text=True)
print(result.stdout)