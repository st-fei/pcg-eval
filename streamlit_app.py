import os
import json
import random
import streamlit as st
from datetime import datetime
from database import DataBase
from config import get_cfg
from tools import load_json
from PIL import Image

class UI:
    def __init__(self, cfg: dict):
        # 只有参数保持不变
        self.cfg = cfg
        self.database = DataBase(cfg=cfg)
    
    def load_image(self, image_urls: list):
        target_size = (200, 200)
        combined_image = Image.new('RGB', (target_size[0] * 3, target_size[1]))
        for i in range(len(image_urls)):
            img = Image.open(image_urls[i])
            _img = img.resize(target_size)
            combined_image.paste(_img, (target_size[0] * i, 0))
        return combined_image

    def show_intro(self):
        '''Survey introduction ui'''
        col1, col2 = st.columns([8.2, 1.8])
        with col1:
            st.markdown(f"""
                <div style="border: 2px solid #ccc; padding: 8px; border-radius: 3px;">
                    <h4 style="color: #2978b5;">📘 Survey: Personalized Post Title Generation</h4>
                    <p style="font-weight: bold; font-style: italic; margin-left:20px">欢迎您对我们工作的支持，您当前所处的页面为{st.session_state['page_index'] + 1}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            intro_img_path = "/workspaces/pcg-eval/data/icon/rainbow.png"
            st.image(intro_img_path, width=200)
        


    def show_profile(self):
        anonymous_name = self.anonymous_list[st.session_state['page_index']]
        anonymous_data = self.show_data[anonymous_name]
        # 从anonymous_data中获取user
        user = anonymous_data['user']
        # 构建profile模块
        sex = user['sex']
        job = user['job']
        desc = user['desc_info']
        st.markdown(f"""
            <div style="padding: 20px; border: 2px solid #363a60; border-radius: 10px; margin: 10px 0; background-color: #f9f9f9;">
                <h4 style="color: #2978b5; margin-bottom: 5px;">👨‍🚀 用户简介</h4>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>性别:</b> {sex}</p>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>职业:</b> {job}</p>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>个性签名:</b> {desc}</p>
            </div>
        """, unsafe_allow_html=True)

    def show_history(self):
        anonymous_name = self.anonymous_list[st.session_state['page_index']]
        anonymous_data = self.show_data[anonymous_name]
        # 从anonymous_data中获取history note
        history_list = anonymous_data['history']
        
        # 历史笔记
        st.markdown("""
            <div style="border: 2px solid #ccc; padding: 8px; border-radius: 10px; background-color: #f9f9f9;">
                <h4 style="color: #2978b5;">📗历史笔记:</h4>
            """, unsafe_allow_html=True
        )
        
        for i, history_note in enumerate(history_list):
            title = history_note['title']
            image_prefix = history_note['sample_prefix']
            combined_img_path = os.path.join(self.cfg['FILE_PATH']['sample_img_dir'], image_prefix)

            # 每条笔记内部使用HTML和CSS来进一步格式化和分隔
            st.markdown(f"""
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
                    <p style="font-weight: bold; margin-bottom: 5px;">第{i+1}条历史笔记:</p>
                    <p style="margin-bottom: 5px;"><b>标题:</b> {title}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 显示组合图像
            st.image(combined_img_path)
        
    def show_target(self):
        anonymous_name = self.anonymous_list[st.session_state['page_index']]
        anonymous_data = self.show_data[anonymous_name]
        # 从anonymous_data中获取target note
        target_note = anonymous_data['target']
        # 目标笔记
        st.markdown("""
            <div style="border: 2px solid #ccc; padding: 8px; border-radius: 10px; background-color: #f9f9f9;">
                <h4 style="color: #2978b5;">📙最新笔记:</h4>
            """, unsafe_allow_html=True
        )
        st.markdown(f"""
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee;">
            <p style="font-weight: bold; margin-bottom: 5px;">用户最新笔记图像如下:</p>
        </div>
        """, unsafe_allow_html=True)
        image_prefix = target_note['sample_prefix']
        combined_img_path = os.path.join(self.cfg['FILE_PATH']['sample_img_dir'], image_prefix)
        st.image(combined_img_path)

    def show_rank(self):
        # 模型评估头部
        st.markdown("""
            <style>
                .rowFlex {
                    display: flex;
                    flex-wrap: wrap;
                    align-items: stretch; /* 使所有列高度一致 */
                }
                .columnFlex {
                    flex: 1; /* 每列占用等宽 */
                    margin: 5px; /* 间隔 */
                    border: 1px solid #aaa;
                    padding: 10px;
                    border-radius: 5px;
                }
            </style>
            <div style="border: 2px solid #ccc; padding: 8px; border-radius: 10px; background-color: #f9f9f9;">
                <h4 style="color: #2978b5;">🤖模型评估:</h4>
            </div>
        """, unsafe_allow_html=True)

        anonymous_name = self.anonymous_list[st.session_state['page_index']]
        model_list = list(self.gen_data.keys())
        

        # 准备数据和映射
        base_letter = 'A'
        model_map = {}
        model_reverse_map = {}

        # 结果展示
        st.markdown('<div class="rowFlex">', unsafe_allow_html=True)
        for i, model_name in enumerate(model_list):
            model_map[f'model_{chr(ord(base_letter) + i)}'] = model_name
            model_reverse_map[model_name] = f'model_{chr(ord(base_letter) + i)}'
            title = self.gen_data[model_name][anonymous_name]
            show_title = title[:20] if title != '' else 'None'
            # 使用自定义 flex 列
            st.markdown(f"""
                <div class="columnFlex">
                    <strong>{model_reverse_map[model_name]}:</strong> {show_title}
                </div>
            """, unsafe_allow_html=True)

        # 结束 flex 容器
        st.markdown('</div>', unsafe_allow_html=True)

        # 创建ranking
        max_ranks = self.cfg['UI']['max_rank']
        if anonymous_name not in st.session_state['rank']:
            st.session_state['rank'][anonymous_name] = {
                f'rank_{i+1}':{'model_name': 'NULL', 'gen_res': 'NULL'} for i in range(max_ranks)
        }    

        # 模型评估
        options = list(model_map.keys()) + ['NULL']  # 初始化选项为所有模型标签
        columns = st.columns(max_ranks)
        for i in range(max_ranks):
            with columns[i]:
                selected_model = st.selectbox(f"选择质量第 {i+1} 高的模型:", options, key=f"rank_{i+1}")
                if selected_model != 'NULL':
                    selected_model_name = model_map[selected_model]
                    # 匹配模型rank
                    st.session_state['rank'][anonymous_name][f'rank_{i+1}']['model_name'] = selected_model_name
                    st.session_state['rank'][anonymous_name][f'rank_{i+1}']['gen_res'] = self.gen_data[selected_model_name][anonymous_name]

                   
                    

    def show_next(self):

        # 进度条
        total_pages = len(self.anonymous_list)
        current_page = st.session_state['page_index'] + 1
        progress_value = current_page / total_pages
        st.progress(progress_value)
        
        cols = st.columns([1, 5, 1]) 

        with cols[0]:  # 第一列
            # 只在不是第一页时显示“上一页”按钮
            if st.session_state['page_index'] > 0:
                if st.button('上一页'):
                    self.back_data()

        with cols[2]:  # 第三列
            # 在不是最后一页时显示“下一页”按钮
            if st.session_state['page_index'] < len(self.anonymous_list) - 1:
                if st.button('下一页'):
                    self.forward_data()
            # 在最后一页时显示“提交问卷”按钮
            elif st.session_state['page_index'] == len(self.anonymous_list) - 1:
                if st.button('提交问卷'):
                    st.write('感谢您的参与')
                    # ranking结果保存
                    json_str = json.dumps(st.session_state['rank'], ensure_ascii=False, indent=4)
                    now = datetime.now()
                    formatted_date = now.strftime("%Y-%m-%d-%H%M%S")
                    st.download_button(
                        label='Download Json result',
                        data=json_str,
                        file_name=f'{formatted_date}.json',
                        mime='application/json'
                    )
                    self.database.post_process(group_id=int(st.session_state['select_id']))



    def show(self, ):

        self.show_intro()
        self.show_profile()
        self.show_history()
        self.show_target()
        self.show_rank()
        self.show_next()

    # 更新数据
    def forward_data(self):
        print("当前页码：{} -> {}".format(st.session_state['page_index'], self.anonymous_list[st.session_state['page_index']]))  # 打印当前页码
        st.session_state['page_index'] = st.session_state['page_index'] + 1
        print("翻页后页码：{} -> {}".format(st.session_state['page_index'], self.anonymous_list[st.session_state['page_index']]))  # 打印当前页码
        st.rerun()

    def back_data(self):
        print("当前页码：{} -> {}".format(st.session_state['page_index'], self.anonymous_list[st.session_state['page_index']]))  # 打印当前页码
        st.session_state['page_index'] = st.session_state['page_index'] - 1
        print("回退后页码：{} -> {}".format(st.session_state['page_index'], self.anonymous_list[st.session_state['page_index']]))  # 打印当前页码
        st.rerun()

    def run(self):

        # 初始化session
        if 'page_index' not in st.session_state:
            st.session_state['page_index'] = 0
        if 'select_id' not in st.session_state:
            select_id = self.database.select()
            st.session_state['select_id'] = select_id
        else:
            select_id = st.session_state['select_id']
        if 'rank' not in st.session_state:
            st.session_state['rank'] = {}


        print(f'当前选取组ID为:{select_id}')
        # 该组的展示数据
        self.show_data = self.database.get(group_id=select_id)
        # 获取anonymous_list
        self.anonymous_list = [name for name in self.show_data if name != 'count']
        print(f'当前匿名列表为:{self.anonymous_list}')
        # 所有模型的生成数据
        self.gen_data = self.database.gen_res
        # 获取ui界面
        self.show()

@st.fragment
def Create(cfg: dict):
    ui = UI(cfg=cfg)
    return ui

if __name__ == '__main__':
    cfg = get_cfg()
    ui = Create(cfg=cfg)
    ui.run()

        
    
    




