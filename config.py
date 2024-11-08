import os

def get_cfg():

    cfg = {}

    # File Path
    cfg["FILE_PATH"] = {
        'processed_file':'/home/tfshen/pyproject/pcg/ui/data/dataset/ui_sample.json',
        'raw_test_file':'/home/tfshen/pyproject/pcg/data/split/test.json',    
        'sample_file': '/home/tfshen/pyproject/pcg/ui/data/dataset/test_sample.txt',
        'rank_file':'/home/tfshen/pyproject/pcg/ui/data/result/all_rank.json',
        'img_dir':'/data/tfshen/pcg_imagebase',
        'navigation_path':'/data/tfshen/pcg_imagebase/navigation.json',
        'out_path':'/home/tfshen/pyproject/pcg/ui/data/dataset/ui_sample.json'
    }
    # Gen Path
    cfg["GEN_PATH"] = {
        'ofa_ft_gen_path#1': '/home/tfshen/pyproject/pcg/baselines/ofa/results/caption/translate.txt',
        'maria_ft_gen_path#1':'/data/tfshen/pcg_results/maria/pcg_maria/checkpoint-13-3000/pred-mode=test-seed=2-beam_size=3-do_sample=False-top_k=0-top_p=1-temperature=1-repetition_penalty=1.25.tsv.txt',
        'livebot_ft_gen_path#1':'',
        'mplug-video_z-shot_gen_path#1':'',
        'mplug-owl3_z-shot_gen_path#1':'',
        'qwen2-vl_z-shot_gen_path#1':'',
        'minicpm-v_z-shot_gen_path#1':'',
        'internvl_z-shot_gen_path#1':'',
        'gpt-4o_z-shot_gen_path#1': '',
    }

    # Option
    cfg['OPTION'] = {
        'mode': 'all',
        'ablation_model_name': '',
        'add_list': [],
    }

    # UI
    cfg['UI'] = {
        'max_rank': 1, # 选择前max_rank最高质量的模型
    }

    return cfg

