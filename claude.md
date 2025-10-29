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
- **抽象基类（ABC）**：定义图像和视频生成的标准接口
- **OpenAI API**：默认图像生成提供商
- **WaveSpeed API**：默认视频动画生成提供商
- **python-dotenv**：环境变量管理
- **requests**：HTTP 请求

## 架构设计原则

为了支持多种 API 提供商，系统采用**接口抽象**设计：

- **可扩展性**：通过抽象基类定义标准接口，轻松切换或添加新的 API 提供商
- **解耦合**：业务逻辑与具体 API 实现分离
- **配置化**：通过配置文件选择使用的提供商，无需修改代码

## 项目结构

```
GenAnim/
├── .env                           # 环境变量配置（不提交到git）
├── .gitignore                     # Git忽略文件
├── requirements.txt               # Python依赖
├── config/
│   └── character_config.json      # 角色配置文件
├── src/
│   ├── __init__.py
│   ├── interfaces/                # 接口定义
│   │   ├── __init__.py
│   │   ├── image_provider.py      # 图像生成接口（抽象基类）
│   │   └── video_provider.py      # 视频生成接口（抽象基类）
│   ├── providers/                 # API 提供商实现
│   │   ├── __init__.py
│   │   ├── image/                 # 图像生成提供商
│   │   │   ├── __init__.py
│   │   │   ├── openai_provider.py      # OpenAI 实现
│   │   │   ├── midjourney_provider.py  # Midjourney 实现（示例）
│   │   │   └── stable_diffusion_provider.py  # Stable Diffusion 实现（示例）
│   │   └── video/                 # 视频生成提供商
│   │       ├── __init__.py
│   │       ├── wavespeed_provider.py    # WaveSpeed 实现
│   │       ├── runway_provider.py       # Runway 实现（示例）
│   │       └── pika_provider.py         # Pika 实现（示例）
│   ├── factory.py                 # 工厂类，根据配置创建提供商实例
│   ├── config_loader.py           # 配置加载模块
│   └── utils.py                   # 工具函数
├── outputs/
│   ├── images/                    # 生成的图像
│   └── videos/                    # 生成的视频
└── main.py                        # 主程序入口
```

## 环境配置

### .env 文件格式
```bash
# 图像生成 API Keys
OPENAI_API_KEY=your_openai_api_key_here
MIDJOURNEY_API_KEY=your_midjourney_api_key_here
STABILITY_API_KEY=your_stability_api_key_here

# 视频生成 API Keys
WAVESPEED_API_KEY=your_wavespeed_api_key_here
RUNWAY_API_KEY=your_runway_api_key_here
PIKA_API_KEY=your_pika_api_key_here

# 根据配置文件中选择的提供商，只需配置对应的 API Key
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
  "providers": {
    "image": "openai",
    "video": "wavespeed"
  },
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

**providers 字段说明**：
- `image`: 图像生成提供商，可选值：`openai`, `midjourney`, `stable_diffusion` 等
- `video`: 视频生成提供商，可选值：`wavespeed`, `runway`, `pika` 等

## 接口设计

为了支持多种 API 提供商，系统使用抽象基类（ABC）定义统一接口。

### 1. 图像生成接口 (interfaces/image_provider.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class ImageGenerationResult:
    """图像生成结果"""
    image_url: str          # 图像URL
    local_path: Optional[str] = None  # 本地保存路径
    metadata: Optional[Dict] = None   # 元数据（如模型、参数等）

class ImageProvider(ABC):
    """图像生成提供商抽象基类"""

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1792,
        quality: str = "high",
        **kwargs
    ) -> ImageGenerationResult:
        """
        生成图像

        Args:
            prompt: 图像生成提示词
            width: 图像宽度
            height: 图像高度
            quality: 图像质量
            **kwargs: 其他提供商特定参数

        Returns:
            ImageGenerationResult: 生成结果
        """
        pass

    @abstractmethod
    def generate_image_from_image(
        self,
        prompt: str,
        reference_image_url: str,
        width: int = 1024,
        height: int = 1792,
        **kwargs
    ) -> ImageGenerationResult:
        """
        基于参考图像生成新图像（图生图）

        Args:
            prompt: 图像生成提示词
            reference_image_url: 参考图像URL
            width: 图像宽度
            height: 图像高度
            **kwargs: 其他提供商特定参数

        Returns:
            ImageGenerationResult: 生成结果
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        pass
```

