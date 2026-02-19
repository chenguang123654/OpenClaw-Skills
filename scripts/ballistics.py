#!/usr/bin/env python3
"""弹道计算器 - 计算抛物线轨迹和落点"""

import math

G = 9.81  # 重力加速度 m/s²

# 常见弹丸参数
AMMO_TYPES = {
    "8mm钢珠": {"mass": 2.08, "diameter": 0.008},      # 克, 米
    "9.5mm钢珠": {"mass": 3.6, "diameter": 0.0095},
    "10mm钢珠": {"mass": 4.2, "diameter": 0.010},
    "11mm钢珠": {"mass": 5.6, "diameter": 0.011},
    "12mm钢珠": {"mass": 7.0, "diameter": 0.012},
    "玻璃弹珠": {"mass": 1.5, "diameter": 0.010},
    "黏土弹": {"mass": 0.8, "diameter": 0.008},
    "7mm钢珠": {"mass": 1.4, "diameter": 0.007},
}

def calculate_basic(v0, angle_deg, h0=0):
    """基本弹道计算
    
    Args:
        v0: 初速 (m/s)
        angle_deg: 发射角度 (度)
        h0: 初始高度 (m)
    
    Returns:
        dict: 计算结果
    """
    angle_rad = math.radians(angle_deg)
    sin_a = math.sin(angle_rad)
    cos_a = math.cos(angle_rad)
    
    # 飞行时间（从发射到落地）
    a = 0.5 * G
    b = -v0 * sin_a
    c = -h0
    
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return {"error": "无法命中目标"}
    
    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    flight_time = max(t1, t2)  # 取较大的解
    
    # 落点距离
    distance = v0 * cos_a * flight_time
    
    # 最大高度
    t_up = v0 * sin_a / G
    h_max = v0 * sin_a * t_up - 0.5 * G * t_up * t_up + h0
    
    # 生成轨迹数据
    trajectory = []
    dt = 0.1
    t = 0
    while t <= flight_time:
        x = v0 * cos_a * t
        y = v0 * sin_a * t - 0.5 * G * t * t + h0
        if y >= 0:
            trajectory.append({"t": round(t, 1), "x": round(x, 2), "y": round(y, 2)})
        t += dt
    
    return {
        "flight_time": round(flight_time, 2),
        "max_height": round(h_max, 2),
        "distance": round(distance, 2),
        "trajectory": trajectory
    }

def calculate_angle(v0, distance, h0=0, h_target=0):
    """根据初速和距离计算射击角度"""
    v2 = v0 * v0
    
    # 最大射程（45度，无高度差）
    max_range = v2 / G
    if distance > max_range:
        return {"error": f"距离太远！初速{v0}m/s最大射程约{max_range:.1f}m"}
    
    # 抛物线近似公式
    term1 = distance * G / v2
    sin_2theta = min(term1, 1.0)  # 限制在1以内
    
    theta1 = 0.5 * math.degrees(math.asin(sin_2theta))
    theta2 = 90 - theta1
    
    results = []
    for theta in [theta1, theta2]:
        if 1 <= theta <= 89:  # 只返回合理角度
            angle_rad = math.radians(theta)
            sin_a = math.sin(angle_rad)
            cos_a = math.cos(angle_rad)
            
            a = 0.5 * G
            b = -v0 * sin_a
            c = -h0 + h_target
            
            discriminant = b*b - 4*a*c
            if discriminant < 0:
                continue
                
            t = (-b + math.sqrt(discriminant)) / (2*a)
            calc_distance = v0 * cos_a * t
            
            results.append({
                "angle": round(theta, 2),
                "flight_time": round(t, 2),
                "distance": round(calc_distance, 2),
                "suggestion": "低角度精准" if theta < 45 else "高角度抛射"
            })
    
    return {"required_angle": results}

def calculate_energy(ammo_type, bands):
    """计算弹弓能量
    
    Args:
        ammo_type: 弹丸类型
        bands: 皮筋股数
    
    Returns:
        dict: 能量参数
    """
    if ammo_type in AMMO_TYPES:
        ammo = AMMO_TYPES[ammo_type]
    else:
        # 默认使用8mm
        ammo = AMMO_TYPES["8mm钢珠"]
    
    mass = ammo["mass"] / 1000  # 转换为kg
    
    # 皮筋能量估算（简化公式）
    energy_per_band = 0.3  # 每股约0.3J
    total_energy = energy_per_band * bands
    
    v0_estimated = math.sqrt(2 * total_energy / mass) if mass > 0 else 0
    
    return {
        "ammo_type": ammo_type,
        "mass_g": ammo["mass"],
        "bands": bands,
        "estimated_energy_j": round(total_energy, 2),
        "estimated_v0_ms": round(v0_estimated, 1),
        "estimated_fps": round(v0_estimated * 3.28, 1)
    }

def main():
    import sys
    
    print("=" * 50)
    print("🎯 弹道计算器 v1.1.0")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("""
用法: python3 ballistics.py <命令> <参数...>

命令:
  basic <初速> <角度> [高度]
    计算基本弹道
    示例: basic 50 45 0
    
  angle <初速> <距离> [发射高度] [目标高度]
    计算射击角度
    示例: angle 60 20 0 0
  
  energy <弹丸类型> <皮筋股数>
    估算弹弓能量
    示例: energy "8mm钢珠" 18
  
  ammo
    显示支持的弹丸类型

弹丸类型: 8mm钢珠, 9.5mm钢珠, 10mm钢珠, 11mm钢珠, 12mm钢珠, 玻璃弹珠, 黏土弹
""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "basic" and len(sys.argv) >= 4:
        v0 = float(sys.argv[2])
        angle = float(sys.argv[3])
        h0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        result = calculate_basic(v0, angle, h0)
        
        print(f"\n📊 计算结果:")
        print(f"  初速: {v0} m/s")
        print(f"  角度: {angle}°")
        print(f"  发射高度: {h0} m")
        print(f"  ─────────────")
        print(f"  飞行时间: {result['flight_time']} s")
        print(f"  最大高度: {result['max_height']} m")
        print(f"  落点距离: {result['distance']} m")
        
    elif cmd == "angle" and len(sys.argv) >= 4:
        v0 = float(sys.argv[2])
        distance = float(sys.argv[3])
        h0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
        h_target = float(sys.argv[5]) if len(sys.argv) > 5 else 0
        result = calculate_angle(v0, distance, h0, h_target)
        
        if "error" in result:
            print(f"\n❌ {result['error']}")
        else:
            print(f"\n🎯 推荐射击角度:")
            for r in result['required_angle']:
                print(f"  {r['angle']}° ({r['suggestion']}) - 飞行时间 {r['flight_time']}s")
        
    elif cmd == "energy" and len(sys.argv) >= 4:
        ammo = sys.argv[2]
        bands = int(sys.argv[3])
        result = calculate_energy(ammo, bands)
        
        print(f"\n⚡ 能量估算:")
        print(f"  弹丸: {result['ammo_type']}")
        print(f"  质量: {result['mass_g']} g")
        print(f"  皮筋: {result['bands']} 股")
        print(f"  ─────────────")
        print(f"  估算动能: {result['estimated_energy_j']} J")
        print(f"  估算初速: {result['estimated_v0_ms']} m/s")
        print(f"  估算速度: {result['estimated_fps']} FPS")
        
    elif cmd == "ammo":
        print("\n📦 支持的弹丸类型:")
        for name, data in AMMO_TYPES.items():
            print(f"  {name}: {data['mass']} g")
    
    else:
        print(f"\n❌ 未知命令或参数不足: {cmd}")

if __name__ == "__main__":
    main()
