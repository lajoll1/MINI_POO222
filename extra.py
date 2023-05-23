def get_target_joint_list():
    target_joint_set = set()
    for rule in tronc.iter('rule'): 
        rule.target_joint()