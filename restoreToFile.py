import os
import json
import pandas as pd
import glob
import utils

def getFilePath(path, lang):
    fileList = glob.glob(path)
    for p in fileList:
      if os.path.basename(p).startswith(lang):
        return p

def getJsonData(path):
    fileList = glob.glob(path)
    langData = {}

    for file_path in fileList: 
      lang = utils.getLang(file_path)
      fileContent = utils.getJsonFileContent(file_path)
      langData[lang] = fileContent

    return langData



def restore(file, sheetName, path):
  data = pd.read_excel(file, sheet_name=sheetName)
  # 原始数据
  sourceAllLangData = getJsonData(path) 

  langList = data.columns.tolist()
  langList.remove('key')

  for lang in langList:
    langData = data.get(['key', lang]).to_json(orient="values")
    # excel 转换后的json数据
    targetData = dict(json.loads(langData))
    sourceData = sourceAllLangData[lang]

    # 更新及添加词条，有则更新，无则添加
    for key, value in targetData.items():
      sourceData[key] = value
      
    # 找到文件，写入
    filePath = getFilePath(path, lang)
    file = open(filePath, 'w')
    file.write(json.dumps(sourceData, indent=2))
    file.close()

configList = open('./config.json')
for config in json.load(configList):
  if config.get('fileType') == 'json':
    restore('./excel/rdLang.xlsx', config.get('sheetName'), config.get('path'))
  elif config.get('fileType') == 'js':
    configIsExist = os.path.exists(config.get("scriptPath") + '/config.json')
    print(configIsExist)
    if configIsExist == False:
      utils.generateConfig(config)
    os.system('./scripts/js_restoreToFile.sh' + ' ' + config.get("scriptPath") )



