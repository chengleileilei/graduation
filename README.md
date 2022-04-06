# graduation
毕业设计仓库

## 开发日志
### 已完成
1. 远程数据库增量拷贝到本地数据库（拷贝表结构+拷贝数据）
2. 通过company_patents 抽取inventor数据写入inventors表中（包括增加数据和增量更新数据）
### 待优化
1. 抽取inventor数据是只抽取了inventor name，外观设计类专利为designer name，需添加抽取designer代码
2. 统计collaborators时未将本人去除
3. 未使用消歧规则，当前默认规则为同名即同一inventor
### 计划
1. 爬取patent被引用数据添加到company_patents表中
2. 前端页面设计实现
   1. 动态路由
   2. 数据echarts可视化
3. 后端 flask
   1. flask 

