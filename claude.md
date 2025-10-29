# HooRii Agent 角色生成系统

## 项目概述

本项目用于自动化生成 HooRii Agent 虚拟角色的图像和动画视频。系统通过 JSON 配置文件控制角色参数，调用 OpenAI 图像生成 API 创建角色图像，然后使用 WaveSpeed API 生成角色状态切换动画。

## 功能需求

### 1. 图像生成
- 使用 OpenAI Image Generation API (gpt-image-1) 生成高清人物半身正面图（无背景PNG）
- 使用正面图作为参考生成半身侧面图
- 图像要求：高清、无背景、PNG格式、9:16比例

### 2. 视频动画生成
参考 PDF 文档第 3.3 章节的要求，生成以下角色状态视频：

#### 核心状态视频
- **待机状态 [Default]**：角色不直视镜头，身体微侧，沉浸在自己的世界
- **聆听状态 [Listening]**：角色直视镜头，面对用户，情绪中性
- **说话状态 [Speaking]**：在聆听基础上增加口型开合动画

#### 状态切换视频
- **待机→聆听 [Default2Listening]**：从待机转向正面的过渡动画
- **聆听→待机 [Listening2Default]**：从正面转向侧面的过渡动画

#### 情绪状态视频（9种）
基于 Expression Sheet 设计，生成以下情绪状态：
1. 中性 [Neutral]：与聆听状态相同
2. 开心 [Happy]：开心地笑，脸红，歪头
3. 害羞 [Shy]：低头害羞，脸红
4. 惊讶 [Surprised]：表情惊讶，身体一震，后退
5. 自信 [Smug]：胸前抱手臂，得意自信
6. 生气 [Angry]：咬紧牙关，皱眉
7. 困惑 [Confused]：皱眉，手扶下巴思考
8. 悲伤 [Sad]：皱眉，深吸一口气，低头
9. 困倦 [Sleepy]：眼睛要闭起来，头向下耷拉

#### 多端切换视频
- **离开 [Leave]**：角色从画面中快速跑出
- **进入 [Enter]**：角色从画面边缘探头进入

### 3. 首尾帧控制
- 所有状态切换视频必须保证首尾帧一致，实现无缝衔接
- 聆听状态的首尾帧作为基准帧
- 所有情绪状态视频的首尾帧必须与聆听状态保持一致

## 技术栈

- **Python 3.8+**
- **OpenAI API**：图像生成
- **WaveSpeed API**：视频动画生成
- **python-dotenv**：环境变量管理
- **requests**：HTTP 请求

## 项目结构

```
GenAnim/
├── .env                      # 环境变量配置（不提交到git）
├── .gitignore               # Git忽略文件
├── requirements.txt         # Python依赖
├── config/
│   └── character_config.json # 角色配置文件
├── src/
│   ├── __init__.py
│   ├── image_generator.py   # OpenAI图像生成模块
│   ├── video_generator.py   # WaveSpeed视频生成模块
│   ├── config_loader.py     # 配置加载模块
│   └── utils.py             # 工具函数
├── outputs/
│   ├── images/              # 生成的图像
│   └── videos/              # 生成的视频
└── main.py                  # 主程序入口
```

## 环境配置

### .env 文件格式
```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# WaveSpeed API Key
WAVESPEED_API_KEY=your_wavespeed_api_key_here
```

### .gitignore 配置
确保添加以下内容：
```
.env
*.pyc
__pycache__/
outputs/
.DS_Store
```

## 角色配置文件格式 (character_config.json)

```json
{
  "character": {
    "name": "HooRii",
    "gender": "女",
    "age": 24,
    "personality": "傲娇、鬼马、可爱、机灵",
    "occupation": "爱打游戏的电竞少女",
    "background": "夜猫子，经常熬夜打游戏，喜欢与人连麦，但对待不熟的人话并不多，喜欢小动物，尤其喜欢猫",
    "special_features": "经常戴着一个黑色的猫耳电竞无线耳机，喜欢黑色简单的衣服和饰品"
  },
  "image_settings": {
    "style": "日系/90年代/二次元/半厚涂画风",
    "clothing": "黑色裙子，戴着黑色的choker，戴着黑色的无线猫耳耳机",
    "face": "眼睛狭长，眼神高冷带着一丝疏离迷离",
    "hairstyle": "黑色长发及腰，齐刘海",
    "pose": "半身正面站立姿势",
    "background": "纯白色背景",
    "image_settings": "9:16，画质高清，面部高清，细节刻画，无背景PNG"
  },
  "video_settings": {
    "duration": 5,
    "resolution": "1080p",
    "aspect_ratio": "9:16",
    "fps": 24,
    "format": "mp4"
  }
}
```

