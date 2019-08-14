# -*-coding: utf-8 -*-
"""
    @Project: python-learning-notes
    @File   : classification_report.py
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2019-07-13 13:23:05
"""
from sklearn import metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import pandas_tools,file_processing

def plot_confusion_matrix(conf_matrix, labels_name, title,normalization=True):
    if normalization:
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]  # 归一化
    plt.imshow(conf_matrix, interpolation='nearest')  # 在特定的窗口上显示图像
    plt.title(title)  # 图像标题
    plt.colorbar()
    num_local = np.array(range(len(labels_name)))
    plt.xticks(num_local, labels_name)  # 将标签印在x轴坐标上
    plt.yticks(num_local, labels_name)  # 将标签印在y轴坐标上
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


def get_confusion_matrix(true_labels, pred_labels, class_names, filename=None,normalization=False,plot=False, title="Confusion Matrix"):
    '''
    :param true_labels: Y-ylabel
    :param pred_labels: X-xlabel
    :param class_names:
    :param labels:
    :param plot:
    :param title:
    :return:
    '''
    if class_names is None:
        class_names = list(set(pred_labels+true_labels))
        class_names.sort()
    conf_matrix = metrics.confusion_matrix(true_labels, pred_labels,class_names)
    if normalization:
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]  # 归一化
    pdf=pd.DataFrame(conf_matrix, columns=class_names, index=class_names)
    print(pdf)
    if filename is not None:
        file_processing.create_file_path(filename)
        pandas_tools.save_csv(filename,pdf,save_index=True)
    if plot:
        plot_confusion_matrix(conf_matrix, class_names, title,normalization=normalization)
    return conf_matrix


def get_classification_report(true_labels, pred_labels, labels=None, output_dict=False):
    result = metrics.classification_report(true_labels, pred_labels, labels=labels, output_dict=output_dict)
    if output_dict:
        macro_avg = result["macro avg"]
        accuracy = result["accuracy"]
        weighted_avg = result["weighted avg"]
        out_result = {"macro_avg": macro_avg, "accuracy": accuracy, "weighted_avg": weighted_avg}
        # pdf=pd.DataFrame.from_dict(result)
        # save_csv("classification_report.csv", pdf)

    else:
        out_result = result
    print("out_result:{}".format(out_result))

    return out_result


if __name__ == "__main__":
    true_labels = [0, 1, 2, 3, 4, 1]  # Y
    pred_labels = [0, 1, 1, 2, 2, 1]  # X
    # true_labels = [0, 1, 1, 2, 2]
    # pred_labels = [0, 1, 1, 2, 2]
    class_names = ["A", "B", "C", "D", "E"]
    # get_classification_report(true_labels, pred_labels, target_names, output_dict=False)
    get_confusion_matrix(true_labels, pred_labels, class_names=None, normalization=False,plot=True, title="NVR Confusion Matrix")
