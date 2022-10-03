from transformers import pipeline
import json
classifier = pipeline("sentiment-analysis", device=2)
id = 12042
with open('./misc/comment_text_{}.json'.format(id),'r') as f:
    text_list = json.load(f)
pred = classifier(text_list)
with open('./misc/comment_sentiment_{}.json'.format(id), 'w') as f:
    json.dump(pred, f, ensure_ascii=False)

pos_cnt = len([x for x in pred if x['label']=='POSITIVE'])
neg_cnt = len([x for x in pred if x['label']=='NEGATIVE'])
print(
    'id:{}'.format(id),
    'pos_cnt:{}'.format(pos_cnt),
    'neg_cnt:{}'.format(neg_cnt)
)