## 实现细节

### 1. 图像生成模块 (image_generator.py)

**功能**：
- 读取角色配置
- 构建 OpenAI 图像生成提示词
- 生成正面半身图（无背景PNG）
- 基于正面图生成侧面图
- 保存图像到 outputs/images/

**关键提示词构建**：
```
基础角色描述 + 外观特征 + 姿势视角 + 图像设置

示例：
"A 24-year-old anime girl gamer, Japanese 90s semi-thick paint art style,
black long hair with bangs, narrow eyes with cold gaze, wearing black dress,
black choker, black cat-ear wireless gaming headset, half-body front view,
standing pose, white background, high quality, detailed face, 9:16 ratio, PNG format"
```

**API 调用示例**：
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.images.generate(
    model="dall-e-3",  # 或 gpt-image-1 如果可用
    prompt=prompt,
    size="1024x1792",  # 9:16 ratio
    quality="hd",
    n=1,
    response_format="url"
)
```

### 2. 视频生成模块 (video_generator.py)

**功能**：
- 使用生成的角色图像作为参考
- 根据状态类型生成不同的视频动画
- 确保首尾帧一致性
- 轮询检查生成状态
- 下载并保存视频

**WaveSpeed API 集成参考**：

```python
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

class VideoGenerator:
    def __init__(self):
        self.api_key = os.getenv("WAVESPEED_API_KEY")
        self.base_url = "https://api.wavespeed.ai/api/v3"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate_video(self, image_url, prompt, duration=5, camera_fixed=False):
        """
        生成视频动画

        Args:
            image_url: 参考图像URL（需要是公开可访问的URL）
            prompt: 动画描述提示词
            duration: 视频时长（秒）
            camera_fixed: 是否固定镜头

        Returns:
            视频URL
        """
        url = f"{self.base_url}/bytedance/seedance-v1-pro-i2v-720p"

        payload = {
            "camera_fixed": camera_fixed,
            "duration": duration,
            "image": image_url,
            "prompt": prompt,
            "seed": -1  # -1 表示随机种子
        }

        # 提交生成任务
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f"Failed to submit task: {response.status_code}, {response.text}")

        result = response.json()["data"]
        request_id = result["id"]
        print(f"Task submitted. Request ID: {request_id}")

        # 轮询检查生成状态
        return self._poll_result(request_id)

    def _poll_result(self, request_id, poll_interval=2, max_wait_time=300):
        """
        轮询检查视频生成结果

        Args:
            request_id: 任务ID
            poll_interval: 轮询间隔（秒）
            max_wait_time: 最大等待时间（秒）

        Returns:
            视频URL
        """
        url = f"{self.base_url}/predictions/{request_id}/result"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Failed to check status: {response.status_code}, {response.text}")

            result = response.json()["data"]
            status = result["status"]

            if status == "completed":
                video_url = result["outputs"][0]
                print(f"Video generated successfully: {video_url}")
                return video_url
            elif status == "failed":
                raise Exception(f"Video generation failed: {result.get('error')}")
            else:
                print(f"Status: {status}, waiting...")
                time.sleep(poll_interval)

        raise TimeoutError("Video generation timed out")
