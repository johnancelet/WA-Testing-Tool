#! /usr/bin/python
# coding: utf-8

# Copyright 2018 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Generate per intent metrics on True Positive/False Positives
"""
import csv
import pandas as pd
from argparse import ArgumentParser
from sklearn.metrics import precision_recall_fscore_support
from __init__ import UTF_8


def func(args):
    in_df = pd.read_csv(args.in_file, quoting=csv.QUOTE_ALL,
                        encoding=UTF_8, keep_default_na=False)
    # Look for target columns
    if args.test_column not in in_df or args.golden_column not in in_df:
        raise ValueError('Missing required columns')

    labels = in_df[args.golden_column].drop_duplicates().sort_values()

    precisions, recalls, _, support = \
        precision_recall_fscore_support(y_true=in_df[args.golden_column],
                                        y_pred=in_df[args.test_column],
                                        labels=labels)

    if args.partial_credit_on is not None:
        for idx, label in enumerate(labels):
            retrieved_doc_indx = in_df[args.test_column] == label
            relevant_doc_indx = in_df[args.golden_column] == label
            retrieved_doc_num = len(in_df[retrieved_doc_indx])
            relevant_doc_num  = len(in_df[relevant_doc_indx])

            precision = in_df[retrieved_doc_indx]['score'].sum() / retrieved_doc_num
            recall = in_df[relevant_doc_indx]['score'].sum()/ relevant_doc_num

            precisions[idx] = precision
            recalls[idx] = recall

    out_df = pd.DataFrame(data={'intent': labels,
                                'true positive rate': recalls,
                                'positive predictive value': precisions,
                                'number of samples': support})

    out_df.to_csv(args.out_file, encoding='utf-8', quoting=csv.QUOTE_ALL,
                  index=False, columns=['intent', 'number of samples', 'true positive rate',
                  'positive predictive value'] )


def create_parser():
    parser = ArgumentParser(
        description='Generate intent metrics')
    parser.add_argument('-i', '--in_file', type=str, required=True,
                        help='File that contains intent test and golden data')
    parser.add_argument('-o', '--out_file', type=str,
                        help='Output file path',
                        default='intent-metrics.csv')
    parser.add_argument('-t', '--test_column', type=str,
                        default='predicted intent',
                        help='Test column name')
    parser.add_argument('-g', '--golden_column', type=str,
                        default='golden intent',
                        help='Golden column name')
    parser.add_argument('-p', '--partial_credit_on', type=str,
                        help='Use only if partial credit scoring ')
    return parser


if __name__ == '__main__':
    ARGS = create_parser().parse_args()
    func(ARGS)
