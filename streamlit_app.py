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

    def show_init(self):
        self.show_intro()
        self.show_example()
        self.show_next()


    def show_example(self):
        # 展示样例
        st.markdown("### 🎉参考示例")
        st.write("**以下是一个问卷实例，帮助您了解如何分析并填写该问卷**")
        # 准备数据
        anonymous_name = "2O4P7O"
        example_data = {
            "user": {
                "url": "https://www.xiaohongshu.com/user/profile/647060aa000000002b008a65",
                "raw_name": "王大维v",
                "sex": "男",
                "desc_info": "“这世界的一切 都在吸引我”\n➡️ 1187250508@qq.com",
                "splm_info": "unk",
                "job": "户外博主",
                "concern_num": 18,
                "fans_num": 50736,
                "like_num": 470318
            },  
            "history": [
                {
                    "title": "以为青岛够美了，直到我去了连云港…",
                    "image_indexs": [
                        118688,
                        118692,
                        118696
                    ],
                    "image_urls": [
                        "/data/tfshen/pcg_imagebase/image_base6/image_118688.png",
                        "/data/tfshen/pcg_imagebase/image_base6/image_118692.png",
                        "/data/tfshen/pcg_imagebase/image_base6/image_118696.png"
                    ],
                    "sample_prefix": "Group_2-2O4P7O-1.png"
                },
                {
                    "title": "为什么山西的古建筑都这么美❓",
                    "image_indexs": [
                        118697,
                        118702,
                        118708
                    ],
                    "image_urls": [
                        "/data/tfshen/pcg_imagebase/image_base6/image_118697.png",
                        "/data/tfshen/pcg_imagebase/image_base6/image_118702.png",
                        "/data/tfshen/pcg_imagebase/image_base6/image_118708.png"
                    ],
                    "sample_prefix": "Group_2-2O4P7O-2.png"
                }
            ],
            "target": {
                "title": "我很少用“震撼”来形容一个地方",
                "image_indexs": [
                    118709,
                    118712,
                    118716
                ],
                "image_urls": [
                    "/data/tfshen/pcg_imagebase/image_base6/image_118709.png",
                    "/data/tfshen/pcg_imagebase/image_base6/image_118712.png",
                    "/data/tfshen/pcg_imagebase/image_base6/image_118716.png"
                ],
                "sample_prefix": "Group_2-2O4P7O-3.png"
            }
        }
        # profile 
        st.markdown(f"""
            <div style="padding: 20px; border: 2px solid #363a60; border-radius: 10px; margin: 10px 0; background-color: #f9f9f9;">
                <h4 style="color: #2978b5; margin-bottom: 5px;">👨‍🚀 用户简介</h4>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>性别:</b> {example_data["user"]["sex"]}</p>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>职业:</b> {example_data["user"]["job"]}</p>
                <p style="font-weight: bold; margin-bottom: 5px;"><b>个性签名:</b> {example_data["user"]["desc_info"]}</p>
            </div>
        """, unsafe_allow_html=True)
        # history
        history_list = example_data['history']
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

        # target
        target_note = example_data['target']
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

        # rank
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

        true_title = example_data['target']['title']
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
            show_title = title[:25] if title != '' else 'None'
            # 使用自定义 flex 列
            st.markdown(f"""
                <div class="columnFlex">
                    <strong>{model_reverse_map[model_name]}:</strong> {show_title}
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
                <div class="columnFlex">
                    <strong>{"真实标题"}:</strong> {true_title}
                </div>
        """, unsafe_allow_html=True)

        # 结束 flex 容器
        st.markdown('</div>', unsafe_allow_html=True)

        # 创建ranking
        max_ranks = self.cfg['UI']['max_rank']

        # 模型评估
        options = list(model_map.keys()) + ['NULL']  # 初始化选项为所有模型标签
        columns = st.columns(max_ranks)
        for i in range(max_ranks):
            with columns[i]:
                selected_model = st.selectbox(f"选择质量第 {i+1} 高的模型:", options, key=f"rank_{i+1}")
        
        # tag
        st.markdown("### 🏷️个性化标签与情绪标签")

        # 个性化标签输入
        st.markdown("**个性化标签**")
        personalization_options = ["探索", "艺术", "自然", "科技", "设计", "温馨", "书籍", "自拍", "好物分享", "其他"]
        selected_personalization_tags = st.multiselect("请选择用户的个性化标签（可多选）", personalization_options)

        # 情绪标签选择
        st.markdown("**情绪标签**")
        emotion_options = ["期待", "好奇", "惊叹", "放松", "愉悦", "emo", "分享欲", "中性"]
        selected_emotion_tags = st.multiselect("请选择用户的情绪标签（可多选）", emotion_options)

        # 示例讲解
        st.markdown("### 📝示例讲解")
        st.write("""
        **用户画像分析**:
        - **个人简介:** 此示例中的用户是一位**户外博主**，个人简介中提到“**这世界的一切都在吸引我**”，展现了他对自然景观的强烈探索欲。
        - **历史发帖:** 用户的历史发帖标题涉及**地理位置**和自然美景的描述，如"青岛"、"连云港"、"山西的古建筑"等，表明他倾向于记录中国各地的特色风景。
        - **最新发帖:** 用户最新发帖的标题使用了“震撼”一词来描述佛像，这反映出他在标题中更习惯于表达自己的**情绪转折**，而非简单的客观描述。

        **模型生成评估**：
        - **筛选与排除:** 首先排除生成质量明显较差的模型（如 model_A、model_C、model_D）。
        - **重复性检查:** 在**与历史标题的重复程度**方面，发现 model_B 只是对历史标题的简单重复，因此被归为质量较差; model_F 和 model_G 在历史标题基础上进行扩展，不视为质量较差，但在排序时酌情扣分。
        - **情绪与表达习惯分析:** 针对生成质量较高的模型（model_E、model_F、model_G、model_H），具体分析如下：
             - **表达习惯:** 虽然该用户的标题风格没有固定的格式（如 xxx|yyy），但他倾向于在标题中提及中国地名。因此，如果生成标题中包含地名，则在表达习惯上更符合用户风格（model_F、model_G）。
             - **情绪状态:** 用户倾向于在标题中表达出浓厚的探索欲和情绪转折，model_H 和 model_F 在标题中较好地体现了这种情绪特征，考虑适当加分。
             - **总结:** 由于 model_E 和 model_G 的生成标题偏向陈述性叙述，缺乏用户的情绪表达，最终质量排序为 model_H > model_F > model_E > model_G。
        """)

        
    def show_intro(self):
        st.markdown(f"""
                <div style="border: 2px solid #ccc; padding: 8px; border-radius: 3px;">
                    <h4 style="color: #2978b5;">📘 Survey: Personalized Post Title Generation</h4>
                </div>
        """, unsafe_allow_html=True)
        st.markdown("")

        # 参考标准左栏显示
        # 使用 st.sidebar 设置注意事项内容
        with st.sidebar:
            st.markdown("### 注意事项")
            st.write("1. 请确保填写所有必填项。")
            st.write("2. 若遇到问题，请联系作者。")
            st.write("3. 请用 **浏览器** 打开该网页以便于文件下载。")
            st.markdown("### 选择标准")
            st.write("1. 与历史标题的重复程度")
            st.write("2. 是否符合用户表达习惯")
            st.write("3. 是否符合用户情绪状态")
            st.write("4. 与真实标题的风格贴合")
            st.write("5. 若发现某个模型生成结果与真实标签完全一样，请不要选择该模型")

        # 问卷介绍
        with st.expander("问卷介绍"):
            st.markdown("### 📄问卷介绍")
            st.markdown("""
                本问卷旨在评估不同模型生成个性化笔记标题的质量。

                对于每一页问卷，请你分别阅读 **用户简介**、**历史笔记**，分析该用户的个性爱好、情绪状态、表达习惯。
                在上述基础上，不同模型为用户的最新笔记设计了不同的个性化标题。

                你可以参考以下几个角度进行质量排序：
                - **与历史标题的重复程度**：若模型只是简单对历史标题进行重复或拼接，则一律认为质量不佳。
                - **表达习惯**：是否符合用户历史笔记的表达习惯。
                - **情绪状态**：是否能反映用户当前的情绪状态，而不是千篇一律地进行图像画面描述。
                - **与真实标题的风格贴合程度**：若你认为真实标题质量不佳，请忽略该因素。
                <span style="color: red; font-weight: bold;">若你发现某模型生成的答案与真实标题完全一样，则可能出现标签泄露，请不要选择该模型。</span>

                **注意事项：**
                - **请注意**：请用 **浏览器** 打开该网页（后续涉及下载文件）
                - **请注意**：打开左侧滑动栏能够方便查看
                - **请注意**：请对应上述角度进行认真分析
                - **请注意**：不要重复选择相同的模型
                - **请注意**：当你选择完质量第 1 高、质量第 2 高的模型后，若你认为剩余模型生成质量均不理想，可在后续选项中选择 **NULL** 项
                - **请注意**：在问卷提交后，会出现导出问卷评估数据的按钮，请点击进行下载。
                - **请注意**：每一页问卷会询问当前用户的个性标签和情绪标签，支持多选。
                """, unsafe_allow_html=True)
        

    def show_profile(self):
        anonymous_name = st.session_state['anonymous_list'][st.session_state['page_index']]
        anonymous_data = st.session_state['show_data'][anonymous_name]
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
        anonymous_name = st.session_state['anonymous_list'][st.session_state['page_index']]
        anonymous_data = st.session_state['show_data'][anonymous_name]
        # 从anonymous_data中获取history note
        history_list = anonymous_data['history']
        history_titles = []
        
        # 历史笔记
        st.markdown("""
            <div style="border: 2px solid #ccc; padding: 8px; border-radius: 10px; background-color: #f9f9f9;">
                <h4 style="color: #2978b5;">📗历史笔记:</h4>
            """, unsafe_allow_html=True
        )
        
        for i, history_note in enumerate(history_list):
            title = history_note['title']
            history_titles.append(title)
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
        with st.sidebar:
            st.markdown("### 历史笔记窗口")
            for i in range(len(history_titles)):
                title = history_titles[i]
                st.write(f"第{i+1}条历史笔记标题：{title}")
        
    def show_target(self):
        anonymous_name = st.session_state['anonymous_list'][st.session_state['page_index']]
        anonymous_data = st.session_state['show_data'][anonymous_name]
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

        anonymous_name = st.session_state['anonymous_list'][st.session_state['page_index']]
        anonymous_data = st.session_state['show_data'][anonymous_name]
        # 从anonymous_data中获取target title
        true_title = anonymous_data['target']['title']
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
            show_title = title[:25] if title != '' else 'None'
            # 使用自定义 flex 列
            st.markdown(f"""
                <div class="columnFlex">
                    <strong>{model_reverse_map[model_name]}:</strong> {show_title}
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
                <div class="columnFlex">
                    <strong>{"真实标题"}:</strong> {true_title}
                </div>
        """, unsafe_allow_html=True)

        # 结束 flex 容器
        st.markdown('</div>', unsafe_allow_html=True)

        # 创建ranking
        max_ranks = self.cfg['UI']['max_rank']
        if anonymous_name not in st.session_state['rank']:
            st.session_state['_rank'][anonymous_name] = {
                f'rank_{i+1}':{'model_name': 'NULL', 'gen_res': 'NULL'} for i in range(max_ranks)
        }    
        if anonymous_name not in st.session_state['rank']:
            st.session_state['rank'][anonymous_name] = {
                f'rank_{i+1}':{'model_name': 'NULL', 'gen_res': 'NULL'} for i in range(max_ranks)
        }    

        # 模型评估
        options = list(model_map.keys()) + ['NULL']  # 初始化选项为所有模型标签
        columns = st.columns(max_ranks)
        for i in range(max_ranks):
            with columns[i]:
                default_value = model_reverse_map[st.session_state['rank'][anonymous_name][f'rank_{i+1}']['model_name']] if st.session_state['rank'][anonymous_name][f'rank_{i+1}']['model_name'] != 'NULL' else 'NULL'
                default_index = options.index(default_value)
                selected_model = st.selectbox(f"选择质量第 {i+1} 高的模型:", options, key=f"rank_{i+1}_{st.session_state['page_index']}", index=default_index)
                if selected_model != 'NULL':
                    selected_model_name = model_map[selected_model]
                    # 匹配模型rank
                    st.session_state['_rank'][anonymous_name][f'rank_{i+1}']['model_name'] = selected_model_name
                    st.session_state['_rank'][anonymous_name][f'rank_{i+1}']['gen_res'] = self.gen_data[selected_model_name][anonymous_name]
             
    def show_tag(self):
        anonymous_name = st.session_state['anonymous_list'][st.session_state['page_index']]
        # for tag
        if anonymous_name not in st.session_state['tag']:
            st.session_state['tag'][anonymous_name] = {
                'personalization_tags': [],
                'emotion_tags': []
            }
        # for _tag
        if anonymous_name not in st.session_state['_tag']:
            st.session_state['_tag'][anonymous_name] = {
                'personalization_tags': [],
                'emotion_tags': []
            }

        st.markdown("### 🏷️个性化标签与情绪标签")

        # 个性化标签输入
        st.markdown("**个性化标签**")
        personalization_options = ["探索", "艺术", "自然", "校园", "摄影", "科技", "萌宠", "运动", "设计", "温馨", "美食", "卡通", "书籍", "自拍", "好物分享", "其他"]
        default_personalization_options = st.session_state['tag'][anonymous_name]['personalization_tags']
        selected_personalization_tags = st.multiselect("请选择用户的个性化标签（可多选）", personalization_options, key=f"personalization_{st.session_state['page_index']}", default=default_personalization_options)

        # 情绪标签选择
        st.markdown("**情绪标签**")
        emotion_options = ["期待", "好奇", "惊叹", "放松", "愉悦", "emo", "分享欲", "中性"]
        default_emotion_tags = st.session_state['tag'][anonymous_name]['emotion_tags']
        selected_emotion_tags = st.multiselect("请选择用户的情绪标签（可多选）", emotion_options, key=f"emotion_{st.session_state['page_index']}", default=default_emotion_tags)

        # 更新tag放到下一页中
        st.session_state['_tag'][anonymous_name]['personalization_tags'] = selected_personalization_tags
        st.session_state['_tag'][anonymous_name]['emotion_tags'] = selected_emotion_tags

        st.session_state['_rank'][anonymous_name]['tag'] = {
            'personalized_tags': selected_personalization_tags,
            'emotion_tags': selected_emotion_tags
        }
    
    def show_next(self):
        # 问卷调查已经开始
        if st.session_state['start']:
            # 进度条
            total_pages = len(st.session_state['anonymous_list'])
            current_page = st.session_state['page_index'] + 1
            progress_value = current_page / total_pages
            st.progress(progress_value)
            
            cols = st.columns([1, 5, 1]) 

            with cols[0]:  # 第一列
                # 只在不是第一页时显示“上一页”按钮
                if st.session_state['page_index'] > 0:
                    if st.button('上一页'):
                        st.session_state['tag'] = st.session_state['_tag']
                        st.session_state['rank'] = st.session_state['_rank'].copy()
                        self.back_data()

            with cols[2]:  # 第三列
                # 在不是最后一页时显示“下一页”按钮
                if st.session_state['page_index'] < len(st.session_state['anonymous_list']) - 1:
                    if st.button('下一页'):
                        st.session_state['tag'] = st.session_state['_tag'].copy()
                        st.session_state['rank'] = st.session_state['_rank'].copy()
                        self.forward_data()
                # 在最后一页时显示“提交问卷”按钮
                elif st.session_state['page_index'] == len(st.session_state['anonymous_list']) - 1:
                    if st.button('提交问卷'):
                        st.session_state['tag'] = st.session_state['_tag'].copy()
                        st.session_state['rank'] = st.session_state['_rank'].copy()
                        st.session_state['submitted'] = True
                        self.database.post_process(group_id=int(st.session_state['select_id']))

            if st.session_state.get('submitted', False):
                st.success('感谢您的参与！您的反馈对于我们非常重要！🎉')
                # ranking结果保存
                json_str = json.dumps(st.session_state['rank'], ensure_ascii=False, indent=4)
                now = datetime.now()
                formatted_date = now.strftime("%Y-%m-%d-%H%M%S")
                # 下载按钮
                st.markdown("### 📥下载您的评估结果")
                st.write("点击下方按钮以下载您的评估结果文件。")
                st.download_button(
                    label='📥下载JSON 结果',
                    data=json_str,
                    file_name=f'{formatted_date}.json',
                    mime='application/json'
                )
                # 数据处理提示
                st.info("我们会将您的评估结果用于进一步分析，感谢您提供的宝贵反馈！")


                        
        else:
            columns = st.columns([5, 2, 5])
            with columns[1]:
                if st.button('开始'):
                    st.session_state['start'] = True
                    st.rerun()


    def show(self, ):

        self.show_intro()
        self.show_profile()
        self.show_history()
        self.show_target()
        self.show_rank()
        self.show_tag()
        self.show_next()

    # 更新数据
    def forward_data(self):
        print("当前页码：{} -> {}".format(st.session_state['page_index'], st.session_state['anonymous_list'][st.session_state['page_index']]))  # 打印当前页码
        st.session_state['page_index'] = st.session_state['page_index'] + 1
        print("翻页后页码：{} -> {}".format(st.session_state['page_index'], st.session_state['anonymous_list'][st.session_state['page_index']]))  # 打印当前页码
        st.rerun()

    def back_data(self):
        print("当前页码：{} -> {}".format(st.session_state['page_index'], st.session_state['anonymous_list'][st.session_state['page_index']]))  # 打印当前页码
        st.session_state['page_index'] = st.session_state['page_index'] - 1
        print("回退后页码：{} -> {}".format(st.session_state['page_index'], st.session_state['anonymous_list'][st.session_state['page_index']]))  # 打印当前页码
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
        if '_rank' not in st.session_state:
            st.session_state['_rank'] = {}
        if 'start' not in st.session_state:
            st.session_state['start'] = False
        if 'tag' not in st.session_state:
            st.session_state['tag'] = {}
        if '_tag' not in st.session_state:
            st.session_state['_tag'] = {}

        # 所有模型的生成数据
        self.gen_data = self.database.gen_res

        if st.session_state['start']:
            print(f'当前选取组ID为:{select_id}')
            # 该组的展示数据
            st.session_state['show_data'] = self.database.get(group_id=select_id)
            # 获取anonymous_list
            st.session_state['anonymous_list'] = [name for name in st.session_state['show_data'] if name != 'count']
            print(f"当前匿名列表为:{st.session_state['anonymous_list']}")
            # 获取ui界面
            self.show()
        else:
            # 展示起始页
            self.show_init()

@st.fragment
def Create(cfg: dict):
    ui = UI(cfg=cfg)
    return ui

if __name__ == '__main__':
    cfg = get_cfg()
    ui = Create(cfg=cfg)
    ui.run()

        
    
    