```

### 3. 状态视频生成提示词

根据 PDF 3.3 章节要求，各状态的提示词：

#### 待机状态 [Default]
```
"女孩看向一侧，偶尔眨眼，头发被风微微吹起，身体不动，镜头保持固定不动，光线环境均不变"
时长：5秒
camera_fixed: True
```

#### 待机→聆听 [Default2Listening]
```
"女孩从左侧转向正面，看着镜头，手放在身体两侧，动作过程流畅自然，无变形无卡顿"
时长：5秒
首帧：待机尾帧
尾帧：聆听首帧
```

#### 聆听状态 [Listening]
```
"创建一段5s的视频，女孩头发自然的被风微微吹动，眨眨眼"
时长：5秒
camera_fixed: True
```

#### 聆听→待机 [Listening2Default]
```
"女孩从正面转向左侧，手背在后面，动作过程流畅自然，无变形无卡顿"
时长：5秒
```

#### 说话状态 [Speaking]
```
"女孩在说话，头发被风自然的微微吹动，偶尔眨眼，头部可以自然的偶尔歪一下头，动作幅度很小"
时长：4秒
camera_fixed: True
```

#### 开心 [Happy]
```
"创建一段5s的视频，女孩开心地笑，脸红，歪头，镜头固定"
时长：5秒
首尾帧：与聆听状态一致
```

#### 害羞 [Shy]
```
"女孩听到某句话低头害羞，脸红"
时长：5秒（可分两段生成后拼接）
首尾帧：与聆听状态一致
```

#### 惊讶 [Surprised]
```
"女孩像被什么吓到了，表情惊讶，身体一震，后退两步，肩耸起来，慌张的左右看"
时长：5秒
首尾帧：与聆听状态一致
```

#### 自信 [Smug]
```
"女孩在胸前抱起手臂，得意自信的样子，又放下"
时长：5秒
首尾帧：与聆听状态一致
```

#### 生气 [Angry]
```
"女孩生气，咬紧牙关，皱眉，再回归平静"
时长：5秒
首尾帧：与聆听状态一致
```

#### 困惑 [Confused]
```
"女孩皱着眉，表情严肃，很困惑的样子，一只手扶着下巴，好像在思考什么，镜头固定不动"
时长：5秒
首尾帧：与聆听状态一致
```

#### 悲伤 [Sad]
```
"女孩皱着眉，深吸一口气，微微低头，眼睛向下看"
时长：5秒
首尾帧：与聆听状态一致
```

#### 困倦 [Sleepy]
```
"女孩看起来很困的样子，眼睛要闭起来了，头向下耷拉，身体微微晃动"
时长：5秒
首尾帧：与聆听状态一致
```

#### 离开 [Leave]
```
"女孩从画面中快速离开，从右侧跑出画面，只留下纯白的背景，动作自然流畅无变形，跑步姿势流畅"
时长：5秒
首帧：聆听首帧
尾帧：纯白背景
```

#### 进入 [Enter]
```
"创建一段5s的视频，首帧时人物不在画面中，画面只有纯白色背景，然后人物从画面左侧边缘探头进画面，然后走进画面，正对镜头，整个过程中人物占画面画幅比例不变，人物细节保持一致"
时长：5秒
首帧：纯白背景
尾帧：聆听尾帧
```

### 4. 首尾帧控制策略

为确保视频切换的流畅性，需要：

1. **保存关键帧**：
   - 从聆听状态视频提取首帧和尾帧作为基准
   - 所有情绪状态视频的首尾帧必须与此一致

2. **视频生成顺序**：
   - 先生成聆听状态视频（基准）
   - 生成待机状态视频
   - 生成过渡视频（使用对应的首尾帧）
   - 生成情绪状态视频（使用聆听的首尾帧）
   - 生成多端切换视频

3. **验证流程**：
   - 生成后使用视频编辑工具拼接检查
   - 确保无跳帧、无卡顿
   - 统一分辨率、帧率、码率

### 5. 视频输出规格

根据 PDF 第五章要求：

- **比例**：9:16
- **分辨率**：1080p (1088x1920)
- **帧率**：24fps
- **视频编码**：H.264
- **格式**：MP4
- **色彩空间**：Rec.709 SDR

## 实现步骤

### 第一步：环境准备
1. 创建虚拟环境
2. 安装依赖包
3. 配置 .env 文件
4. 创建项目目录结构

### 第二步：配置管理
1. 实现 config_loader.py
2. 支持从 JSON 读取角色配置
3. 验证配置完整性

### 第三步：图像生成
1. 实现 image_generator.py
2. 调用 OpenAI API 生成正面图
3. 生成侧面图（可使用图生图）
4. 保存图像并返回路径

### 第四步：视频生成
1. 实现 video_generator.py
2. 上传图像到公开可访问的位置（或使用URL）
3. 按照生成顺序依次生成所有状态视频
4. 实现轮询和下载机制
5. 保存视频到本地

### 第五步：主流程整合
1. 实现 main.py 主入口
2. 整合图像生成和视频生成流程
3. 添加进度显示和错误处理
4. 生成视频清单和统计

### 第六步：后期处理
1. 使用 FFmpeg 或 MoviePy 进行视频后处理
2. 统一视频参数
3. 拼接检查
4. 生成最终交付清单

## 交付清单

生成完成后应包含以下文件：

### 图像文件（2个）
- `front_view.png` - 正面半身图
- `side_view.png` - 侧面半身图

### 视频文件（17个）

**待机+聆听（4个）**：
- `default.mp4` - 待机状态
- `default2listening.mp4` - 待机→聆听
- `listening.mp4` - 聆听状态（2个版本）
- `speaking.mp4` - 说话状态
- `listening2default.mp4` - 聆听→待机

**情绪状态（9个）**：
- `neutral.mp4` - 中性
- `happy.mp4` - 开心
- `shy.mp4` - 害羞
- `surprised.mp4` - 惊讶
- `smug.mp4` - 自信
- `angry.mp4` - 生气
- `confused.mp4` - 困惑
- `sad.mp4` - 悲伤
- `sleepy.mp4` - 困倦

**多端切换（3个）**：
- `listening2leave.mp4` - 聆听→离开
- `default2leave.mp4` - 待机→离开
- `enter.mp4` - 进入

## 使用说明

### 运行程序
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python main.py --config config/character_config.json

# 仅生成图像
python main.py --config config/character_config.json --images-only

# 仅生成视频（需要已有图像）
python main.py --config config/character_config.json --videos-only
```

