
CUR_DIR=$(pwd)/excel
cd $1
npm install
node generateExcel.js
cp feLang.xlsx $CUR_DIR