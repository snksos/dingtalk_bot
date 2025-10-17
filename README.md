# HACS 集成组件

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

## 简介

这是一个用于 Home Assistant 的自定义集成组件。通过 HACS（Home Assistant Community Store）进行安装。

## 安装方法

1. 确保你已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中搜索此集成，如果搜索不到，请在 HACS 中添加此仓库
3. 点击下载按钮进行安装
4. 重启 Home Assistant

## 配置说明

在 Home Assistant 的配置文件 `configuration.yaml` 中添加以下配置：

```yaml
notify:
  - platform: dingtalk_bot
    name: dingtalk_notify
    access_token: "你的access_token" # 必填
    secret: "你的secret" # 可选，仅在机器人开启"加签"安全设置时需要
```

## 注意事项

1. 请确保你的钉钉机器人已经配置好，并且能够正常发送消息
2. 请确保你的 Home Assistant 能够正常访问互联网
3. 请确保你的 Home Assistant 能够正常访问钉钉服务器

