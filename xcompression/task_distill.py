# coding=utf-8
# 2019.12.2-Changed for TinyBERT task-specific distillation
#      Huawei Technologies Co., Ltd. <yinyichun@huawei.com>
# Copyright 2020 Huawei Technologies Co., Ltd.
# Copyright 2018 The Google AI Language Team Authors, The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""BERT finetuning runner."""

from __future__ import absolute_import, division, print_function

import argparse
import csv
import logging
import math
import os
import random
import sys, time
import copy
import numpy as np
import torch
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
from tqdm import tqdm, trange

from torch.nn import CrossEntropyLoss, MSELoss
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import matthews_corrcoef, f1_score

from transformer import BertTokenizer
from transformer import BertAdam
from transformer import WEIGHTS_NAME, CONFIG_NAME
from transformer.SVDEmbedding import SVDEmbedding
from transformer.TTEmbedding import TTEmbedding
from transformer.TTLinear import TTLinear
from transformer.compressed_modeling_tt import CompressedBertForSequenceClassification
from transformer.modeling import BertForSequenceClassification, BertModel
from filelock import FileLock
from torch.utils.data.distributed import DistributedSampler

logger = logging.getLogger(__name__)


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_id, seq_length=None):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.seq_length = seq_length
        self.label_id = label_id


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                if sys.version_info[0] == 2:
                    line = list(unicode(cell, 'utf-8') for cell in line)
                lines.append(line)
            return lines


class MrpcProcessor(DataProcessor):
    """Processor for the MRPC data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, i)
            text_a = line[3]
            text_b = line[4]
            label = line[0]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class MnliProcessor(DataProcessor):
    """Processor for the MultiNLI data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_matched.tsv")),
            "dev_matched")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["contradiction", "entailment", "neutral"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[8]
            text_b = line[9]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class MnliMismatchedProcessor(MnliProcessor):
    """Processor for the MultiNLI Mismatched data set (GLUE version)."""

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_mismatched.tsv")),
            "dev_matched")


