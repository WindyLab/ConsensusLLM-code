import pickle
import re

def parse_answer(sentence):
    # print(sentence)
    # Use regular expressions to find floating-point numbers
    floats = re.findall(r'[-+]?\d*\.\d+|\d+', sentence)
    # print(floats)
    # If there are floats found, return the last one; otherwise, return None
    if floats:
        return float(floats[-1])
    else:
        return None

def parse_p_file(filename):
    objects = []
    with (open(filename, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects[0]

def read_conversations(filename):
    object = parse_p_file(filename)
    conversations = [value for key, value in object.items()]
    return conversations

    
def read_from_file(filename):
    object = parse_p_file(filename)
    final_ans= []
    count = 0
    for key, value in object.items():
        text_answers = []
        agent_contexts = value
        # print("initial position is {}".format(key))
        count += 1
    
        for agent_id, agent_context in enumerate(agent_contexts):
            ans = [key[agent_id]]
            # if(count == 4):
            # print("================ agent_0{} ================".format(i))
            for i, msg in enumerate(agent_context):
                # if(agent_id == 1 and count == 2):
                    # print(msg, i)
                if(i > 0 and i % 2 == 0): # this is for user and robot
                # if(i % 3 == 2): # this is for user , robot and mathemtician
                    text_answer =  agent_context[i]['content']
                    text_answer = text_answer.replace(",", ".")
                    text_answer = parse_answer(text_answer)
                    # if(agent_id == 1 and count == 2):
                    #     print(msg, text_answer)
                    # if text_answer is None:
                    #     continue
                    # print("i: {}, answer is: {}".format(i, text_answer))
                    ans.append(text_answer)         
            text_answers.append(ans)
        final_ans.append(text_answers)
    
    return final_ans



if __name__ == "__main__":
    res = "Based on the advice of your two friends, the position to meet your friend is 65.5, which is the midpoint of your position (64) and your friend's position (67). Therefore, the position to meet your friend is 65.."
    print(parse_answer(res))

       