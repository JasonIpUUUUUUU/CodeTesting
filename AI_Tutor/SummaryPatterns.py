from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import DataCollatorForSeq2Seq
import evaluate
import numpy as np
from transformers import AdamWeightDecay
from transformers import TFAutoModelForSeq2SeqLM
import tensorflow as tf

billsum = load_dataset("billsum", split="ca_test")
billsum = billsum.train_test_split(test_size=0.2)

checkpoint = "google-t5/t5-small"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

prefix = "summarize: "

def preprocess_function(examples):
    inputs = [prefix + doc for doc in examples["text"]]
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    labels = tokenizer(text_target=examples["summary"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    result = rouge.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens)
    return {k: round(v, 4) for k, v in result.items()}

tokenized_billsum = billsum.map(preprocess_function, batched=True)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint, return_tensors="tf")
rouge = evaluate.load("rouge")

optimizer = AdamWeightDecay(learning_rate=2e-5, weight_decay_rate=0.01)
model = TFAutoModelForSeq2SeqLM.from_pretrained(checkpoint)

tf_train_set = model.prepare_tf_dataset(
    tokenized_billsum["train"],
    shuffle=True,
    batch_size=16,
    collate_fn=data_collator,
)

tf_test_set = model.prepare_tf_dataset(
    tokenized_billsum["test"],
    shuffle=False,
    batch_size=16,
    collate_fn=data_collator,
)

model.compile(optimizer=optimizer)

model.fit(
    tf_train_set,
    epochs=3,
    validation_data=tf_test_set,
    callbacks=[tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)],
    verbose=1
)

model.save_pretrained("t5_small_summarizer")
tokenizer.save_pretrained("t5_small_summarizer")