import requests
import json
from datetime import datetime, timedelta


def test_knife_statistics_api():
    # 服务器基础地址
    base_url = "http://39.98.115.114:8983"

    # 接口地址
    api_url = f"{base_url}/qw/knife/web/from/mes/statistics/chartsDeviceRanking"

    # 从token.txt读取token
    with open('token.txt', 'r', encoding='utf-8') as f:
        token_ = f.read().strip()

    # 设置请求头
    headers = {
        'Authorization': f'Bearer {token_}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }

    # 设置查询参数 - 这里设置一些示例参数，你可以根据需要调整
    params = {
        'startTime': '2025-01-01 00:00:00',  # 开始时间
        'endTime': '2025-12-31 23:59:59',  # 结束时间
        'order': 0,  # 0:从大到小 1：从小到大
        'rankingType': 0,  # 0:数量 1:金额
        'recordStatus': 0  # 0:取刀 1:还刀 2:收刀 3:暂存 4:完成 5：违规还刀
    }

    try:
        # 发送GET请求
        response = requests.get(
            url=api_url,
            headers=headers,
            params=params,
            timeout=30  # 设置超时时间
        )

        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        # 尝试解析JSON响应
        try:
            json_data = response.json()
            print("响应数据 (JSON格式):")
            print(json.dumps(json_data, indent=2, ensure_ascii=False))

            # 保存响应到文件以便后续分析
            with open('api_response.json', 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print("\n响应数据已保存到 api_response.json 文件")

        except json.JSONDecodeError:
            print("响应不是有效的JSON格式")
            print("原始响应内容:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def test_with_different_parameters():
    """测试不同参数组合的响应"""
    base_url = "http://39.98.115.114:8983"
    api_url = f"{base_url}/qw/knife/web/from/mes/statistics/chartsDeviceRanking"

    with open('token.txt', 'r', encoding='utf-8') as f:
        token_ = f.read().strip()

    headers = {
        'Authorization': f'Bearer {token_}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }

    # 不同的参数组合测试
    test_cases = [
        {
            'name': '数量排名-从大到小',
            'params': {
                'startTime': '2024-01-01 00:00:00',
                'endTime': '2024-12-31 23:59:59',
                'order': 0,
                'rankingType': 0,
                'recordStatus': 0
            }
        },
        {
            'name': '金额排名-从小到大',
            'params': {
                'startTime': '2024-01-01 00:00:00',
                'endTime': '2024-12-31 23:59:59',
                'order': 1,
                'rankingType': 1,
                'recordStatus': 1
            }
        },
        {
            'name': '仅时间范围',
            'params': {
                'startTime': '2024-06-01 00:00:00',
                'endTime': '2024-06-30 23:59:59'
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n{'=' * 50}")
        print(f"测试用例: {test_case['name']}")
        print(f"参数: {test_case['params']}")
        print('=' * 50)

        try:
            response = requests.get(
                url=api_url,
                headers=headers,
                params=test_case['params'],
                timeout=30
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                try:
                    json_data = response.json()
                    print("响应数据结构:")
                    print(f"数据类型: {type(json_data)}")
                    if isinstance(json_data, dict):
                        print(f"包含字段: {list(json_data.keys())}")
                    elif isinstance(json_data, list):
                        print(f"数组长度: {len(json_data)}")
                        if len(json_data) > 0:
                            print(f"数组元素类型: {type(json_data[0])}")
                            if isinstance(json_data[0], dict):
                                print(f"第一个元素的字段: {list(json_data[0].keys())}")

                    # 保存到单独的文件
                    filename = f"response_{test_case['name']}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                    print(f"响应已保存到: {filename}")

                except json.JSONDecodeError:
                    print("响应不是有效的JSON格式")
                    print(f"原始响应: {response.text[:200]}...")  # 只显示前200个字符
            else:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"错误信息: {response.text}")

        except Exception as e:
            print(f"请求异常: {e}")


if __name__ == "__main__":
    print("开始测试刀具统计API...")

    # 执行基本测试
    print("\n1. 基本API测试:")
    test_knife_statistics_api()

    # 执行多参数测试
    print("\n2. 多参数组合测试:")
    test_with_different_parameters()