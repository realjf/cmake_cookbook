## 检测python库

可以使用Python工具来分析和操作程序的输出。 然而， 还有更强大的方法可以将解释语言(如Python)
与编译语言(如C或C++)组合在一起使用。 一种是扩展Python， 通过编译成共享库的C或C++模块在这
些类型上提供新类型和新功能， 这是第9章的主题。 另一种是将Python解释器嵌入到C或C++程序中。
两种方法都需要下列条件:

- Python解释器的工作版本
- Python头文件Python.h的可用性
- Python运行时库libpython

三个组件所使用的Python版本必须相同。 

### 准备


