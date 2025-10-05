# assume user_score, difficulty, and question_history are tracked per user
# questions is the JSON dataset

def get_next_question(user_state, questions):
    # user_state includes:
    #   last_difficulty (1–3)
    #   streak_correct (count)
    #   streak_incorrect (count)
    #   seen_question_ids (list)
    
    base_diff = user_state.get("last_difficulty", 1)
    
    # ADAPT DIFFICULTY
    if user_state["streak_correct"] >= 2 and base_diff < 3:
        target_diff = base_diff + 1         # level up
    elif user_state["streak_incorrect"] >= 2 and base_diff > 1:
        target_diff = base_diff - 1         # step down
    else:
        target_diff = base_diff             # stay same level

    # SELECT NEW QUESTION
    unseen = [q for q in questions if q["id"] not in user_state["seen_question_ids"] and q["difficulty"] == target_diff]
    if not unseen:
        unseen = [q for q in questions if q["difficulty"] == target_diff]
    
    # fallback: if no questions of this difficulty remain
    if not unseen:
        unseen = [q for q in questions]
    
    next_q = random.choice(unseen)
    
    # UPDATE STATE
    user_state["last_difficulty"] = target_diff
    user_state["seen_question_ids"].append(next_q["id"])
    
    return next_q
