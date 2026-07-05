def calculate_readiness(company_id, topic_weights, topic_practice):
    """
    topic_weights: list of dicts like [{'topic_id': 1, 'weight': 0.4}, ...]
    topic_practice: dict like {1: {'solved': 8, 'total': 10}, 2: {'solved': 5, 'total': 10}}
    """
    total_score = 0
    for tw in topic_weights:
        topic_id = tw['topic_id']
        weight = tw['weight']
        
        if topic_id in topic_practice and topic_practice[topic_id]['total'] > 0:
            coverage = topic_practice[topic_id]['solved'] / topic_practice[topic_id]['total']
        else:
            coverage = 0  # no practice logged yet for this topic
        
        total_score += weight * coverage
    
    return round(total_score * 100, 2)  # as a percentage


# Test with fake data
weights = [
    {'topic_id': 1, 'weight': 0.4},  # DP
    {'topic_id': 2, 'weight': 0.4},  # SQL
    {'topic_id': 3, 'weight': 0.2},  # Aptitude
]

practice = {
    1: {'solved': 8, 'total': 10},
    2: {'solved': 5, 'total': 10},
    3: {'solved': 3, 'total': 5},
}

print(calculate_readiness('goldman', weights, practice))  # should print 64.0