### 2. 视频生成接口 (interfaces/video_provider.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class VideoGenerationResult:
    """视频生成结果"""
    video_url: str          # 视频URL
    local_path: Optional[str] = None  # 本地保存路径
    duration: Optional[float] = None  # 视频时长（秒）
    metadata: Optional[Dict] = None   # 元数据

class VideoProvider(ABC):
    """视频生成提供商抽象基类"""

    @abstractmethod
    def generate_video(
        self,
        image_url: str,
        prompt: str,
        duration: int = 5,
        camera_fixed: bool = False,
        first_frame_url: Optional[str] = None,
        last_frame_url: Optional[str] = None,
        **kwargs
    ) -> VideoGenerationResult:
        """
        基于图像生成视频动画

        Args:
            image_url: 参考图像URL
            prompt: 动画描述提示词
            duration: 视频时长（秒）
            camera_fixed: 是否固定镜头
            first_frame_url: 首帧图像URL（用于首尾帧控制）
            last_frame_url: 尾帧图像URL（用于首尾帧控制）
            **kwargs: 其他提供商特定参数

        Returns:
            VideoGenerationResult: 生成结果
        """
        pass

    @abstractmethod
    def check_status(self, task_id: str) -> Dict:
        """
        检查视频生成任务状态

        Args:
            task_id: 任务ID

        Returns:
            Dict: 包含状态信息的字典
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """获取提供商名称"""
        pass
```

### 3. 工厂类 (factory.py)

```python
from typing import Dict
from src.interfaces.image_provider import ImageProvider
from src.interfaces.video_provider import VideoProvider

class ProviderFactory:
    """提供商工厂类"""

    # 注册的图像提供商
    _image_providers: Dict[str, type] = {}

    # 注册的视频提供商
    _video_providers: Dict[str, type] = {}

    @classmethod
    def register_image_provider(cls, name: str, provider_class: type):
        """注册图像提供商"""
        cls._image_providers[name] = provider_class

    @classmethod
    def register_video_provider(cls, name: str, provider_class: type):
        """注册视频提供商"""
        cls._video_providers[name] = provider_class

    @classmethod
    def create_image_provider(cls, name: str, **kwargs) -> ImageProvider:
        """
        创建图像提供商实例

        Args:
            name: 提供商名称
            **kwargs: 初始化参数

        Returns:
            ImageProvider: 提供商实例
        """
        if name not in cls._image_providers:
            raise ValueError(f"Unknown image provider: {name}")

        return cls._image_providers[name](**kwargs)

    @classmethod
    def create_video_provider(cls, name: str, **kwargs) -> VideoProvider:
        """
        创建视频提供商实例

        Args:
            name: 提供商名称
            **kwargs: 初始化参数

        Returns:
            VideoProvider: 提供商实例
        """
        if name not in cls._video_providers:
            raise ValueError(f"Unknown video provider: {name}")

        return cls._video_providers[name](**kwargs)

# 注册内置提供商
from src.providers.image.openai_provider import OpenAIImageProvider
from src.providers.video.wavespeed_provider import WaveSpeedVideoProvider

ProviderFactory.register_image_provider("openai", OpenAIImageProvider)
ProviderFactory.register_video_provider("wavespeed", WaveSpeedVideoProvider)

# 添加其他提供商时，在这里注册
# ProviderFactory.register_image_provider("midjourney", MidjourneyImageProvider)
# ProviderFactory.register_video_provider("runway", RunwayVideoProvider)
```

### 4. 使用示例

```python
from src.factory import ProviderFactory
from src.config_loader import load_config

# 加载配置
config = load_config("config/character_config.json")

# 根据配置创建提供商
image_provider = ProviderFactory.create_image_provider(
    config["providers"]["image"]
)

video_provider = ProviderFactory.create_video_provider(
    config["providers"]["video"]
)

# 使用提供商生成图像
result = image_provider.generate_image(
    prompt="A beautiful anime girl...",
    width=1024,
    height=1792
)

# 使用提供商生成视频
video_result = video_provider.generate_video(
    image_url=result.image_url,
    prompt="Girl gently blinking...",
    duration=5,
    camera_fixed=True
)
```

## 实现细节

### 1. OpenAI 图像提供商实现 (providers/image/openai_provider.py)

```python
import os
import requests
from typing import Optional
from openai import OpenAI
from src.interfaces.image_provider import ImageProvider, ImageGenerationResult

class OpenAIImageProvider(ImageProvider):
    """OpenAI 图像生成提供商"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1792,
        quality: str = "hd",
        **kwargs
    ) -> ImageGenerationResult:
        """生成图像"""
        # OpenAI DALL-E 3 的尺寸选项有限
        size = f"{width}x{height}"
        if size not in ["1024x1024", "1024x1792", "1792x1024"]:
            size = "1024x1792"  # 默认 9:16

        response = self.client.images.generate(
            model=kwargs.get("model", "dall-e-3"),
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
            response_format="url"
        )

        image_url = response.data[0].url

        return ImageGenerationResult(
            image_url=image_url,
            metadata={
                "model": kwargs.get("model", "dall-e-3"),
                "size": size,
                "quality": quality
            }
        )

    def generate_image_from_image(
        self,
        prompt: str,
        reference_image_url: str,
        width: int = 1024,
        height: int = 1792,
        **kwargs
    ) -> ImageGenerationResult:
        """
        基于参考图像生成新图像
        注意：OpenAI 的 DALL-E 3 不直接支持图生图
        这里可以使用 GPT-4 Vision 分析参考图，然后用新提示词生成
        或者集成其他支持图生图的模型
        """
        # 简化实现：将参考图的特征加入提示词
        enhanced_prompt = f"{prompt}, maintain the style and character from reference"

        return self.generate_image(
            prompt=enhanced_prompt,
            width=width,
            height=height,
            **kwargs
        )

    def get_provider_name(self) -> str:
        return "openai"
