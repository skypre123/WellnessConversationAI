import torch
import torch.nn as nn
from torch.utils.data import Dataset # 데이터로더

from kogpt2_transformers import get_kogpt2_tokenizer
from kobert_transformers import get_tokenizer

class WellnessAutoRegressiveDataset(Dataset):
  """Wellness Auto Regressive Dataset"""

  def __init__(self,
               file_path = "../data/wellness_dialog_for_autoregressive.txt"
               ):
    self.file_path = file_path
    self.data =[]
    self.tokenizer = get_kogpt2_tokenizer()
    bos_token_id = [self.tokenizer.bos_token_id]
    eos_token_id = [self.tokenizer.eos_token_id]

    file = open(self.file_path, 'r', encoding='utf-8')

    while True:
      line = file.readline()
      if not line:
        break
      datas = line.split("    ")
      index_of_words = bos_token_id +self.tokenizer.encode(datas[0]) + eos_token_id + bos_token_id + self.tokenizer.encode(datas[1][:-1])+ eos_token_id

      self.data.append(index_of_words)

    file.close()

  def __len__(self):
    return len(self.data)
  def __getitem__(self,index):
    item = self.data[index]
    return item

class WellnessTextClassificationDataset(Dataset):
  """Wellness Text Classification Dataset"""
  def __init__(self,
               file_path = "../data/wellness_dialog_for_text_classification.txt",
               num_label = 360,
               max_seq_len = 512, # KoBERT max_length
               ):
    self.file_path = file_path
    self.data =[]
    tokenizer = get_tokenizer()
    one_hot = torch.eye(num_label)


    file = open(self.file_path, 'r', encoding='utf-8')

    while True:
      line = file.readline()
      if not line:
        break
      datas = line.split("    ")
      index_of_words = tokenizer.encode(datas[0])
      token_type_ids = [0] * len(index_of_words)
      attention_mask = [1] * len(index_of_words)

      # Padding Length
      padding_length = max_seq_len - len(index_of_words)

      # Zero Padding
      index_of_words += [0] * padding_length
      token_type_ids += [0] * padding_length
      attention_mask += [0]
      label = one_hot[int(datas[1][:-1])]

      data = {'input':index_of_words, 'label': label}

      self.data.append(data)

    file.close()

  def __len__(self):
    return len(self.data)
  def __getitem__(self,index):
    item = self.data[index]
    return item

if __name__ == "__main__":
  dataset = WellnessAutoRegressiveDataset()
  dataset2 = WellnessTextClassificationDataset()
  print(dataset)
  print(dataset2)