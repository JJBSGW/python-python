import requests
from bs4 import BeautifulSoup
import urllib3
import time

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 获取项目详细信息的函数
def get_project_comments(project_id):
    """
    根据项目ID获取项目的评论数量
    :param project_id: 项目ID
    :return: 项目ID和评论数量
    """
    url = f'https://zhongchou.modian.com/item/{project_id}.html'  # 生成对应的URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')


        # 提取评论数量（假设页面中评论数的位置）
        comment_count_element = soup.select_one('h3.tit.comment_num span')  # 假设评论数在这里
        if comment_count_element:
            comment_count = comment_count_element.get_text(strip=True)
        else:
            comment_count = "未找到评论数"

        title_element = soup.select_one('h3.title span')
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            title = "未找到标题"

        change_element = soup.select_one('li.pro-gengxin span')
        if change_element:
            change = change_element.get_text(strip=True)
        else:
            change = "未找到更新次数"

        commentback_count_element = soup.select_one('li.nav-commentst strong')  # 假设评论数在这里
        if commentback_count_element:
            commentback_count = commentback_count_element.get_text(strip=True)
        else:
            commentback_count = "未找到回报评论数"

        money_element = soup.select_one('div.col1.project-goal.success h3 span')  # 假设评论数在这里
        if money_element:
            money = money_element.get_text(strip=True)
        else:
            money = "未找到筹款金额"

        moneygoal_element = soup.select_one('span.goal-money')  # 假设评论数在这里
        if moneygoal_element:
            moneygoal = moneygoal_element.get_text(strip=True)
        else:
            moneygoal = "未找到目标金额"

        percent_element = soup.select_one('span.percent')  # 假设评论数在这里
        if percent_element:
            percent = percent_element.get_text(strip=True)
        else:
            percent = "未找到筹款百分比"

        people_element = soup.select_one('div.col3.support-people h3 span')  # 假设评论数在这里
        if people_element:
            people = people_element.get_text(strip=True)
        else:
            people = "未找到支持人数"

        print(f"{project_id}\n")
        return project_id, comment_count , title , change , commentback_count , money , moneygoal , percent , people

    except requests.exceptions.RequestException as e:
        print(f"抓取项目ID {project_id} 时出错: {e}")
        return project_id, "抓取失败"


# 从文件读取项目ID并抓取评论数
def read_ids_and_grab_comments(input_file, output_file):
    """
    从文件读取项目ID，并抓取评论数，然后保存到输出文件
    :param input_file: 输入文件（包含项目ID）
    :param output_file: 输出文件（保存评论数）
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        project_ids = [line.strip() for line in f.readlines()]  # 按行读取ID

    # 打开输出文件并写入结果
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for project_id in project_ids:
            project_id, comment_count , title , change , commentback_count , money , moneygoal , percent , people= get_project_comments(project_id)
            f_out.write(f"项目ID: {project_id}, 项目标题：{title} , 更新次数：{change}  , 回报评价数：{commentback_count}, 筹款金额:{money} , {moneygoal} , 筹款百分比:{percent} , 支持人数：{people}人, 评论数: {comment_count}\n")

    print(f"已保存到 {output_file}")


if __name__ == "__main__":
    input_file = 'project_ids_success.txt'  # 项目ID输入文件
    output_file = 'comments_success.txt'    # 评论数输出文件

    # 读取ID并抓取评论数
    read_ids_and_grab_comments(input_file, output_file)
