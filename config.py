import os

def get_cfg():

    cfg = {}

    # File Path
    cfg["FILE_PATH"] = {
        'processed_file':'/workspaces/pcg-eval/data/dataset/ui_sample.json',
        'raw_test_file':'/workspaces/pcg-eval/data/dataset/test.json',    
        'sample_file': '/workspaces/pcg-eval/data/dataset/test_sample.txt',
        'rank_file':'',
        'img_dir':'',
        'sample_img_dir': '/workspaces/pcg-eval/data/pcg_img_sample',
        'navigation_path':'',
        'out_path':''
    }
    # Gen Path
    cfg["GEN_PATH"] = {
        'ofa_ft_gen_path#1': '/workspaces/pcg-eval/data/generation/ofa.txt',
        'maria_ft_gen_path#1':'/workspaces/pcg-eval/data/generation/maria.txt',
        'livebot_ft_gen_path#1':'/workspaces/pcg-eval/data/generation/livebot.txt',
        'mplug-video_z-shot_gen_path#1':'/workspaces/pcg-eval/data/generation/mplug-video.txt',
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
        'max_rank': 2, # 选择前max_rank最高质量的模型
    }

    return cfg

