from staticfg import CFGBuilder

cfg = CFGBuilder().build_from_file('main.py', './main.py')

cfg.build_visual('main_CFG', 'png')