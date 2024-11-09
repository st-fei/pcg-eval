'''
2024.10.29 by stf
用于构建交互标注平台的数据
'''
import os
import json
import random
from tools import load_json, text_process, query

class DataBase:
    def __init__(self, cfg):
        # 参数初始化
        self.cfg = cfg
        self.processed_file = cfg['FILE_PATH']['processed_file']
        self.raw_test_file = cfg['FILE_PATH']['raw_test_file']
        self.sample_file = cfg['FILE_PATH']['sample_file']
        self.rank_file = cfg['FILE_PATH']['rank_file']
        self.img_dir = cfg['FILE_PATH']['img_dir']
        self.navigation_path = cfg['FILE_PATH']['navigation_path']
        self.out_path = cfg['FILE_PATH']['out_path']
        
        # 如果processed_file不为None，直接读取
        if self.processed_file is not None:
            self.data = load_json(self.processed_file)
        # 否则，处理匿名采样文件
        else:
            self.data = self.process(
                raw_test_file=self.raw_test_file, 
                sample_file=self.sample_file,
                out_path=self.out_path
            )
        # 建立映射
        self.id2count, self.count2id, self.name2id = self.build_map()
        # 集成不同模型生成结果
        self.gen_res = self.integrate(cfg=cfg)
        # 获取需人工评估填入的Rank结果文件
        # self.rank_res = self.init_rank(rank_file=self.rank_file)

    # 筛选候选image_indexs
    def filter_image_indexs(self, candidate_img_indexs: list, threshold=3):
        assert threshold in [2, 3], 'threshold must be 2 or 3'
        if len(candidate_img_indexs) <= threshold:
            return candidate_img_indexs
        if threshold == 2:
            st = 0
            ed = len(candidate_img_indexs) - 1
            med = None
        elif threshold == 3:
            st = 0
            ed = len(candidate_img_indexs) - 1
            med = (st + ed) >> 1

        img_indexs = [candidate_img_indexs[i] for i in [st, med, ed] if i is not None]
        return img_indexs

    # 重新组织匿名数据架构
    def reorganize(self, anonymous_data: dict):
        new_data = {}
        user = anonymous_data['user']
        history = anonymous_data['history']
        target = anonymous_data['target']
        new_data['user'] = user
        new_data['history'] = []
        note_num = len(history) + 1
        # reorganize history
        
        for history_note in history:
            title = history_note['title']
            candidate_image_indexs = history_note['image_indexs']
            if note_num > 3:
                image_indexs = self.filter_image_indexs(candidate_img_indexs=candidate_image_indexs, threshold=2)
            else:
                image_indexs = self.filter_image_indexs(candidate_img_indexs=candidate_image_indexs, threshold=3)
            image_urls = [os.path.join(query(img_dir=self.img_dir, navigation_path=self.navigation_path, index=img_index), f'image_{img_index}.png') for img_index in image_indexs]
            new_data['history'].append({
                'title': title,
                'image_indexs': image_indexs,
                'image_urls': image_urls
            })

        # reorganize target
        title = target['title']
        candidate_image_indexs = target['image_indexs']
        if note_num > 3:
            image_indexs = self.filter_image_indexs(candidate_img_indexs=candidate_image_indexs, threshold=2)
        else:
            image_indexs = self.filter_image_indexs(candidate_img_indexs=candidate_image_indexs, threshold=3)
        image_urls = [os.path.join(query(img_dir=self.img_dir, navigation_path=self.navigation_path, index=img_index), f'image_{img_index}.png') for img_index in image_indexs]
        new_data['target'] = {
                'title': title,
                'image_indexs': image_indexs,
                'image_urls': image_urls
        }

        return new_data
        
    # 对数据进行分组存储    
    def process(self,
        raw_test_file,
        sample_file,
        out_path
    ):
        data = load_json(raw_test_file)
        sample_data = {}
        sample_anonymous_list = []
        with open(sample_file, 'r', encoding='utf-8') as f:
            for line in f:
                anonymous_name = line.strip()
                if anonymous_name not in data:
                    raise ValueError(f'读取采样文件匿名{anonymous_name}不存在 ...')
                sample_anonymous_list.append(anonymous_name)

        assert len(sample_anonymous_list) == 400, f'采样匿名数据统计{len(sample_anonymous_list)} !=400'
        # Group Split
        numbers = list(range(400))
        random.shuffle(numbers)
        groups = [numbers[i: i+20] for i in range(0, 400, 20)]
        for i, group in enumerate(groups):
            # 组名
            group_name = f'Group_{i+1}'
            # 初始化
            sample_data[group_name] = {'count': 0}
            # 遍历当前组的数字切片
            for idx in group:
                anonymous_name = sample_anonymous_list[idx]
                sample_data[group_name][anonymous_name] = self.reorganize(data[anonymous_name])
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=4)
                
    # 建立映射
    # Group_ID -> count (int -> int)
    # count -> Group_ID (int -> int)
    # anonymous_name -> Group_ID
    def build_map(self, ):
        id2count = {}
        count2id = {}
        name2id = {}
        for group_idx, group_data in self.data.items():
            group_id = group_idx.split('_')[-1]
            if isinstance(group_id, str):
                group_id = int(group_id)
            cnt = group_data['count']
            # name2id
            group_name_list = [name for name in list(group_data.keys()) if name != 'count']
            for group_name in group_name_list:
                name2id[group_name] = group_id
            # id2count
            id2count[group_id] = cnt
            # count2id
            if count2id.get(cnt, -1) == -1:
                count2id[cnt] = [group_id]
            else:
                count2id[cnt].append(group_id)
        return id2count, count2id, name2id
                
    # 用于提供某一组数据作为问卷
    def get(self, group_id):
        assert group_id in list(range(1, 21)), f'Group_id:{group_id}不合法'
        return self.data[f'Group_{group_id}']
    
    # 用于随机获取当前Group Count最少的一个Group_ID
    def select(self):
        count_list = list(self.count2id.keys())
        min_count = min(count_list)
        candidate_ids = self.count2id[min_count]
        random_idx = random.randint(0, len(candidate_ids) - 1)
        group_id = candidate_ids[random_idx]
        return group_id

    # 用于在当前问卷成功后修正Group Count
    def post_process(self, group_id):
        # 修正映射
        if isinstance(group_id, str):
            group_id = int(group_id)
        pre_count = self.id2count[group_id]
        cur_count = pre_count + 1
        self.id2count[group_id] = cur_count
        self.count2id[pre_count].remove(group_id)
        if self.count2id.get(cur_count, -1) == -1:
            self.count2id[cur_count] = [group_id]
        else:
            self.count2id[cur_count].append(group_id)

        # 修正数据存储文件
        self.data[f'Group_{group_id}']['count'] = cur_count
        save_path = self.processed_file if self.processed_file is not None else self.out_path
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        
    # 用于汇聚不同模型生成结果
        # 两种模式: [all, ablation]
        # all对应所有模型，ablation对应单一模型的不同架构
    # 规范所有模型参数
        # {model_name}_{model_arch}_gen_path#{idx}
        # {model_name}用于标识模型名称，{model_arch}用于标识不同的模型架构，{idx}用来标识哪些模型用来作NDCG分数证明
    def integrate(self, cfg: dict):
        # 存储最终结果
        result = {}
        # 获取参数变量
        mode = cfg['OPTION']['mode']
        ablation_model_name = cfg['OPTION']['ablation_model_name']
        add_list = cfg['OPTION']['add_list']
        assert mode in ['all', 'ablation'], f'mode:{mode}不在规定范围内'
        gen_keys = list(cfg['GEN_PATH'].keys())
        anonymous_list = list(load_json(cfg['FILE_PATH']['raw_test_file']).keys())

        # 解析模型参数
        def parse_model_args(model_args):
            split_args = model_args.split('_')
            assert len(split_args) == 4, f'model_args:{model_args} conflicts'
            model_name = split_args[0]
            model_arch = split_args[1]
            idx = split_args[-1].split('#')[-1]
            return model_name, model_arch, idx
        
        # 解析模型生成结果
        def parse_gen_file(gen_path: str, anonymous_list: list):
            anonymous_res = {}
            with open(gen_path, 'r', encoding='utf-8') as f:
                for anonymous_name, res in zip(anonymous_list, f):
                    anonymous_res[anonymous_name] = res
            return anonymous_res

        # 遍历所有模型参数
        for gen_key in gen_keys:
            model_name, model_arch, idx = parse_model_args(gen_key)
            gen_path = cfg['GEN_PATH'][gen_key]
            if os.path.isfile(gen_path):
                # 若满足以下条件，将该模型加入result
                if (mode == 'all' and idx == '1') or (mode == 'ablation' and (gen_key in add_list or model_name == ablation_model_name)):
                    result[gen_key] = parse_gen_file(gen_path=gen_path, anonymous_list=anonymous_list)
            # 若赋值（不赋值则代表该模型结果尚未传入）
            elif gen_path != '':
                raise ValueError(f'{gen_key}参数值非合法路径')
            
        return result
            
    '''
    # 用于初始化记录Rank的文件
    def init_rank(self, rank_file):
        # 如果已存在rank_file，直接加载
        if rank_file is not None and os.path.isfile(rank_file):
            rank_res = load_json(rank_file)
            return rank_res
        # 否则，初始化rank_res
        else:
            rank_res = {}
            model_list = list(self.gen_res.keys())
            for group_id, group_value in self.data.items():
                for key in group_value:
                    # key is anonymous_name
                    if key != 'count':
                        value = group_value[key]
                        value['human_eval'] = {}
                        for i in range(self.cfg['UI']['max_rank']):
                            value['human_eval'][f'rank_{i+1}'] = {
                                'model_name': 'NULL', 
                                'gen_res': 'NULL'
                            }
                        rank_res[key] = value
            # 写入rank_file
            with open(rank_file, 'w', encoding='utf-8') as f:
                json.dump(rank_res, f, ensure_ascii=False, indent=4)
            
            return rank_res
    
    # 写入rank接口
        # rank_map结构:{anonymous_name: {rank_num: {'model_name': str, 'gen_res': str}}}
        # rank_res结构:{anonymous_name: {human_eval:{rank_name: {'model_name': str, 'gen_res': str}}}}
    def write_rank(self, rank_map:dict, rank_file: str):
        for anonymous_name in rank_map:
            self.rank_res[anonymous_name]['human_eval'] = rank_map
        # 写入rank_file
        if rank_file is not None and os.path.isfile(rank_file):
            with open(rank_file, 'w', encoding='utf-8') as f:
                json.dump(self.rank_res, f, ensure_ascii=False, indent=4)
        else:
            raise ValueError(f'rank_file参数:{rank_file}不合法')
        
    '''
            





if __name__ == "__main__":

    processed_file = "/home/tfshen/pyproject/pcg/ui/data/ui_sample.json"
    pipeline = DataBase(
        processed_file=processed_file
    )