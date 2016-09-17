from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from caffe2.python import core, workspace
from caffe2.python.test_util import TestCase

import numpy as np


class TestSparseToDenseMask(TestCase):

    def test_sparse_to_dense_mask_float(self):
        op = core.CreateOperator(
            'SparseToDenseMask',
            ['indices', 'values', 'default', 'lengths'],
            ['output'],
            mask=[999999999, 2, 6])
        workspace.FeedBlob(
            'indices',
            np.array([2, 4, 6, 1, 2, 999999999, 2], dtype=np.int32))
        workspace.FeedBlob(
            'values',
            np.array([1, 2, 3, 4, 5, 6, 7], dtype=np.float))
        workspace.FeedBlob('default', np.array(-1, dtype=np.float))
        workspace.FeedBlob('lengths', np.array([3, 4], dtype=np.int32))
        workspace.RunOperatorOnce(op)
        output = workspace.FetchBlob('output')
        expected = np.array([[-1, 1, 3], [6, 7, -1]], dtype=np.float)
        self.assertEqual(output.shape, expected.shape)
        np.testing.assert_array_equal(output, expected)

    def test_sparse_to_dense_mask_subtensor(self):
        op = core.CreateOperator(
            'SparseToDenseMask',
            ['indices', 'values', 'default', 'lengths'],
            ['output'],
            mask=[999999999, 2, 888, 6])
        workspace.FeedBlob(
            'indices',
            np.array([2, 4, 6, 999999999, 2], dtype=np.int64))
        workspace.FeedBlob(
            'values',
            np.array([[[1, -1]], [[2, -2]], [[3, -3]], [[4, -4]], [[5, -5]]],
                     dtype=np.float))
        workspace.FeedBlob('default', np.array([[-1, 0]], dtype=np.float))
        workspace.FeedBlob('lengths', np.array([2, 3], dtype=np.int32))
        workspace.RunOperatorOnce(op)
        output = workspace.FetchBlob('output')
        expected = np.array([
            [[[-1, 0]], [[1, -1]], [[-1, 0]], [[-1, 0]]],
            [[[4, -4]], [[5, -5]], [[-1, 0]], [[3, -3]]]], dtype=np.float)
        self.assertEqual(output.shape, expected.shape)
        np.testing.assert_array_equal(output, expected)

    def test_sparse_to_dense_mask_string(self):
        op = core.CreateOperator(
            'SparseToDenseMask',
            ['indices', 'values', 'default', 'lengths'],
            ['output'],
            mask=[999999999, 2, 6])
        workspace.FeedBlob(
            'indices',
            np.array([2, 4, 6, 1, 2, 999999999, 2], dtype=np.int32))
        workspace.FeedBlob(
            'values',
            np.array(['1', '2', '3', '4', '5', '6', '7'], dtype=np.str))
        workspace.FeedBlob('default', np.array('-1', dtype=np.str))
        workspace.FeedBlob('lengths', np.array([3, 4], dtype=np.int32))
        workspace.RunOperatorOnce(op)
        output = workspace.FetchBlob('output')
        expected = np.array([['-1', '1', '3'], ['6', '7', '-1']], dtype=np.str)
        self.assertEqual(output.shape, expected.shape)
        np.testing.assert_array_equal(output, expected)

    def test_sparse_to_dense_mask_empty_lengths(self):
        op = core.CreateOperator(
            'SparseToDenseMask',
            ['indices', 'values', 'default', 'lengths'],
            ['output'],
            mask=[1, 2, 6])
        workspace.FeedBlob('indices', np.array([2, 4, 6], dtype=np.int32))
        workspace.FeedBlob('values', np.array([1, 2, 3], dtype=np.float))
        workspace.FeedBlob('default', np.array(-1, dtype=np.float))
        workspace.FeedBlob('lengths', np.array([], dtype=np.int32))
        workspace.RunOperatorOnce(op)
        output = workspace.FetchBlob('output')
        expected = np.array([-1, 1, 3], dtype=np.float)
        self.assertEqual(output.shape, expected.shape)
        np.testing.assert_array_equal(output, expected)

    def test_sparse_to_dense_mask_no_lengths(self):
        op = core.CreateOperator(
            'SparseToDenseMask',
            ['indices', 'values', 'default'],
            ['output'],
            mask=[1, 2, 6])
        workspace.FeedBlob('indices', np.array([2, 4, 6], dtype=np.int32))
        workspace.FeedBlob('values', np.array([1, 2, 3], dtype=np.float))
        workspace.FeedBlob('default', np.array(-1, dtype=np.float))
        workspace.RunOperatorOnce(op)
        output = workspace.FetchBlob('output')
        expected = np.array([-1, 1, 3], dtype=np.float)
        self.assertEqual(output.shape, expected.shape)
        np.testing.assert_array_equal(output, expected)
