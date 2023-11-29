# Protocol 协议

* 生成代码使用的是 [flatbuffers](https://google.github.io/flatbuffers/)
* 脚本使用 TypeScript 编写, ts-node 运行
* 包括配置表 csv 和 网络通信协议 fbs
* fbs 可以引用 csv 生成的结构
* csv 包括三种
  * 枚举表 {Enum Name}Enum.csv
  * 结构表 {Struct Name}Struct.csv
  * 数据表 {Data Name}Table.csv
* 枚举表和结构表只生成代码，数据表作为静态配置，生成代码和数据 bytes
* 导出代码时处理了一些代码使其使用起来更简单一点（其实是懒得写那么长
