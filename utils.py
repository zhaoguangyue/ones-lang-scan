import os
import json
import pandas as pd


# 获取lang对应的路径
def getLangPath(fileList, lang):
    for p in fileList:
      if os.path.basename(p).startswith(lang):
        return p

# 根据path获取lang
def getLang(path):
    fileName = os.path.basename(path)	
    lang = os.path.splitext(fileName)[0]
    return lang

# 获取json文件的内容
def getJsonFileContent(path):
    file = open(path, 'r')
    return json.load(file) 
  
def generateLangData(data, result, lang, isSource=False):
    for key, value in data.items():
      if isSource:
        result[key] = {'key': key, lang: value}
      elif key in result: 
        result[key][lang] = value
    return result


def generateExcel(sheetDataList):
    with pd.ExcelWriter("./excel/rdLang.xlsx") as writer:
      for sheetName, sheetData in sheetDataList.items():
        print(sheetName)
        df = pd.DataFrame(sheetData)
        df.to_excel(writer, sheet_name=sheetName, index=False)


def generateConfig(config):
    file = open('./scripts/config.json', 'w')
    file.write(json.dumps(config, indent=4, ensure_ascii=False))
    file.close()
    os.system('cp ./scripts/config.json '+ config.get("scriptPath"))