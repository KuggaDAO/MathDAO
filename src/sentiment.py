from transformers import pipeline
import json
classifier = pipeline("sentiment-analysis", 'cardiffnlp/twitter-roberta-base-sentiment', device=1)
id = 6312
with open('./misc/comment_text_{}.json'.format(id),'r') as f:
    text_list = json.load(f)
pred = classifier(text_list)
id2label = {'LABEL_0':'negative', 'LABEL_1': "neutral", 'LABEL_2': "positive"}

for i,x in enumerate(pred):
    x['sentence'] = text_list[i]
    x['label'] = id2label[x['label']]

with open('./misc/comment_sentiment_{}.json'.format(id), 'w') as f:
    json.dump(pred, f, ensure_ascii=False)

pos_cnt = len([x for x in pred if x['label']=='positive'])
neu_cnt = len([x for x in pred if x['label']=='neutral'])
neg_cnt = len([x for x in pred if x['label']=='negative'])
print(
    'id:{}'.format(id),
    'pos_cnt:{}'.format(pos_cnt),
    'neu_cnt:{}'.format(neu_cnt),
    'neg_cnt:{}'.format(neg_cnt)
)
