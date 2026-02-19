#!/usr/bin/env python3
"""弹弓瞄准计算器 v2.0 - 快速计算瞄准补偿

用法:
  1. 配置: slingshot config <弹丸> <皮筋股数> [实测初速m/s]
  2. 计算: slingshot calc <距离米>

特点:
  - 先配置参数，记住配置
  - 以后只要说距离，告诉我瞄准点
"""

import math
import json
import os
from pathlib import Path

G = 9.81  # 重力加速度 m/s²
CONFIG_FILE = os.environ.get('SLINGSHOT_CONFIG', '~/.slingshot_config.json')

AMMO_TYPES = {
    "8mm钢珠": 2.08,
    "9.5mm钢珠": 3.6,
    "10mm钢珠": 4.2,
    "11mm钢珠": 5.6,
    "12mm钢珠": 7.0,
    "玻璃弹珠": 1.5,
    "黏土弹": 0.8,
    "7mm钢珠": 1.4,
    "9mm钢珠": 3.0,
}

def load_config():
    path = Path(CONFIG_FILE).expanduser()
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    path = Path(CONFIG_FILE).expanduser()
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
    return path

def calculate_aim(v0, distance):
    """计算瞄准补偿
    
    弹道公式:
    - 水平: x = v0 * cos(θ) * t
    - 垂直: y = v0 * sin(θ) * t - 0.5 * g * t²
    
    目标: 已知x=distance，求y
    """
    angle = 45  # 默认45度
    rad = math.radians(angle)
    
    # 飞行时间
    t = distance / (v0 * math.cos(rad))
    
    # 垂直位移（子弹落点时的y值，理论上应该是0）
    # 但由于我们固定45度，distance可能是任意值
    # 所以需要计算的是：子弹在飞行时间t内的弹道高度曲线
    
    # 弹道最高点时间
    t_up = v0 * math.sin(rad) / G
    
    # 弹道最高点高度
    h_max = v0 * math.sin(rad) * t_up - 0.5 * G * t_up * t_up
    
    # 实际飞行时间内的最大高度（在t时刻的y值）
    # 抛物线: y = v0*sin*g*t - 0.5*g*t²
    # 在飞行时间t时的高度
    y_at_t = v0 * math.sin(rad) * t - 0.5 * G * t * t
    
    # 瞄准建议：打在弹道最高点下方一些（大约在2/3高度处）
    if y_at_t > 0:
        aim_height = y_at_t * 0.4
    else:
        aim_height = h_max * 0.4
    
    return {
        "v0": v0,
        "distance": distance,
        "angle": angle,
        "flight_time": round(t, 2),
        "max_height": round(h_max, 2),
        "aim_cm": round(aim_height * 100, 0),
        "suggestion": f"瞄准目标上方约{aim_height*100:.0f}cm"
    }

def main():
    import sys
    
    config = load_config()
    script_name = os.path.basename(sys.argv[0])
    
    print("=" * 50)
    print("🎯 弹弓瞄准计算器 v2.0")
    print("=" * 50)
    
    if config:
        print(f"\n📋 当前配置:")
        print(f"   弹丸: {config['ammo']}")
        print(f"   皮筋: {config['bands']}股")
        print(f"   初速: {config['v0']} m/s")
        print(f"   能量: {config.get('energy', '?')} J")
    else:
        print("\n⚠️ 未配置")
    
    print("\n用法:")
    print(f"   {script_name} config <弹丸> <皮筋股数> [实测初速]")
    print(f"   {script_name} calc <距离>")
    print(f"   {script_name} ammo  (查看弹丸类型)")
    
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        
        if cmd == "config" and len(sys.argv) >= 4:
            ammo = sys.argv[2]
            bands = int(sys.argv[3])
            v0 = float(sys.argv[4]) if len(sys.argv) > 4 else 50
            
            config = {
                "ammo": ammo,
                "bands": bands,
                "v0": v0,
                "energy": round(v0 * v0 * AMMO_TYPES.get(ammo, 2.08) / 2000, 2),
                "timestamp": "2026-02-19"
            }
            path = save_config(config)
            
            print(f"\n✅ 配置已保存!")
            print(f"   弹丸: {ammo}")
            print(f"   皮筋: {bands}股")
            print(f"   初速: {v0} m/s")
            print(f"   能量: {config['energy']} J")
            print(f"\n💡 以后: {script_name} calc <距离>")
            
        elif cmd == "calc" and len(sys.argv) >= 3:
            if not config:
                print("\n❌ 请先配置: slingshot config <弹丸> <皮筋股数> [初速]")
                return
                
            distance = float(sys.argv[2])
            result = calculate_aim(config['v0'], distance)
            
            print(f"\n📊 {distance}米目标:")
            print(f"   初速: {result['v0']} m/s")
            print(f"   角度: {result['angle']}°")
            print(f"   飞行: {result['flight_time']}s")
            print(f"   ─────────────")
            print(f"   🎯 {result['suggestion']}")
            print(f"\n💡 {distance}m，打在目标上方{result['aim_cm']}cm处！")
                
        elif cmd == "ammo":
            print("\n📦 支持的弹丸:")
            for name, mass in AMMO_TYPES.items():
                print(f"   {name}: {mass}g")
        
        else:
            print("\n❌ 命令错误")
    
    else:
        print("\n💡 直接告诉我距离，我来算瞄准点!")

if __name__ == "__main__":
    main()
