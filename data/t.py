with open (r'C:\Users\misha\Desktop\Important Stuff\Python Programs\Machine Learning\Medibot\TestBot\data\nlu.yml', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines() if 'intent: ' in line]

lines = lines[10:]

for i in range(len(lines)):
    lines[i] = lines[i][10:]

for line in lines:
    print (line)

with open (r'C:\Users\misha\Desktop\Important Stuff\Python Programs\Machine Learning\Medibot\TestBot\data\rules.yml', 'a', encoding='utf-8') as f:
    for line in lines:
        t = [f"- rule: Respond to {line.lower().replace('_', ' ')}\n", "  steps:\n", f"  - intent: {line}\n", "  - action: action_provide_disease_info\n", "\n"]
        f.writelines(t)