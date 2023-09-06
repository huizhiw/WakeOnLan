# Wake On Lan Via Docker

通过Docker来进行Wake On Lan，运行一次，唤醒Windows。
Implementation of Wake on Lan based on python. List 2 running methods, one is directly running through python enviroment, the other is running through docker

---

## 前提

- 主板支持WOL，打开 PCIE设备唤醒
- Windows 相关设置，包括远程唤醒 + 电源相关里 取消勾选 快速启动

具体查看一下其他教程，主要是以上两点

---

## 使用

### 1. Docker运行

#### 1.1 首先需要打包成镜像

在Dockerfile所在目录下运行

```shell
docker build -t <dwol>:<latest> .
```

#### 1.2 运行

然后运行下面这个

```shell
docker run --rm --net=host \
               -e mac='xx:xx:xx:xx:xx:xx' \   # 目标机MAC地址
               -e ip='192.168.1.123' \        # 目标机IP
               -e port=9 \
               --restart=no \
               --name="WakeOnLan" \
               dwol
```

每次运行这个容器会唤醒一次对应主机，然后销毁容器，相当于容器开关就是唤醒按钮~

### 2.直接python运行

可以直接下载/app/main.py，然后运行这个python即可，但注意要调整main里面的mac和ip到自己要唤醒的目标机的mac和ip

---
## 流程说明

1. 根据mac地址生成对应的 magic packet `'FF'*6 + str(mac)*16`，然后把这个转换到bytes类型的二进制，这个现在是十六进制的
2. 创建socket，发送到对应的机器即可，一般，默认的端口是9（或者7），IP是目标Windows的IP（顺带一提，这个IP最好在路由器的DHCP中绑定成固定IP，也就是IP-mac对应）

P.S. 在python里有个wakeonlan的包已经实现过了，先`pip install wakeonlan`，然后调用`wakeonlan.send_magic_packet(mac, ip, port)`即可
