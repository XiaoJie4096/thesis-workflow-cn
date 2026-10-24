# 论文常用图的 Mermaid 模板

文件放在 `figures/src/<文件名>.mmd`，渲染后得到 `figures/<文件名>.png`。文件名用英文或拼音，图题写在正文的图片标记里。下面示例以农场游戏为例，替换成项目里真实存在的模块。

## 1. 系统总体架构图（分层）

```mermaid
flowchart TB
  subgraph UI[表现层]
    direction LR
    A1[主菜单界面] --- A2[游戏主界面] --- A3[背包与商店界面]
  end
  subgraph Logic[逻辑层]
    direction LR
    B1[种植系统] --- B2[时间系统] --- B3[经济系统] --- B4[背包系统]
  end
  subgraph Data[数据层]
    direction LR
    C1[(作物配置 ScriptableObject)] --- C2[(存档 JSON 文件)]
  end
  UI --> Logic --> Data
```

## 2. 功能模块图（树状）

```mermaid
flowchart TB
  root[农场游戏系统]
  root --> m1[种植模块] & m2[经济模块] & m3[时间模块] & m4[存档模块]
  m1 --> m11[翻地] & m12[播种] & m13[浇水] & m14[收获]
  m2 --> m21[出售作物] & m22[购买种子]
  m3 --> m31[昼夜循环] & m32[季节切换]
  m4 --> m41[保存游戏] & m42[读取存档]
```

叶子节点超过 15 个时，按一级模块拆成多张图。

## 3. 业务流程图

```mermaid
flowchart TB
  s([开始]) --> a[玩家选择地块]
  a --> b{地块已翻耕?}
  b -- 否 --> c[使用锄头翻地] --> b
  b -- 是 --> d{背包有种子?}
  d -- 否 --> e[提示前往商店购买] --> z([结束])
  d -- 是 --> f[播种并记录播种时间] --> g[生长阶段随时间推进]
  g --> h{已成熟?}
  h -- 否 --> g
  h -- 是 --> i[收获作物放入背包] --> z
```

开始/结束用 `([ ])`，判断用 `{ }`，处理用 `[ ]`。

## 4. E-R 图

```mermaid
erDiagram
  PLAYER ||--o{ PLOT : 拥有
  PLOT ||--o| CROP : 种植
  CROP }o--|| CROP_TYPE : 属于
  PLAYER ||--|| INVENTORY : 持有
  INVENTORY ||--o{ ITEM : 包含
  PLAYER {
    string playerName
    int gold
    int day
  }
  CROP_TYPE {
    string id
    string name
    int growDays
    int sellPrice
  }
```

Mermaid 的 E-R 图是鸦脚标记法，不是陈氏（菱形）E-R 图。学校明确要求陈氏画法时，把 `.mmd` 当作草稿，提醒用户用 draw.io / ProcessOn 重画，或改用下面的 flowchart 近似画法：

```mermaid
flowchart LR
  P[玩家] --- R1{拥有} --- L[地块]
  L --- R2{种植} --- C[作物]
  P --- a1([玩家名]) & a2([金币]) & a3([天数])
```

## 5. 用例图（近似画法）

Mermaid 没有标准 UML 用例图，用 flowchart 近似：

```mermaid
flowchart LR
  actor((玩家))
  subgraph sys[农场游戏系统]
    direction TB
    u1([翻地与播种])
    u2([浇水与收获])
    u3([买卖物品])
    u4([保存与读取游戏])
  end
  actor --- u1 & u2 & u3 & u4
```

## 6. 类图

```mermaid
classDiagram
  class CropManager {
    -Dictionary~Vector3Int, Crop~ crops
    +Plant(Vector3Int pos, CropType type) bool
    +Water(Vector3Int pos) void
    +OnDayPassed() void
  }
  class Crop {
    +CropType type
    +int growthStage
    +bool watered
    +Grow() void
  }
  class CropType {
    +string id
    +int growDays
    +Sprite[] stageSprites
  }
  CropManager "1" o-- "*" Crop
  Crop --> CropType
```

类名、字段、方法必须和项目代码一致，只画核心类。

## 7. 时序图

```mermaid
sequenceDiagram
  participant 玩家
  participant UI as 存档界面
  participant SM as SaveManager
  participant FS as 本地文件
  玩家->>UI: 点击保存
  UI->>SM: SaveGame()
  SM->>SM: 收集玩家、地块、背包数据
  SM->>FS: 写入 save.json
  FS-->>SM: 写入完成
  SM-->>UI: 提示保存成功
```

## 8. 状态图

```mermaid
stateDiagram-v2
  [*] --> 种子
  种子 --> 幼苗: 浇水且经过1天
  幼苗 --> 生长期: 经过 growDays/2 天
  生长期 --> 成熟: 达到 growDays
  成熟 --> [*]: 收获
  幼苗 --> 枯萎: 连续2天未浇水
```

## 渲染效果问题

| 问题 | 处理 |
|---|---|
| 图太宽，缩到页面后字太小 | 改 `flowchart TB`，或 `subgraph` 里用 `direction TB` |
| 连线交叉多 | 调整节点声明顺序，或拆图 |
| 中文显示成方块 | 确认系统有宋体/黑体，或在 `mermaid.json` 里改字体 |
| 节点文字含括号、冒号报错 | 用引号包住：`a["存档(JSON)"]` |
