# Backend - Smart Plug API

本后端用于封装 Tuya 智能插座控制接口，前端不要直接调用 Tuya API。

## 配置

不要把 Access Secret 写进代码。运行前在 IntelliJ IDEA 的 Run Configuration 里添加环境变量：

```text
TUYA_ACCESS_ID=你的 Access ID
TUYA_ACCESS_SECRET=你的 Access Secret
```

配置文件：

```text
src/main/resources/application.properties
```

当前设备：

```text
tuya.device-id=a31eb1ded013b84ec7d1op
tuya.base-url=https://openapi-sg.iotbing.com
```

## 接口

```text
GET  http://localhost:8080/api/plug/status
POST http://localhost:8080/api/plug/on
POST http://localhost:8080/api/plug/off
```

## curl 测试

```bash
curl http://localhost:8080/api/plug/status
curl -X POST http://localhost:8080/api/plug/on
curl -X POST http://localhost:8080/api/plug/off
```