```

**关键提示词构建**：
```python
def build_image_prompt(character_config: dict) -> str:
    """根据角色配置构建图像生成提示词"""
    char = character_config["character"]
    img_settings = character_config["image_settings"]

    prompt = f"""
A {char['age']}-year-old anime {char['gender']} character,
{char['occupation']}, {char['personality']} personality,
{img_settings['style']},
{img_settings['face']},
{img_settings['hairstyle']},
wearing {img_settings['clothing']},
{img_settings['pose']},
{img_settings['background']},
{img_settings['image_settings']}
    """.strip()

    return prompt
```

### 2. WaveSpeed 视频提供商实现 (providers/video/wavespeed_provider.py)

```python
import os
import requests
import json
import time
from typing import Optional, Dict
from src.interfaces.video_provider import VideoProvider, VideoGenerationResult

class WaveSpeedVideoProvider(VideoProvider):
    """WaveSpeed 视频生成提供商"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("WAVESPEED_API_KEY")
        self.base_url = "https://api.wavespeed.ai/api/v3"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def generate_video(
        self,
        image_url: str,
        prompt: str,
        duration: int = 5,
        camera_fixed: bool = False,
        first_frame_url: Optional[str] = None,
        last_frame_url: Optional[str] = None,
        **kwargs
    ) -> VideoGenerationResult:
        """生成视频动画"""
        url = f"{self.base_url}/bytedance/seedance-v1-pro-i2v-720p"

        payload = {
            "camera_fixed": camera_fixed,
            "duration": duration,
            "image": image_url,
            "prompt": prompt,
            "seed": kwargs.get("seed", -1)
        }

        # 如果支持首尾帧控制，添加到 payload
        if first_frame_url:
            payload["first_frame"] = first_frame_url
        if last_frame_url:
            payload["last_frame"] = last_frame_url

        # 提交生成任务
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f"Failed to submit task: {response.status_code}, {response.text}")

        result = response.json()["data"]
        task_id = result["id"]
        print(f"Task submitted. Request ID: {task_id}")

        # 轮询检查生成状态
        video_url = self._poll_result(task_id)

        return VideoGenerationResult(
            video_url=video_url,
            duration=duration,
            metadata={
                "task_id": task_id,
                "camera_fixed": camera_fixed,
                "prompt": prompt
            }
        )

    def check_status(self, task_id: str) -> Dict:
        """检查任务状态"""
        url = f"{self.base_url}/predictions/{task_id}/result"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to check status: {response.status_code}, {response.text}")

        return response.json()["data"]

    def _poll_result(self, task_id: str, poll_interval: int = 2, max_wait_time: int = 300) -> str:
        """轮询检查视频生成结果"""
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            result = self.check_status(task_id)
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

    def get_provider_name(self) -> str:
        return "wavespeed"
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

## 如何添加新的 API 提供商

### 添加图像生成提供商

1. **创建提供商类**：在 `src/providers/image/` 目录下创建新文件，例如 `midjourney_provider.py`

```python
from typing import Optional
from src.interfaces.image_provider import ImageProvider, ImageGenerationResult

class MidjourneyImageProvider(ImageProvider):
    """Midjourney 图像生成提供商"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("MIDJOURNEY_API_KEY")
        # 初始化 Midjourney API 客户端

    def generate_image(self, prompt: str, width: int = 1024, height: int = 1792, quality: str = "high", **kwargs) -> ImageGenerationResult:
        # 实现 Midjourney 的图像生成逻辑
        pass

    def generate_image_from_image(self, prompt: str, reference_image_url: str, width: int = 1024, height: int = 1792, **kwargs) -> ImageGenerationResult:
        # 实现 Midjourney 的图生图逻辑
        pass

    def get_provider_name(self) -> str:
        return "midjourney"
