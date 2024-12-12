from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

# 设置浏览器选项，启用无头模式
options = Options()
options.headless = True

# 初始化浏览器驱动
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# 从project_ids.txt文件中读取项目ID
with open('project_ids_going.txt', 'r', encoding='utf-8') as file:
    project_ids = [line.strip() for line in file.readlines()]

# 用来保存所有评论的列表
comments = []

# 爬取每个项目ID的评论
for project_id in project_ids:
    # 标记是否已经添加过项目标题
    title_added = False
    url = f'https://zhongchou.modian.com/item/{project_id}.html'
    driver.get(url)

    try:
        # 等待标题加载完成
        title_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.title span')))
        # 提取标题
        title = title_element.text
    except TimeoutException:
        print(f"项目ID {project_id} 标题加载超时，跳过该项目")
        continue

    try:
        # 等待评论区加载完成
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.comment-lists')))
    except TimeoutException:
        print(f"项目ID {project_id} 评论区加载超时，跳过该项目")
        continue

    # 滚动页面以加载更多评论
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        comments_elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.comment-list')))
    except TimeoutException:
        print(f"项目ID {project_id} 评论加载超时")
        continue

    for comment in comments_elements:
        try:
            # 等待并提取评论者的用户名和评论内容
            user_name_elem = WebDriverWait(comment, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.nickname a')))
            comment_text_elem = WebDriverWait(comment, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.comment-txt')))
            user_name = user_name_elem.text
            comment_text = comment_text_elem.text
            # 将提取的评论保存到列表中
            if not title_added:
                comments.append({'项目标题': title})
                title_added = True
            comments.append({'用户名': user_name, '评论内容': comment_text})
        except StaleElementReferenceException:
            print(f"项目ID {project_id} 中的评论元素引用失效，重新尝试加载")
            continue
        except Exception as e:
            print(f"项目ID {project_id} 中出现异常: {e}")

# 将所有评论写入文件
with open('comments_going.txt', 'w', encoding='utf-8') as file:
    for comment in comments:
        if '项目标题' in comment:
            file.write(f"项目标题: {comment['项目标题']}\n\n")
        else:
            file.write(f"用户名: {comment['用户名']}\n")
            file.write(f"评论内容: {comment['评论内容']}\n\n")

# 退出浏览器
driver.quit()
