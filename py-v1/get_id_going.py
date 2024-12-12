import requests
import re
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_project_ids(base_url):
    """
    爬取指定URL下所有页面的项目ID，通过正则表达式提取
    :param base_url: 网站的基础URL
    :return: 所有项目ID列表
    """
    project_ids = []
    page = 1  # 初始页码
    pattern = re.compile(r'data-pro-id="(\d+)"')  # 匹配 data-pro-id 的正则表达式

    while True:
        print(f"正在抓取第 {page} 页...")
        # 构造分页URL
        url = f"{base_url}/{page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, verify=False, proxies={"http": None, "https": None})
            response.raise_for_status()

            # 获取整个HTML内容
            html_content = response.text

            # 使用正则表达式提取所有的 data-pro-id 值
            ids = pattern.findall(html_content)
            if not ids:
                print("没有更多项目，抓取结束。")
                break

            project_ids.extend(ids)
            page += 1  # 进入下一页

        except requests.exceptions.RequestException as e:
            print(f"抓取第 {page} 页时出现错误: {e}")
            break

    return project_ids

def save_to_txt(data, filename):
    """
    将数据保存到TXT文件
    :param data: 要保存的数据（列表）
    :param filename: 文件名
    """
    with open(filename, "w", encoding="utf-8") as f:
        for item in data:
            f.write(item + "\n")  # 每个ID单独一行

if __name__ == "__main__":
    base_url = "https://zhongchou.modian.com/food/top_comment/going"
    ids = get_project_ids(base_url)
    print(f"共抓取到 {len(ids)} 个项目ID：")
    print(ids)

    # 保存到 TXT 文件
    save_to_txt(ids, "project_ids_going.txt")
    print("数据已保存到 project_ids_going.txt")