class ColaProcessor(DataProcessor):
    """Processor for the CoLA data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = line[3]
            label = line[1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples


class Sst2Processor(DataProcessor):
    """Processor for the SST-2 data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, i)
            text_a = line[0]
            label = line[1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples


class StsbProcessor(DataProcessor):
    """Processor for the STS-B data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return [None]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[7]
            text_b = line[8]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class QqpProcessor(DataProcessor):
    """Processor for the STS-B data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            try:
                text_a = line[3]
                text_b = line[4]
                label = line[5]
            except IndexError:
                continue
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class QnliProcessor(DataProcessor):
    """Processor for the STS-B data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")),
            "dev_matched")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["entailment", "not_entailment"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class RteProcessor(DataProcessor):
    """Processor for the RTE data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_aug_examples(self, data_dir):
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train_aug.tsv")), "aug")

    def get_labels(self):
        """See base class."""
        return ["entailment", "not_entailment"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class WnliProcessor(DataProcessor):
    """Processor for the WNLI data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


def convert_examples_to_features(examples, label_list, max_seq_length,
                                 tokenizer, output_mode, is_aug=False, cached_features_file="cached_task"):
    """Loads a data file into a list of `InputBatch`s."""
    lock_path = cached_features_file + ".lock"

    with FileLock(lock_path):
        if os.path.exists(cached_features_file):
            logger.info("Loading features from cached file {} ".format(cached_features_file))
            features = torch.load(cached_features_file)
        else:
            label_map = {label: i for i, label in enumerate(label_list)}

            features = []
            for (ex_index, example) in enumerate(examples):
                if ex_index % 10000 == 0:
                    logger.info("Writing example %d of %d" % (ex_index, len(examples)))

                tokens_a = tokenizer.tokenize(example.text_a)

                tokens_b = None
                if example.text_b:
                    tokens_b = tokenizer.tokenize(example.text_b)
                    _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - 3)
                else:
                    if len(tokens_a) > max_seq_length - 2:
                        tokens_a = tokens_a[:(max_seq_length - 2)]

                tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
                segment_ids = [0] * len(tokens)

                if tokens_b:
                    tokens += tokens_b + ["[SEP]"]
                    segment_ids += [1] * (len(tokens_b) + 1)

                input_ids = tokenizer.convert_tokens_to_ids(tokens)
                input_mask = [1] * len(input_ids)
                seq_length = len(input_ids)

                padding = [0] * (max_seq_length - len(input_ids))
                input_ids += padding
                input_mask += padding
                segment_ids += padding

                assert len(input_ids) == max_seq_length
                assert len(input_mask) == max_seq_length
                assert len(segment_ids) == max_seq_length

                # print(example.label)

                if output_mode == "classification":
                    # label_id = label_map[example.label]
                    if is_aug:
                        label_id = 0
                    else:
                        label_id = label_map[example.label]
                elif output_mode == "regression":
                    label_id = float(example.label)
                else:
                    raise KeyError(output_mode)

                if ex_index < 5:
                    logger.info("*** Example ***")
                    logger.info("guid: %s" % (example.guid))
                    logger.info("tokens: %s" % " ".join(
                        [str(x) for x in tokens]))
                    logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
                    logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
                    logger.info(
                        "segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
                    logger.info("label: {}".format(example.label))
                    logger.info("label_id: {}".format(label_id))

                features.append(
                    InputFeatures(input_ids=input_ids,
                                  input_mask=input_mask,
                                  segment_ids=segment_ids,
                                  label_id=label_id,
                                  seq_length=seq_length))
            torch.save(features, cached_features_file)
    return features


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def simple_accuracy(preds, labels):
    return (preds == labels).mean()


def acc_and_f1(preds, labels):
    acc = simple_accuracy(preds, labels)
    f1 = f1_score(y_true=labels, y_pred=preds)
    return {
        "acc": acc,
        "f1": f1,
        "acc_and_f1": (acc + f1) / 2,
    }


def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    spearman_corr = spearmanr(preds, labels)[0]
    return {
        "pearson": pearson_corr,
        "spearmanr": spearman_corr,
        "corr": (pearson_corr + spearman_corr) / 2,
    }


def compute_metrics(task_name, preds, labels):
    assert len(preds) == len(labels)
    if task_name == "cola":
        return {"mcc": matthews_corrcoef(labels, preds)}
    elif task_name == "sst-2":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "mrpc":
        return acc_and_f1(preds, labels)
    elif task_name == "sts-b":
        return pearson_and_spearman(preds, labels)
    elif task_name == "qqp":
        return acc_and_f1(preds, labels)
    elif task_name == "mnli":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "mnli-mm":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "qnli":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "rte":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "wnli":
        return {"acc": simple_accuracy(preds, labels)}
    else:
        raise KeyError(task_name)


def get_tensor_data(output_mode, features):
    if output_mode == "classification":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long)
    elif output_mode == "regression":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.float)

    all_seq_lengths = torch.tensor([f.seq_length for f in features], dtype=torch.long)
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    tensor_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids,
                                all_label_ids, all_seq_lengths)
    return tensor_data, all_label_ids


def result_to_file(result, file_name):
    with open(file_name, "a") as writer:
        logger.info("***** Eval results *****")
        for key in sorted(result.keys()):
            logger.info("  %s = %s", key, str(result[key]))
            writer.write("%s = %s\n" % (key, str(result[key])))


def do_eval(model, task_name, eval_dataloader,
            device, output_mode, eval_labels, num_labels):
    eval_loss = 0
    nb_eval_steps = 0
    preds = []
    model.eval()
    for batch_ in tqdm(eval_dataloader, desc="Evaluating", mininterval=120, maxinterval=300):
        batch_ = tuple(t.to(device) for t in batch_)
        with torch.no_grad():
            input_ids, input_mask, segment_ids, label_ids, seq_lengths = batch_

            # logits, _, _ = model(input_ids, segment_ids, input_mask)
            logits, _, _ = model(input_ids, input_mask, segment_ids)

        # create eval loss and other metric required by the task
        if output_mode == "classification":
            loss_fct = CrossEntropyLoss()
            tmp_eval_loss = loss_fct(logits.view(-1, num_labels), label_ids.view(-1))
        elif output_mode == "regression":
            loss_fct = MSELoss()
            tmp_eval_loss = loss_fct(logits.view(-1), label_ids.view(-1))

        eval_loss += tmp_eval_loss.mean().item()
        nb_eval_steps += 1
        if len(preds) == 0:
            preds.append(logits.detach().cpu().numpy())
        else:
            preds[0] = np.append(
                preds[0], logits.detach().cpu().numpy(), axis=0)

    eval_loss = eval_loss / nb_eval_steps

    preds = preds[0]
    if output_mode == "classification":
        preds = np.argmax(preds, axis=1)
    elif output_mode == "regression":
        preds = np.squeeze(preds)
    # print(preds,eval_labels.numpy())
    result = compute_metrics(task_name, preds, eval_labels.numpy())
    result['eval_loss'] = eval_loss
    model.train()
    return result


processors = {
    "cola": ColaProcessor,
    "mnli": MnliProcessor,
    "mnli-mm": MnliMismatchedProcessor,
    "mrpc": MrpcProcessor,
    "sst-2": Sst2Processor,
    "sts-b": StsbProcessor,
    "qqp": QqpProcessor,
    "qnli": QnliProcessor,
    "rte": RteProcessor,
    "wnli": WnliProcessor
}

output_modes = {
    "cola": "classification",
    "mnli": "classification",
    "mrpc": "classification",
    "sst-2": "classification",
    "sts-b": "regression",
    "qqp": "classification",
    "qnli": "classification",
    "rte": "classification",
    "wnli": "classification"
}

# intermediate distillation default parameters

default_params = {
    "cola": {"num_train_epochs": 50, "max_seq_length": 64},
    "mnli": {"num_train_epochs": 3, "max_seq_length": 128},
    "mrpc": {"num_train_epochs": 20, "max_seq_length": 128},
    "sst-2": {"num_train_epochs": 5, "max_seq_length": 64},
    "sts-b": {"num_train_epochs": 10, "max_seq_length": 128},
    "qqp": {"num_train_epochs": 3, "max_seq_length": 128},
    "qnli": {"num_train_epochs": 10, "max_seq_length": 128},
    "rte": {"num_train_epochs": 20, "max_seq_length": 128}
}

default_params_first = {
    "cola": {"num_train_epochs": 20, "max_seq_length": 64},
    "mnli": {"num_train_epochs": 3, "max_seq_length": 128},
    "mrpc": {"num_train_epochs": 40, "max_seq_length": 128},
    "sst-2": {"num_train_epochs": 5, "max_seq_length": 64},
    "sts-b": {"num_train_epochs": 15, "max_seq_length": 128},
    "qqp": {"num_train_epochs": 3, "max_seq_length": 128},
    "qnli": {"num_train_epochs": 10, "max_seq_length": 128},
    "rte": {"num_train_epochs": 20, "max_seq_length": 128}
}
default_params_second = {
    "cola": {"num_train_epochs": 30, "max_seq_length": 64},
    "mnli": {"num_train_epochs": 3, "max_seq_length": 128},
    "mrpc": {"num_train_epochs": 40, "max_seq_length": 128},
    "sst-2": {"num_train_epochs": 5, "max_seq_length": 64},
    "sts-b": {"num_train_epochs": 5, "max_seq_length": 128},
    "qqp": {"num_train_epochs": 3, "max_seq_length": 128},
    "qnli": {"num_train_epochs": 10, "max_seq_length": 128},
    "rte": {"num_train_epochs": 20, "max_seq_length": 128}
}

acc_tasks = ["mnli", "mrpc", "sst-2", "qqp", "qnli", "rte"]
corr_tasks = ["sts-b"]
mcc_tasks = ["cola"]


def soft_cross_entropy(predicts, targets):
    student_likelihood = torch.nn.functional.log_softmax(predicts, dim=-1)
    targets_prob = torch.nn.functional.softmax(targets, dim=-1)
    return (- targets_prob * student_likelihood).mean()


def train_and_evaluate(args, teacher_model, student_model, train_dataloader, tokenizer, label_list, device, output_mode,
                       train_examples, num_labels, eval_examples, eval_labels, eval_dataloader, eval_data):
    # Train and evaluate
    task_name = args.task_name.lower()
    # if task_name in default_params:
    #     args.num_train_epochs = default_params[task_name]["num_train_epochs"]
    if not args.pred_distill:
        args.num_train_epochs = default_params_first[task_name]["num_train_epochs"]
    else:
        args.num_train_epochs = default_params_second[task_name]["num_train_epochs"]

    num_train_optimization_steps = int(
        len(train_examples) / args.train_batch_size / args.gradient_accumulation_steps) * args.num_train_epochs

    logger.info("***** Running training *****")
    logger.info("  Task name = %s", args.task_name)
    logger.info("  Num examples = %d", len(train_examples))
    logger.info("  Batch size = %d", args.train_batch_size)
    logger.info("  Num steps = %d", num_train_optimization_steps)

    # args.num_train_epochs =1
    param_optimizer = list(student_model.named_parameters())
    size = 0
    emb_size = 0
    for n, p in student_model.named_parameters():
        if 'embeddings' in n:
            emb_size += p.nelement()
        size += p.nelement()

    logger.info('Total parameters: {}'.format(size))
    logger.info('Embedding parameters: {}'.format(emb_size))
    logger.info('Backbone parameters: {}'.format(size - emb_size))
    no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
    schedule = 'warmup_linear'
    if not args.pred_distill:
        schedule = 'none'
    optimizer = BertAdam(optimizer_grouped_parameters,
                         schedule=schedule,
                         lr=args.learning_rate,
                         warmup=args.warmup_proportion,
                         t_total=num_train_optimization_steps)
    # Prepare loss functions
    loss_mse = MSELoss()

    global_step = 0
    best_dev_acc = 0.0
    output_eval_file = os.path.join(args.output_dir, "eval_results.txt")

    for epoch_ in trange(int(args.num_train_epochs), desc="Epoch"):
        tr_loss = 0.
        tr_att_loss = 0.
        tr_rep_loss = 0.
        tr_cls_loss = 0.

        student_model.train()
        nb_tr_examples, nb_tr_steps = 0, 0

        for step, batch in enumerate(
                tqdm(train_dataloader, desc="Iteration", mininterval=120, maxinterval=300, ascii=True)):
            batch = tuple(t.to(device) for t in batch)

            input_ids, input_mask, segment_ids, label_ids, seq_lengths = batch
            if input_ids.size()[0] != args.train_batch_size:
                continue

            att_loss = 0.
            rep_loss = 0.
            cls_loss = 0.

            student_logits, student_reps, student_atts = student_model(input_ids, input_mask, segment_ids)

            with torch.no_grad():
                teacher_logits, teacher_reps, teacher_atts = teacher_model(input_ids, input_mask, segment_ids)

            if not args.pred_distill:
                teacher_layer_num = len(teacher_atts)
                student_layer_num = len(student_atts)
                # assert teacher_layer_num % student_layer_num == 0

                new_teacher_atts = teacher_atts[-1]
                new_student_atts = student_atts[-1]

                for student_att, teacher_att in zip(new_student_atts, new_teacher_atts):
                    student_att = torch.where(student_att <= -1e2, torch.zeros_like(student_att).to(device),
                                              student_att)
                    teacher_att = torch.where(teacher_att <= -1e2, torch.zeros_like(teacher_att).to(device),
                                              teacher_att)

                    tmp_loss = loss_mse(student_att, teacher_att)
                    att_loss += tmp_loss

                new_teacher_reps = teacher_reps[-1]
                new_student_reps = student_reps[-1]
                for student_rep, teacher_rep in zip(new_student_reps, new_teacher_reps):
                    tmp_loss = loss_mse(student_rep, teacher_rep)
                    rep_loss += tmp_loss

                loss = rep_loss + att_loss
                tr_att_loss += att_loss.item()
                tr_rep_loss += rep_loss.item()
            else:
                if output_mode == "classification":
                    cls_loss = soft_cross_entropy(student_logits / args.temperature,
                                                  teacher_logits / args.temperature)
                elif output_mode == "regression":
                    loss_mse = MSELoss()
                    cls_loss = loss_mse(student_logits.view(-1), label_ids.view(-1))

                loss = cls_loss
                tr_cls_loss += cls_loss.item()

            if torch.cuda.device_count() > 1:
                loss = loss.mean()  # mean() to average on multi-gpu.
            if args.gradient_accumulation_steps > 1:
                loss = loss / args.gradient_accumulation_steps

            loss.backward()

            tr_loss += loss.item()
            nb_tr_examples += label_ids.size(0)
            nb_tr_steps += 1

            if (step + 1) % args.gradient_accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()
                global_step += 1

            if not (args.local_rank == -1 or args.local_rank == 0):
                continue

            if (global_step + 1) % args.eval_step == 0:
                logger.info("***** Running evaluation *****")
                logger.info("  Task name  = %s", args.task_name)
                logger.info("  Epoch = {} iter {} step".format(epoch_, global_step))
                logger.info("  Num examples = %d", len(eval_examples))
                logger.info("  Batch size = %d", args.eval_batch_size)

                student_model.eval()

                loss = tr_loss / (step + 1)
                cls_loss = tr_cls_loss / (step + 1)
                att_loss = tr_att_loss / (step + 1)
                rep_loss = tr_rep_loss / (step + 1)

                result = {}
                result = do_eval(student_model, task_name, eval_dataloader,
                                 device, output_mode, eval_labels, num_labels)
                result['global_step'] = global_step
                result['cls_loss'] = cls_loss
                result['att_loss'] = att_loss
                result['rep_loss'] = rep_loss
                result['loss'] = loss

                result_to_file(result, output_eval_file)

                save_model = True

                if save_model:
                    logger.info("***** Save model *****")

                    model_to_save = student_model.module if hasattr(student_model, 'module') else student_model

                    model_name = WEIGHTS_NAME
                    if not args.pred_distill:
                        model_name = "step_{}_{}".format(global_step, WEIGHTS_NAME)
                    else:
                        model_name = "stage_{}_{}".format(global_step, WEIGHTS_NAME)
                    output_model_file = os.path.join(args.output_dir, model_name)
                    output_config_file = os.path.join(args.output_dir, CONFIG_NAME)

                    torch.save(model_to_save.state_dict(), output_model_file)
                    model_to_save.config.to_json_file(output_config_file)
                    tokenizer.save_vocabulary(args.output_dir)

                    # Test mnli-mm
                    if args.pred_distill and task_name == "mnli":
                        task_name = "mnli-mm"
                        processor = processors[task_name]()
                        if not os.path.exists(args.output_dir + '-MM'):
                            os.makedirs(args.output_dir + '-MM')

                        eval_examples = processor.get_dev_examples(args.data_dir)

                        cached_features_file = "cached_{}_{}_{}_{}".format("dev", tokenizer.__class__.__name__,
                                                                           str(args.max_seq_len), task_name)

                        eval_features = convert_examples_to_features(
                            eval_examples, label_list, args.max_seq_len, tokenizer, output_mode,
                            cached_features_file=cached_features_file)
                        eval_data, eval_labels = get_tensor_data(output_mode, eval_features)

                        logger.info("***** Running mm evaluation *****")
                        logger.info("  Num examples = %d", len(eval_examples))
                        logger.info("  Batch size = %d", args.eval_batch_size)

                        eval_sampler = SequentialSampler(eval_data)
                        eval_dataloader = DataLoader(eval_data, sampler=eval_sampler,
                                                     batch_size=args.eval_batch_size)

                        result = do_eval(student_model, task_name, eval_dataloader,
                                         device, output_mode, eval_labels, num_labels)

                        result['global_step'] = global_step

                        tmp_output_eval_file = os.path.join(args.output_dir + '-MM', "eval_results.txt")
                        result_to_file(result, tmp_output_eval_file)

                        task_name = 'mnli'

                student_model.train()


def decompose(model):
    # model = BertModel.from_pretrained('models/bert-base-uncased')
    print(model)
    if hasattr(model, 'bert'):
        model = model.bert
    model.embeddings.word_embeddings = SVDEmbedding(num_embeddings=model.embeddings.word_embeddings.num_embeddings,
                                                    embedding_dim=model.embeddings.word_embeddings.embedding_dim,
                                                    compression_ratio=4.5,
                                                    weights=model.embeddings.word_embeddings.weight)

    # model.pooler.dense = TTLinear(in_features=model.pooler.dense.in_features,
    #                               out_features=model.pooler.dense.out_features, bias=True, in_shapes=[32, 24],
    #                               out_shapes=[768], ranks=[1, 9, 9, 1], dense_w=model.pooler.dense.weight.data,
    #                               dense_b=model.pooler.dense.bias.data)
    for layer in model.encoder.layer:
        layer.attention.self.query = TTLinear(in_features=layer.attention.self.query.in_features,
                                              out_features=layer.attention.self.query.out_features, bias=True,
                                              in_shapes=[24, 32],
                                              out_shapes=[768], ranks=[1, 18, 18, 1],
                                              dense_w=layer.attention.self.query.weight.data,
                                              dense_b=layer.attention.self.query.bias.data)
        layer.attention.self.key = TTLinear(in_features=layer.attention.self.key.in_features,
                                            out_features=layer.attention.self.key.out_features, bias=True,
                                            in_shapes=[24, 32],
                                            out_shapes=[768], ranks=[1, 18, 18, 1],
                                            dense_w=layer.attention.self.key.weight.data,
                                            dense_b=layer.attention.self.key.bias.data)
        layer.attention.self.value = TTLinear(in_features=layer.attention.self.value.in_features,
                                              out_features=layer.attention.self.value.out_features, bias=True,
                                              in_shapes=[24, 32],
                                              out_shapes=[768], ranks=[1, 18, 18, 1],
                                              dense_w=layer.attention.self.value.weight.data,
                                              dense_b=layer.attention.self.value.bias.data)
        layer.attention.output.dense = TTLinear(in_features=layer.attention.output.dense.in_features,
                                                out_features=layer.attention.output.dense.out_features, bias=True,
                                                in_shapes=[24, 32],
                                                out_shapes=[768], ranks=[1, 18, 18, 1],
                                                dense_w=layer.attention.output.dense.weight.data,
                                                dense_b=layer.attention.output.dense.bias.data)
        layer.intermediate.dense = TTLinear(in_features=layer.intermediate.dense.in_features,
                                            out_features=layer.intermediate.dense.out_features, bias=True,
                                            in_shapes=[layer.intermediate.dense.in_features], out_shapes=[64, 48],
                                            ranks=[1, 18, 18, 1],
                                            dense_w=layer.intermediate.dense.weight.data,
                                            dense_b=layer.intermediate.dense.bias.data)
        layer.output.dense = TTLinear(in_features=layer.output.dense.in_features,
                                      out_features=layer.output.dense.out_features, bias=True,
                                      in_shapes=[48, 64], out_shapes=[layer.output.dense.out_features],
                                      ranks=[1, 17, 17, 1],
                                      dense_w=layer.output.dense.weight.data,
                                      dense_b=layer.output.dense.bias.data)


def test():
    t = torch.randn([144, 768, 768])
    c = 50
    svd_r = int(768 / (2 * c))
    ms = []
    for i in range(144):
        m = t[i, :, :].numpy()
        u, s, v = np.linalg.svd(m, full_matrices=False)
        u = u[:, :svd_r]
        s = s[:svd_r]
        v = v[:svd_r, :]
        ms.append(u @ np.diag(s) @ v)
    ms = torch.as_tensor(ms)
    print(torch.sum(torch.abs(t - ms)))

    tucker_r = int((math.sqrt((2 * 768) ** 2 - 4 * 144 * (144 * 144 - t.numel() / c)) - 2 * 768) / (2 * 144))
    from tensorly.decomposition import tucker, tensor_train
    import tensorly as tl
    tl.set_backend('pytorch')
    core, factors = tucker(t, rank=[144, tucker_r, tucker_r], init='random', verbose=True)
    n = core.numel()
    print(core.shape)
    for fac in factors:
        n += fac.numel()
        print(fac.shape)
    print(t.numel() / n)
    r_t = tl.tucker_to_tensor((core, factors))
    print(torch.sum(torch.abs(t - r_t)))

    tt_r = int((math.sqrt((768 + 144) ** 2 + 4 * 768 * (t.numel() / c)) - (768 + 144)) / (2 * 768))
    if tt_r > 144:
        tt_r = int((t.numel() / c - 144 * 144) / (768 * 145))

    tt = tensor_train(t, rank=[1, tt_r, tt_r, 1], verbose=True)
    n = 0
    for fac in tt:
        n += fac.numel()
        print(fac.shape)
    print(t.numel() / n)
    r_t = tl.tt_to_tensor(tt)
    print(torch.sum(torch.abs(t - r_t)))


def main1():
    model = BertModel.from_pretrained('models/bert-base-uncased')
    decompose(model)
    # print(model)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The input data dir. Should contain the .tsv files (or other data files) for the task.")
    parser.add_argument("--teacher_model",
                        default=None,
                        type=str,
                        help="The teacher model dir.")
    parser.add_argument("--student_model",
                        default=None,
                        type=str,
                        required=True,
                        help="The student model dir.")
    parser.add_argument("--task_name",
                        default=None,
                        type=str,
                        required=True,
                        help="The name of the task to train.")
    parser.add_argument("--output_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--cache_dir",
                        default="",
                        type=str,
                        help="Where do you want to store the pre-trained models downloaded from s3")
    parser.add_argument("--max_seq_length",
                        default=128,
                        type=int,
                        help="The maximum total input sequence length after WordPiece tokenization. \n"
                             "Sequences longer than this will be truncated, and sequences shorter \n"
                             "than this will be padded.")
    parser.add_argument("--do_lower_case",
                        action='store_true',
                        help="Set this flag if you are using an uncased model.")
    parser.add_argument("--train_batch_size",
                        default=32,
                        type=int,
                        help="Total batch size for training.")
    parser.add_argument("--eval_batch_size",
                        default=32,
                        type=int,
                        help="Total batch size for eval.")
    parser.add_argument("--learning_rate",
                        default=5e-5,
                        type=float,
                        help="The initial learning rate for Adam.")
    parser.add_argument('--weight_decay', '--wd',
                        default=1e-4,
                        type=float,
                        metavar='W',
                        help='weight decay')
    parser.add_argument("--num_train_epochs",
                        default=3.0,
                        type=float,
                        help="Total number of training epochs to perform.")
    parser.add_argument("--warmup_proportion",
                        default=0.1,
                        type=float,
                        help="Proportion of training to perform linear learning rate warmup for. "
                             "E.g., 0.1 = 10%% of training.")
    parser.add_argument("--no_cuda",
                        action='store_true',
                        help="Whether not to use CUDA when available")
    parser.add_argument('--seed',
                        type=int,
                        default=526,
                        help="random seed for initialization")
    parser.add_argument('--gradient_accumulation_steps',
                        type=int,
                        default=1,
                        help="Number of updates steps to accumulate before performing a backward/update pass.")

    # added arguments
    parser.add_argument('--aug_train',
                        action='store_true')
    parser.add_argument('--eval_step',
                        type=int,
                        default=500)
    parser.add_argument('--pred_distill',
                        action='store_true')
    parser.add_argument('--data_url',
                        type=str,
                        default="")
    parser.add_argument('--temperature',
                        type=float,
                        default=1.)
    parser.add_argument('--train_url',
                        type=str,
                        default="NVIDIA")
    parser.add_argument("--local_rank",
                        type=int,
                        default=-1,
                        help="local_rank for distributed training on gpus")

    args = parser.parse_args()
    logger.info('The args: {}'.format(args))

    # Prepare devices
    device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
    n_gpu = torch.cuda.device_count()

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)

    logger.info("device: {} n_gpu: {}".format(device, n_gpu))

    # Prepare seed
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

    # Prepare task settings
    if os.path.exists(args.output_dir) and os.listdir(args.output_dir):
        raise ValueError("Output directory ({}) already exists and is not empty.".format(args.output_dir))
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if args.local_rank == -1:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        n_gpu = torch.cuda.device_count()
        print(n_gpu)
    else:
        torch.cuda.set_device(args.local_rank)
        device = torch.device("cuda", args.local_rank)
        n_gpu = 1
        # Initializes the distributed backend which will take care of sychronizing nodes/GPUs
        torch.distributed.init_process_group(backend='nccl')

    task_name = args.task_name.lower()

    if task_name in default_params:
        args.max_seq_len = default_params[task_name]["max_seq_length"]

    if task_name not in processors:
        raise ValueError("Task not found: %s" % task_name)

    processor = processors[task_name]()
    output_mode = output_modes[task_name]
    label_list = processor.get_labels()
    num_labels = len(label_list)
    from transformers import BertTokenizer
    tokenizer = BertTokenizer(os.path.join(args.student_model, 'vocab.txt'), do_lower_case=True)
    # tokenizer = BertTokenizer.from_pretrained(args.student_model, do_lower_case=args.do_lower_case)

    if not args.aug_train:
        train_examples = processor.get_train_examples(args.data_dir)
    else:
        train_examples = processor.get_aug_examples(args.data_dir)
    if args.gradient_accumulation_steps < 1:
        raise ValueError("Invalid gradient_accumulation_steps parameter: {}, should be >= 1".format(
            args.gradient_accumulation_steps))

    args.train_batch_size = args.train_batch_size // args.gradient_accumulation_steps

    cached_features_file = "cached_{}_{}_{}_{}".format("train", tokenizer.__class__.__name__, str(args.max_seq_len),
                                                       args.task_name)
    train_features = convert_examples_to_features(train_examples, label_list,
                                                  args.max_seq_len, tokenizer, output_mode, is_aug=args.aug_train,
                                                  cached_features_file=os.path.join(args.data_dir,
                                                                                    cached_features_file))
    train_data, _ = get_tensor_data(output_mode, train_features)

    if args.local_rank == -1:
        train_sampler = RandomSampler(train_data)
    else:
        train_sampler = DistributedSampler(train_data, num_replicas=1, rank=0)

    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=args.train_batch_size)

    cached_features_file = "cached_{}_{}_{}_{}".format("dev", tokenizer.__class__.__name__, str(args.max_seq_len),
                                                       args.task_name)
    print("used cached_features_file for dev in {}".format(cached_features_file))
    eval_examples = processor.get_dev_examples(args.data_dir)
    eval_features = convert_examples_to_features(eval_examples, label_list, args.max_seq_len, tokenizer, output_mode,
                                                 cached_features_file=os.path.join(args.data_dir, cached_features_file))

    eval_data, eval_labels = get_tensor_data(output_mode, eval_features)

    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=args.eval_batch_size, shuffle=False)

    teacher_model = BertForSequenceClassification.from_pretrained(args.teacher_model, num_labels=num_labels)
    # student_model = BertForSequenceClassification.from_pretrained(args.student_model, num_labels=num_labels)
    model = BertForSequenceClassification.from_pretrained(args.teacher_model, num_labels=num_labels)
    decompose(model)
    student_model = CompressedBertForSequenceClassification.from_scratch(args.student_model, num_labels=num_labels)
    student_model.load_state_dict(model.state_dict(), False)
    # target = torch.load('output/bert-tt-bak/step_79999_pytorch_model.bin')
    # student_model.bert.load_state_dict(target, False)
    # s = student_model.state_dict()
    # t = copy.deepcopy(teacher_model.state_dict())
    # target = {}
    # for k, v in t.items():
    #     if k in s and s[k].shape == v.shape:
    #         target[k] = v
    # student_model.load_state_dict(target, False)
    student_model.to(device)
    teacher_model.to(device)

    if n_gpu > 1:
        student_model = torch.nn.DataParallel(student_model)
        teacher_model = torch.nn.DataParallel(teacher_model)

    logger.info("***** Running teacher evaluation *****")
    logger.info("  Task name = %s", args.task_name)
    logger.info("  Num examples = %d", len(eval_examples))
    logger.info("  Batch size = %d", args.eval_batch_size)
    result = do_eval(teacher_model, task_name, eval_dataloader,
                     device, output_mode, eval_labels, num_labels)
    logger.info("***** Eval results *****")

    for key in sorted(result.keys()):
        logger.info("  %s = %s", key, str(result[key]))

    logger.info("***** Running student evaluation *****")
    print("  Task name = ", args.task_name)
    logger.info("  Num examples = %d", len(eval_examples))
    logger.info("  Batch size = %d", args.eval_batch_size)
    result = do_eval(student_model, task_name, eval_dataloader,
                     device, output_mode, eval_labels, num_labels)
    logger.info("***** Eval results *****")
    logger.info("  Task name = %s", args.task_name)
    for key in sorted(result.keys()):
        logger.info("  %s = %s", key, str(result[key]))

    args.pred_distill = False
    train_and_evaluate(args, teacher_model, student_model, train_dataloader, tokenizer, label_list, device,
                       output_mode, train_examples, num_labels, eval_examples, eval_labels, eval_dataloader, eval_data)
    args.pred_distill = True
    # args.eval_step = 2500
    train_and_evaluate(args, teacher_model, student_model, train_dataloader, tokenizer, label_list, device,
                       output_mode, train_examples, num_labels, eval_examples, eval_labels, eval_dataloader, eval_data)

    logger.info("***** Running student evaluation *****")
    logger.info("  Task name = %s", args.task_name)
    logger.info("  Num examples = %d", len(eval_examples))
    logger.info("  Batch size = %d", args.eval_batch_size)

    result = do_eval(student_model, task_name, eval_dataloader,
                     device, output_mode, eval_labels, num_labels)
    logger.info("***** Eval results *****")
    logger.info("  Task name = %s", args.task_name)
    for key in sorted(result.keys()):
        logger.info("  %s = %s", key, str(result[key]))

def export_onnx():
    model = BertModel.from_pretrained('models/bert-base-uncased')
    decompose(model)
    model_name = 'tt_bert_base'

    export_module = {
        # TTLinear,
        torch.nn.LayerNorm,
        torch.nn.GroupNorm,
        torch.nn.SiLU,
        torch.nn.GELU,
    }

    dummy_input = torch.randint(0, 30522, (1, 128), dtype=torch.int32)

    # Export the model
    torch.onnx.export(model,         # model being run
                      dummy_input,       # model input (or a tuple for multiple inputs)
                      "../onnx/{}_func_ln.onnx".format(model_name),
                      export_params=True,  # store the trained parameter weights inside the model file
                      opset_version=17,    # the ONNX version to export the model to
                      do_constant_folding=True,  # whether to execute constant folding for optimization
                      input_names = ['modelInput'],   # the model's input names
                      output_names = ['modelOutput'], # the model's output names
                      # export_modules_as_functions=export_module,
                      )


if __name__ == "__main__":
    export_onnx()