### 命令行参数
- `--config`: 角色配置文件路径
- `--images-only`: 仅生成图像
- `--videos-only`: 仅生成视频
- `--output-dir`: 输出目录
- `--skip-existing`: 跳过已存在的文件

## 注意事项

1. **API 限制**：
   - OpenAI 和 WaveSpeed API 都有调用频率限制
   - 建议添加重试机制和速率限制

2. **成本控制**：
   - 图像生成和视频生成都会产生费用
   - 建议先小规模测试

3. **图像托管**：
   - WaveSpeed API 需要公开可访问的图像URL
   - 可使用临时图床或对象存储服务

4. **视频质量**：
   - AI 生成的视频质量可能需要多次尝试
   - 建议保存中间结果便于调试

5. **首尾帧一致性**：
   - 这是最关键的技术点
   - 可能需要手动调整或使用图像编辑工具

6. **批量生成**：
   - 17个视频生成时间较长
   - 建议实现异步并发和进度保存

## 扩展功能（可选）

1. **多角色支持**：支持批量生成多个角色
2. **Web UI**：提供可视化配置界面
3. **预览功能**：生成前预览提示词效果
4. **版本管理**：保存多个版本便于对比
5. **自动上传**：集成云存储自动上传
6. **质量评估**：自动评估生成质量

## 参考文档

- OpenAI Image Generation API: https://platform.openai.com/docs/guides/images
- WaveSpeed API 文档: 参考提供的示例代码
- PDF 文档: HooRii Agent 角色创建流程.pdf（第3.3章节开始）

## 问题排查

### 常见问题

1. **API Key 无效**
   - 检查 .env 文件配置
   - 确认 API Key 有效且有足够余额

2. **图像生成失败**
   - 检查提示词是否合规
   - 尝试简化提示词
   - 检查网络连接

3. **视频生成超时**
   - 增加 max_wait_time 参数
   - 检查图像URL是否可访问
   - 简化动画提示词

4. **首尾帧不一致**
   - 使用视频编辑工具手动提取和设置关键帧
   - 考虑使用更精确的帧控制参数

## 版本记录

- v1.0.0: 初始版本，支持基础图像和视频生成
