# 使用 Web+ 部署 Python 应用

感谢您使用 Web 应用托管服务（Web+），此教程将向您展示如何使用 Web+ 部署 Python 应用程序。

本教程包含以下内容：

* 安装命令行工具
* 下载并打包样例工程
* 创建应用及部署环境
* 释放环境并删除应用

请单击右下角的“下一步”按钮开始。

## 安装命令行工具

**说明**：Cloud Shell 已经预装 Web+ 的命令行工具（wpctl）。如果您是在 Cloud Shell 中使用本教程，可以跳过此步骤或使用 `wpctl upgrade` 命令将 Web+ 的命令行工具升级到最新版本。

Web+ 命令行工具提供了与控制台相同的功能，当前版本支持 Linux 与 macOS 两种操作系统，请执行以下命令下载并安装：

```bash
eval "$(curl -s -L https://webplus-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/cli/install.sh)"
```

命令行工具成功安装之后，需要执行 `wpctl configure` 命令对其进行配置，该命令的具体参数请参见[文档](https://help.aliyun.com/document_detail/116129.html)。

```bash
wpctl configure --access-key-id <YOUR_ACCESS_KEY_ID> --access-key-secret <YOUR_ACCESS_KEY_SECRET> --region <YOUR_REGION> --profile webplus
```

> `--access-key-id` 和 `--access-key-secret` 访问阿里云服务的授权凭证。关于如何获取 AccessKeyId 和 AccessKeySecret 请参见[文档](https://help.aliyun.com/document_detail/53045.html?parentId=35469)。
>
> `--region` Web+ 创建资源时所使用的默认区域。有关 Web+ 支持的区域列表，请参见[文档](https://help.aliyun.com/document_detail/121097.html)。
>
> `--profile` 配置名称。

## 下载并打包样例工程

本教程将使用 Web+ 提供的[样例工程](https://github.com/aliyun/alibabacloud-webplus-python-demo)，需要将该工程克隆到本地，并进入工程根目录：

```bash
git clone https://github.com/aliyun/alibabacloud-webplus-python-demo.git webplus-python-demo && cd webplus-python-demo
```

**注意**：如果该目录已经存在，请克隆之前先将其删除。

直接打包：

```bash
zip -r dist/webplus-python-demo.zip .
```

## 创建应用及部署环境

接下来需要创建应用及部署环境，然后将打包好的应用程序上传到该部署环境：

```bash
wpctl env:apply --package dist/webplus-python-demo.zip  --category Python --app webplus-python-demo --env test-env --create-on-absent
```

> `--package` 要上传的部署包路径。
>
> `--category` 该应用的技术栈类型。
>
> `--app` 应用名称。
>
> `--env` 部署环境名称。
>
> `--create-on-absent` 如果指定的应用及部署环境不存在将进行创建。

执行该命令时，Web+ 将为您代购所需的资源（默认情况下将以按量付费的方式在当前可用区中购买一台介于 1 核 1G 和 4 核 8G 之间的最小规格的 ECS 实例）。整个过程可能会持续几分钟，在此期间命令行窗口将会滚动显示当前正在进行的操作，部署完成后会输出该部署环境的链接地址。

如果您不小心忽略了该信息，还可以通过以下方式查看事件并获取环境的访问链接：

1. 将当前工作目录与 Web+ 的部署环境进行绑定：

   ```bash
   wpctl env:use test-env --app webplus-python-demo
   ```

   > `--app` 应用名称。

2. 执行事件查看命令，确认变更操作成功完成：

   ```bash
   wpctl env:events
   ```

   **说明**：使用 `q` 命令退出事件查看界面。

3. 获取应用的访问链接：

   ```bash
   wpctl env:info
   ```

## 释放环境并删除应用

当部署环境释放以后，所有代购的 ECS 实例也将被释放，此后将不再收取相关费用。因此当您不再需要该部署环境时请及时释放以免继续产生费用。

释放部署环境：

```bash
wpctl env:terminate --app webplus-python-demo --env test-env
```

> `--app` 应用名称。
>
> `--env` 部署环境名称。

删除应用：

```bash
wpctl app:delete webplus-python-demo
```

## 结束语

恭喜您成功使用 Web+ 部署了一个 Python 应用！接下来您可以继续阅读[文档](https://help.aliyun.com/product/113017.html)来了解 Web+ 的更多功能。

Web+ ——阿里云上应用托管的一站式便捷体验。

您可以使用钉钉扫描以下二维码，加入 Web+ 用户交流群。

![Web+ 用户交流群](https://webplus-common.oss-cn-shenzhen.aliyuncs.com/dingtalk/dingtalk-qrcode.png)
