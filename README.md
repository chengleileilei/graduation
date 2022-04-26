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


## 4月6日素问组会

### 主要算法
1. 消歧
   * 思路一：基于内容
   * 思路二：基于结构
2. 排序：根据专利人标签进行排序（依赖于技术标签提取）
3. 评分：依赖专利数量，topic排名等数据对人进行评分（是基于发明人的评分系统）
   * 专利质量评价（博文）：可参考专利质量进行发明人评价
   * 专利数量等
  
### 其他人工作
1. ipc分类号->技术标签（博文）
2. 专利数据->技术标签（张京）
3. 公司技术标签抽取（张京）

### 系统开发思路
1. 基本流程：消歧 -> 技术标签抽取（为评分和排名系统服务） -> 评分 -> baseline排名（实现搜索排序）
2. 高级搜索功能：
   1. 输入领域标签 -> 输出人才排序
   2. 可视化发明人图谱
  
### 平台对接
1. 输出数据->工程师进行系统开发




## 4月12日工作进展
### 数据
1. 测试10010条专利数据，其中8762条数据inventor和designer都为空，无法提取发明人
2. 10010条专利数据得到427个发明人数据