```

2. **注册提供商**：在 `src/factory.py` 中注册新提供商

```python
from src.providers.image.midjourney_provider import MidjourneyImageProvider

ProviderFactory.register_image_provider("midjourney", MidjourneyImageProvider)
```

3. **更新配置**：在配置文件中使用新提供商

```json
{
  "providers": {
    "image": "midjourney",
    "video": "wavespeed"
  }
}
```

### 添加视频生成提供商

1. **创建提供商类**：在 `src/providers/video/` 目录下创建新文件，例如 `runway_provider.py`

```python
from typing import Optional, Dict
from src.interfaces.video_provider import VideoProvider, VideoGenerationResult

class RunwayVideoProvider(VideoProvider):
    """Runway 视频生成提供商"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY")
        # 初始化 Runway API 客户端

    def generate_video(self, image_url: str, prompt: str, duration: int = 5, camera_fixed: bool = False, first_frame_url: Optional[str] = None, last_frame_url: Optional[str] = None, **kwargs) -> VideoGenerationResult:
        # 实现 Runway 的视频生成逻辑
        pass

    def check_status(self, task_id: str) -> Dict:
        # 实现任务状态检查
        pass

    def get_provider_name(self) -> str:
        return "runway"
```

2. **注册提供商**：在 `src/factory.py` 中注册

```python
from src.providers.video.runway_provider import RunwayVideoProvider

ProviderFactory.register_video_provider("runway", RunwayVideoProvider)
```

3. **添加 API Key**：在 `.env` 文件中添加

```bash
RUNWAY_API_KEY=your_runway_api_key_here
```

## 扩展功能（可选）

1. **多角色支持**：支持批量生成多个角色
2. **Web UI**：提供可视化配置界面
3. **预览功能**：生成前预览提示词效果
4. **版本管理**：保存多个版本便于对比
5. **自动上传**：集成云存储自动上传
6. **质量评估**：自动评估生成质量
7. **提供商对比**：同时使用多个提供商生成，对比选择最佳结果

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
- v1.1.0: 添加接口抽象层设计，支持多 API 提供商切换
  - 定义了 ImageProvider 和 VideoProvider 抽象基类
  - 实现了 OpenAI 和 WaveSpeed 提供商
  - 添加工厂模式支持动态创建提供商
  - 配置文件支持提供商选择
